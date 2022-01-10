import os
import shutil
import requests
import random

from urllib.parse import urlparse, unquote
from dotenv import load_dotenv

VK_API_URL = "https://api.vk.com"
VK_API_VERSION = "5.131"


def get_comic(number):
    response = requests.get(
        url=f"https://xkcd.com/{number}/info.0.json",
    )
    response.raise_for_status()
    return response.json()


def check_vk_errors(response):
    response_data = response.json()
    if response_data.get("error"):
        raise requests.HTTPError()
    return response_data


def get_random_comic():
    response = requests.get(url="https://xkcd.com/info.0.json")
    response.raise_for_status()
    last_comic = int(response.json()["num"])
    return get_comic(random.randint(1, last_comic))


def download_picture(picture_url, folder="Files"):
    img_path = unquote(urlparse(picture_url).path)
    out_file_name = os.path.basename(img_path)

    response = requests.get(url=picture_url, stream=True)
    response.raise_for_status()

    with open(os.path.join(folder, out_file_name), "wb") as file:
        shutil.copyfileobj(response.raw, file)
    return out_file_name


def get_upload_url(access_token, group_id):
    response = requests.get(
        url=f"{VK_API_URL}/method/photos.getWallUploadServer",
        params={
            "access_token": access_token,
            "v": VK_API_VERSION,
            "group_id": group_id
        },
    )
    response.raise_for_status()
    return check_vk_errors(response)["response"]["upload_url"]


def upload_picture(file_name, upload_url, folder="Files"):
    file_path = os.path.join(folder, file_name)
    try:
        with open(file_path, "rb") as file:
            files = {"file1": file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
        return check_vk_errors(response)
    except requests.HTTPError:
        return None


def save_picture(server, _hash, photo, access_token, group_id):
    response = requests.post(
        url=f"{VK_API_URL}/method/photos.saveWallPhoto",
        params={
            "access_token": access_token,
            "v": VK_API_VERSION,
            "group_id": group_id
        },
        data={"server": server, "hash": _hash, "photo": photo},
    )
    response.raise_for_status()
    return check_vk_errors(response)["response"][0]


def publish_picture_on_wall(owner_id, _id, message, access_token, group_id):
    attachment = f"photo{owner_id}_{_id}"

    response = requests.post(
        url=f"{VK_API_URL}/method/wall.post",
        params={
            "access_token": access_token,
            "v": VK_API_VERSION,
        },
        data={
            "owner_id": "-" + group_id,
            "from_group": 1,
            "attachments": attachment,
            "message": message,
        },
    )
    response.raise_for_status()
    return check_vk_errors(response)


if __name__ == "__main__":
    load_dotenv()
    download_folder = "Files"

    VK_ACCESS_TOKEN = os.getenv("VK_ACCESS_TOKEN")
    VK_GROUP_ID = os.getenv("VK_GROUP_ID")

    comic_data = get_random_comic()
    comic_img = comic_data["img"]
    comic_title = comic_data["alt"]

    os.makedirs(download_folder, exist_ok=True)
    file_name = download_picture(comic_img, folder=download_folder)

    upload_url = get_upload_url(access_token=VK_ACCESS_TOKEN, group_id=VK_GROUP_ID)
    uploaded_data = upload_picture(file_name, upload_url)

    if not uploaded_data:
        os.remove(os.path.join(download_folder, file_name))
    else:
        saved_data = save_picture(
            server=uploaded_data["server"],
            _hash=uploaded_data["hash"],
            photo=uploaded_data["photo"],
            access_token=VK_ACCESS_TOKEN,
            group_id=VK_GROUP_ID
        )

        publish_picture_on_wall(
            owner_id=saved_data['owner_id'],
            _id=saved_data['id'],
            message=comic_title,
            access_token=VK_ACCESS_TOKEN,
            group_id=VK_GROUP_ID
        )
