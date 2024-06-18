import logging
from contextlib import asynccontextmanager

import uvicorn
from aiogram.types import Update
from fastapi import FastAPI
from fastapi import Request

from api import api_router
from bot.bot import bot, dp

from config import WEBHOOK_URL

logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(url=WEBHOOK_URL,
                          allowed_updates=dp.resolve_used_update_types(),
                          drop_pending_updates=True)
    yield
    await bot.delete_webhook(drop_pending_updates=True)


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)


app.include_router(api_router, prefix="/api")


def main():
    try:
        uvicorn.run(app, port=5000)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
