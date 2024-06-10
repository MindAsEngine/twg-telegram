import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from backend_api.auth import link_account, auth_user, validate_token
from backend_api.exceptions import AuthError, LinkError
from utils import render_template
from bot.models import UserState
from bot.keyboards import get_start_keyboard

router = Router()


@router.message(Command('start'))
async def start_command(message: Message, state: FSMContext) -> None:
    if (await state.get_data()) is None:
        await state.set_state(UserState().to_dict())
    user_state = UserState(**(await state.get_data()))

    is_linked = None
    if len(message.text.split()) == 2:
        username = user_state.username
        user_state.username = message.text.split()[1]
        tg_id = message.chat.id
        try:
            user_state = await link_account(user_state, tg_id)
            is_linked = True
            user_state = await auth_user(user_state, tg_id)
        except LinkError:
            is_linked = False
            user_state.username = username
        except AuthError:
            user_state.is_authorized = False

    try:
        if user_state.is_authorized:
            user_state = await validate_token(user_state)
    except AuthError:
        user_state.clear()

    await state.set_data(user_state.to_dict())

    text = await render_template('start.html',
                                 user=user_state)
    await message.answer_photo(
        caption=text,
        photo=FSInputFile('media/kiprstart.jpg'),
        reply_markup=get_start_keyboard(user_state)
    )
    if is_linked is not None:
        await message.answer(f'Телеграм аккаунт {"успешно" if is_linked else "не"} привязан')

