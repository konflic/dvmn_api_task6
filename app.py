import os
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
    response = response.json()
    if response.get("error"):
        raise requests.HTTPError(response.get("error").get("error_msg", "No error message"))
    return response


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

    with open(os.path.join(folder, out_file_name), "wb+") as file:
        file.write(response.content)
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
    with open(file_path, "rb") as file:
        files = {"file1": file}
        response = requests.post(upload_url, files=files)
    response.raise_for_status()
    return check_vk_errors(response)


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


def publish_picture_on_wall(owner_id, attachment_id, message, access_token, group_id):
    attachment = f"photo{owner_id}_{attachment_id}"

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

    vk_access_token = os.getenv("VK_ACCESS_TOKEN")
    vk_group_id = os.getenv("VK_GROUP_ID")

    comic = get_random_comic()
    comic_img = comic["img"]
    comic_title = comic["alt"]

    os.makedirs(download_folder, exist_ok=True)
    file_name = download_picture(comic_img, folder=download_folder)

    try:
        upload_url = get_upload_url(access_token=vk_access_token, group_id=vk_group_id)
        uploaded = upload_picture(file_name, upload_url)
    finally:
        os.remove(os.path.join(download_folder, file_name))

    saved = save_picture(
        server=uploaded["server"],
        _hash=uploaded["hash"],
        photo=uploaded["photo"],
        access_token=vk_access_token,
        group_id=vk_group_id
    )

    publish_picture_on_wall(
        owner_id=saved["owner_id"],
        attachment_id=saved["id"],
        message=comic_title,
        access_token=vk_access_token,
        group_id=vk_group_id
    )
