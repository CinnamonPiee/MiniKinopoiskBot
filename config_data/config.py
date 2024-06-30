import os
from dotenv import load_dotenv, find_dotenv


if not find_dotenv():
    exit("Environment variables are not loaded because the file is missing .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_DEV_TOKEN = os.getenv("KINOPOISK_DEV_TOKEN")
