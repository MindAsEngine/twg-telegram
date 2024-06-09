import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi import Request

from api import api_router
from bot import bot_router

import env_config as config
from bot.utils import storage

bot = Bot(token=config.BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage, bot=bot)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=config.WEBHOOK_URL,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


app.include_router(api_router, prefix="/api")
dp.include_router(bot_router)


def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
        filename='logs.log',
        filemode='a'
    )

    try:
        uvicorn.run(app, port=5000)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
