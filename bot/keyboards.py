import logging

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.models import UserState
from config import WEBSITE_URL


def get_start_keyboard(user: UserState) -> InlineKeyboardMarkup:
    logging.log(logging.INFO, 'Keyboard start')
    builder = InlineKeyboardBuilder()

    if not user.username:
        builder.button(text='☎️ Привязать аккаунт ☎️', url=WEBSITE_URL)
    elif not user.is_authorized:
        builder.button(text='🔑 Войти 🔑', url=WEBSITE_URL)

    builder.button(text='🏝️ Туризм 🏝️', callback_data='tourism')
    builder.button(text='🏥 Медицина 🏥', callback_data='medicine')
    builder.button(text='🚌 Автобусные туры 🚌', callback_data='bus_tours')
    builder.button(text='🗺️ Авторские туры 🗺️', callback_data='custom_tours')
    if user.is_agent:
        builder.button(text='👨‍💼 Управление заявками 👨‍💼', callback_data='requests')

    builder.adjust(1)
    return builder.as_markup()
