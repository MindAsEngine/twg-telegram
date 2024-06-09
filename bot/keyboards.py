import logging

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from env_config import WEBSITE_URL


def get_start_keyboard(is_authorized: bool = False, **_) -> InlineKeyboardMarkup:
    logging.log(logging.INFO, 'Keyboard start')
    builder = InlineKeyboardBuilder()

    if not is_authorized:
        builder.button(text='☎️ Привязать аккаунт ☎️', url=WEBSITE_URL)

    builder.button(text='🏝️ Туризм 🏝️', callback_data='tourism')
    builder.button(text='🏥 Медицина 🏥', callback_data='medicine')
    builder.button(text='🚌 Автобусные туры 🚌', callback_data='bus_tours')
    builder.button(text='🗺️ Авторские туры 🗺️', callback_data='custom_tours')

    builder.adjust(1)
    return builder.as_markup()
