import logging

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.fsm.states import UserState
from bot.fsm.callbacks import TourTypeData, TourTypeENUM
from config import WEBSITE_URL


def get_start_keyboard(user: UserState) -> InlineKeyboardMarkup:
    logging.log(logging.INFO, 'Keyboard start')
    builder = InlineKeyboardBuilder()

    if not user.is_linked:
        builder.button(text='☎️ Привязать аккаунт ☎️', url=WEBSITE_URL)
    elif not user.is_authorized:
        builder.button(text='🔑 Войти 🔑', url=WEBSITE_URL)

    builder.button(text='🏝️ Туризм 🏝️', callback_data=TourTypeData(type=TourTypeENUM.TOURISM))
    builder.button(text='🏥 Медицина 🏥', callback_data=TourTypeData(type=TourTypeENUM.MEDICAL))
    builder.button(text='🚌 Автобусные туры 🚌', callback_data=TourTypeData(type=TourTypeENUM.BUS_TOUR))
    builder.button(text='🗺️ Авторские туры 🗺️', callback_data=TourTypeData(is_custom=True))

    builder.adjust(1)
    return builder.as_markup()
