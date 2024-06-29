from aiogram import Router

from bot.handlers.commands import router as commands_router
from bot.handlers.tours import router as tours_router

router = Router()

router.include_router(commands_router)
router.include_router(tours_router)

