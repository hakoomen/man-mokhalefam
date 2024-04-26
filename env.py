from dotenv import load_dotenv
import json
import os

load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", None)
ALLOWED_CHANNEL_IDS: list[str] = json.loads(os.environ.get("ALLOWED_CHANNEL_IDS", "[]"))
DATABASE_URL = os.environ.get("DATABASE_URL", None)

if TELEGRAM_TOKEN is None or DATABASE_URL is None or len(ALLOWED_CHANNEL_IDS) == 0:
    raise Exception("required env variables not set")
