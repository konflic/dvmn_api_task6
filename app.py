import os
import shutil
import requests

from urllib.parse import urlparse, urljoin
from dotenv import load_dotenv

API_URL = "https://api.vk.com"
API_VERSION = "5.131"

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")


def get_comic(number):
    response = requests.get(
        url=f"https://xkcd.com/{number}/info.0.json",
    )
    response.raise_for_status()
    return response.json()


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
        params={"access_token": ACCESS_TOKEN, "v": API_VERSION},
    )
    response.raise_for_status()
    return response.json()["response"]["upload_url"]


def upload_picture(file_name):
    upload_url = get_upload_url()
    with open(f"Files/{file_name}", "rb") as file:
        files = {"file1": file}
        response = requests.post(upload_url, files=files)
        response.raise_for_status()
    return response.json()


def save_picture(upload_data):
    response = requests.post(
        url=f"{API_URL}/method/photos.saveWallPhoto",
        params={"access_token": ACCESS_TOKEN, "v": API_VERSION},
        data={
            "server": upload_data["server"],
            "hash": upload_data["hash"],
            "photo": upload_data["photo"],
        },
    )
    response.raise_for_status()
    return response.json()


def publish_picture_on_wall(save_data):
    response = requests.post(
        url=f"{API_URL}/method/wall.post",
        params={
            "access_token": ACCESS_TOKEN,
            "v": API_VERSION,
        },
    )
    response.raise_for_status()


if __name__ == "__main__":
    comic_data = get_comic(600)
    comic_img = comic_data["img"]
    comic_title = comic_data["alt"]

    file_name = download_picture(comic_img)
    upload_data = upload_picture(file_name)
    save_data = save_picture(upload_data)

    print(save_data)
