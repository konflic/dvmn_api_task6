import os
import shutil
import requests

from urllib.parse import urlparse
from dotenv import load_dotenv

API_VERSION = "5.131"

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")


def get_comic(number):
    response = requests.get(
        url=f"https://xkcd.com/{number}/info.0.json",
    )
    response.raise_for_status()
    return response.json()


def download_picture(picture_url):
    img_path = urlparse(picture_url).path
    out_file = os.path.basename(img_path)
    response = requests.get(url=picture_url, stream=True)
    response.raise_for_status()
    with open(f"Files/{out_file}", "wb") as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response


if __name__ == "__main__":
    img_name = get_comic(600)["img"]
    download_picture(img_name)
