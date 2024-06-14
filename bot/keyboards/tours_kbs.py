import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend_api.models import Page, Tag
from bot.fsm.states import TourFilters
from bot.fsm.callbacks import TagData, ActionENUM


def get_tags_keyboard(tag_page: Page[Tag], filters: TourFilters) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for tag in tag_page.content:
        is_selected = tag in filters.tag_ids
        action = ActionENUM.ADD if not is_selected else ActionENUM.REMOVE
        text = f'{tag.name}{' (Убрать)' if is_selected else ''}'
        builder.button(text=text,
                       callback_data=TagData(
                           id=tag.id,
                           page=tag_page.number,
                           action=action
                       ))
    nav_row_len = 1
    if tag_page.number != 0:
        nav_row_len += 1
        builder.button(text='⬅️ Назад', callback_data=TagData(page=max(tag_page.number - 1, 0)))
    builder.button(text=f'{tag_page.number + 1}/{tag_page.total_pages}', callback_data='none')
    if tag_page.number != tag_page.total_pages - 1:
        nav_row_len += 1
        builder.button(text='Далее ➡️', callback_data=TagData(page=min(tag_page.number + 1, 0)))

    builder.button(text='✅ Применить ✅', callback_data=TagData(action=ActionENUM.ACCEPT))
    builder.button(text='🤷‍ Не важно 🤷', callback_data=TagData(action=ActionENUM.REJECT))
    builder.button(text='🔄 В начало 🔄', callback_data='start')
    builder.adjust(*([1]*len(tag_page.content)), nav_row_len, 1, 1, 1)
    return builder.as_markup()
