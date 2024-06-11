from aiogram import Router

from bot.handlers.commands import router as commands_router

router = Router()

router.include_router(commands_router)