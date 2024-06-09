import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from utils import render_template

router = Router()


@router.message(Command('start'))
async def start_command(message: Message) -> None:

    logging.log(logging.INFO, message.text)
    await message.answer(await render_template('start.html', user=message.from_user.first_name))

