import os

from dotenv import load_dotenv

load_dotenv('.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')
BACKEND_URL = os.getenv('BACKEND.URL')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')
WEBSITE_URL = os.getenv('WEBSITE_URL')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')

