from aiogram import Router

from bot.handlers.commands import router as commands_router

bot_router = Router()

bot_router.include_router(commands_router)
