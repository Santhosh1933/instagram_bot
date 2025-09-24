import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")
BUSINESS_ACCOUNT_ID = os.getenv("BUSINESS_ACCOUNT_ID")
APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")