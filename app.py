import os
import shutil
import requests
import random

from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv

API_URL = "https://api.vk.com"
API_VERSION = "5.131"

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
GROUP_ID = os.getenv("GROUP_ID")


def get_comic(number):
    response = requests.get(
        url=f"https://xkcd.com/{number}/info.0.json",
    )
    response.raise_for_status()
    return response.json()


def get_random_comic():
    response = requests.get(
        url="https://xkcd.com/info.0.json"
    )
    response.raise_for_status()
    last_comic = int(response.json()["num"])
    return get_comic(random.randint(1, last_comic))


def download_picture(picture_url):
    img_path = urlparse(picture_url).path
    out_file_name = os.path.basename(img_path)

    response = requests.get(url=picture_url, stream=True)
    response.raise_for_status()

    with open(f"Files/{out_file_name}", "wb") as file:
        shutil.copyfileobj(response.raw, file)
    return out_file_name


def get_upload_url():
    response = requests.get(
        url=f"{API_URL}/method/photos.getWallUploadServer",
        params={
            "access_token": ACCESS_TOKEN,
             "v": API_VERSION,
             "group_id": GROUP_ID
         },
    )
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_picture(file_name, upload_url):
    file_path = f"Files/{file_name}"
    with open(file_path, "rb") as file:
        files = {"file1": file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    os.remove(file_path)
    return response.json()


def save_picture(upload_data):
    response = requests.post(
        url=f"{API_URL}/method/photos.saveWallPhoto",
        params={
            "access_token": ACCESS_TOKEN, 
            "v": API_VERSION,
            "group_id": GROUP_ID
        },
        data={
            "server": upload_data["server"],
            "hash": upload_data["hash"],
            "photo": upload_data["photo"],
        },
    )
    response.raise_for_status()
    return response.json()["response"][0]


def publish_picture_on_wall(save_data, message):
    attachment = f"photo{save_data['owner_id']}_{save_data['id']}"
    response = requests.post(
        url=f"{API_URL}/method/wall.post",
        params={
            "access_token": ACCESS_TOKEN,
            "v": API_VERSION,
        },
        data={
            "owner_id": "-" + GROUP_ID,
            "from_group": 1,
            "attachments": attachment,
            "message": message,
        },
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    comic_data = get_random_comic()
    comic_img = comic_data["img"]
    comic_title = comic_data["alt"]

    file_name = download_picture(comic_img)
    upload_url = get_upload_url()

    upload_data = upload_picture(file_name, upload_url)
    save_data = save_picture(upload_data)

    publish_picture_on_wall(save_data, message=comic_title)
