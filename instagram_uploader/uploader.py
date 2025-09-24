import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
BUSINESS_ACCOUNT_ID = os.getenv("BUSINESS_ACCOUNT_ID")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

class InstagramUploader:
    def __init__(self, access_token: str = ACCESS_TOKEN, business_account_id: str = BUSINESS_ACCOUNT_ID):
        self.access_token = access_token
        self.business_account_id = business_account_id

    def refresh_access_token(self):
        url = f"https://graph.instagram.com/refresh_access_token"
        params = {
            "grant_type": "ig_refresh_token",
            "access_token": self.access_token
        }

        response = requests.get(url, params=params)
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from Instagram: {response.text}")

        if 'access_token' in data:
            self.access_token = data['access_token']
            print(f"[DEBUG] Access token refreshed successfully!")
        else:
            # Print full response for debugging
            raise Exception(f"Failed to refresh access token. Response: {json.dumps(data, indent=2)}")

    def create_media(self, image_url: str, caption: str):
        url = f"https://graph.instagram.com/v13.0/{self.business_account_id}/media"
        params = {
            "image_url": image_url,
            "caption": caption,
            "access_token": self.access_token
        }

        response = requests.post(url, params=params)
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from Instagram: {response.text}")

        if 'error' in data and data['error']['code'] == 190:  # Token expired or invalid
            self.refresh_access_token()
            return self.create_media(image_url, caption)

        if 'id' in data:
            print(f"[DEBUG] Media created with ID: {data['id']}")
            return data['id']
        else:
            # Print full response for debugging
            raise Exception(f"Failed to create media. Response: {json.dumps(data, indent=2)}")

    def publish_media(self, media_id: str):
        publish_url = f"https://graph.instagram.com/v13.0/{self.business_account_id}/media_publish"
        publish_params = {
            "creation_id": media_id,
            "access_token": self.access_token
        }

        response = requests.post(publish_url, params=publish_params)
        try:
            data = response.json()
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON response from Instagram: {response.text}")

        if 'error' in data and data['error']['code'] == 190:  # Token expired or invalid
            self.refresh_access_token()
            return self.publish_media(media_id)

        if 'id' in data:
            print(f"[DEBUG] Media published successfully with ID: {data['id']}")
            return True
        else:
            # Print full response for debugging
            raise Exception(f"Failed to publish media. Response: {json.dumps(data, indent=2)}")

    def upload_image(self, image_url: str, caption: str):
        media_id = self.create_media(image_url, caption)
        return self.publish_media(media_id)