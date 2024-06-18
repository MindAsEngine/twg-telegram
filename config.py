import os

from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND_URL')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBSITE_URL = os.getenv('WEBSITE_URL')

CUSTOM_TAG_ID = int(os.getenv('CUSTOM_TAG_ID'))

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

