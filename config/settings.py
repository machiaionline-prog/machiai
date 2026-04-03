import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = OPENAI_KEY
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
PAGE_TOKEN = os.getenv("PAGE_TOKEN") or INSTAGRAM_TOKEN
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
MONGO_URL = os.getenv("MONGO_URL")
