import os
import requests

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

if __name__ == "__main__":
    print(get_comic(614))
