from aiogram import Router
from aiogram.filters import CommandObject, CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types.input_file import FSInputFile

from backend_api.auth import link_account, auth_user, validate_token
from backend_api.exceptions import AuthError, LinkError
from backend_api.handlers.tags import get_tags
from utils import render_template
from bot.fsm.states import get_state_data, set_state_data
from bot.keyboards.command_kbs import get_start_keyboard

router = Router()


@router.message(Command('test'))
async def test():
    await get_tags()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext, command: CommandObject) -> None:
    user_state = await get_state_data(state)

    is_linked = None
    if command.args is not None:
        link_uuid = command.args
        tg_id = message.chat.id
        try:
            user_state = await link_account(user_state, tg_id, link_uuid)
            is_linked = True
            user_state = await auth_user(user_state, tg_id)
        except LinkError:
            is_linked = False
        except AuthError:
            user_state.is_authorized = False

    try:
        if user_state.is_linked:
            if user_state.is_authorized:
                user_state = await validate_token(user_state)
            else:
                user_state = await auth_user(user_state, message.from_user.id)
    except AuthError:
        user_state.clear_auth()

    await set_state_data(state, user_state)

    text = await render_template('start.html',
                                 user=user_state)
    await message.answer_photo(
        caption=text,
        photo=FSInputFile('media/kiprstart.jpg'),
        reply_markup=get_start_keyboard(user_state)
    )
    if is_linked is not None:
        await message.answer(f'Телеграм аккаунт {"успешно" if is_linked else "не"} привязан')

