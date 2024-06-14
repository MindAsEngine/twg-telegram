import logging

from aiogram.types import InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.models import UserState
from bot.fsm.states import UserState
from bot.fsm.callbacks import TourTypeData, TourTypeENUM
from config import WEBSITE_URL


def get_start_keyboard(user: UserState) -> InlineKeyboardMarkup:
    logging.log(logging.INFO, 'Keyboard start')
    builder = InlineKeyboardBuilder()

    if not user.is_linked:
        builder.button(text='☎️ Привязать аккаунт ☎️', web_app=WebAppInfo(url=WEBSITE_URL))
    elif not user.is_authorized:
        builder.button(text='🔑 Войти 🔑', web_app=WebAppInfo(url=WEBSITE_URL))

    builder.button(text='🏝️ Туризм 🏝️', callback_data='tourism')
    builder.button(text='🏥 Медицина 🏥', callback_data='medicine')
    builder.button(text='🚌 Автобусные туры 🚌', callback_data='bus_tours')
    builder.button(text='🗺️ Авторские туры 🗺️', callback_data='custom_tours')

    builder.adjust(1)
    return builder.as_markup()
