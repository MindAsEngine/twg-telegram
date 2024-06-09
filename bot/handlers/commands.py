import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from backend_api.auth import link_account
from utils import render_template
from bot.models import UserState
from bot.keyboards import get_start_keyboard

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext) -> None:
    if (await state.get_data()) is None:
        await state.set_state(UserState().to_dict())
    user_state = UserState(**(await state.get_data()))

    is_linked = False
    if len(message.text.split()) == 2:
        username = message.text.split()[1]
        tg_id = message.chat.id
        await link_account(username, tg_id)
        user_state.is_authorized = True
        # user_state.id = id
        is_linked = True

    text = await render_template('start.html',
                                 **user_state.to_dict())
    await message.answer_photo(
        caption=text,
        photo=FSInputFile('media/kiprstart.jpg'),
        reply_markup=get_start_keyboard(user_state.is_authorized)
    )
    if is_linked:
        await message.answer('Телеграм аккаунт успешно привязан')

