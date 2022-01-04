import os
from dotenv import load_dotenv

API_VERSION = "5.131"

load_dotenv()

client_id = os.getenv("CLIENT_ID")
access_token = os.getenv("ACCESS_TOKEN")
