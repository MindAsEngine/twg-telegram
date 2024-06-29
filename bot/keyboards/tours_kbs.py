import logging

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from backend_api.models import Page, Tag, Tour
from bot.fsm.states import TourFilters
from bot.fsm.callbacks import TagData, TagActionENUM, TourData, TourActionENUM


def get_tags_keyboard(tag_page: Page[Tag], filters: TourFilters) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for tag in tag_page.content:
        is_selected = tag.id in filters.tag_ids
        action = TagActionENUM.ADD if not is_selected else TagActionENUM.REMOVE
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
        builder.button(text='⬅️ Назад', callback_data=TagData(action=TagActionENUM.PAGE,
                                                              page=max(tag_page.number - 1, 0)))
    builder.button(text=f'{tag_page.number + 1}/{tag_page.total_pages}', callback_data='none')
    if tag_page.number != tag_page.total_pages - 1:
        nav_row_len += 1
        builder.button(text='Далее ➡️', callback_data=TagData(action=TagActionENUM.PAGE,
                                                              page=min(tag_page.number + 1, 0)))

    builder.button(text='✅ Применить ✅', callback_data=TagData(action=TagActionENUM.ACCEPT))
    builder.button(text='🤷‍ Не важно 🤷', callback_data=TagData(action=TagActionENUM.REJECT))
    builder.button(text='🔄 В начало 🔄', callback_data='start')
    builder.adjust(*([1] * len(tag_page.content)), nav_row_len, 1, 1, 1)
    return builder.as_markup()


def get_tour_keyboard(tag_page: Page[Tour]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    tour = tag_page.content[0]
    builder.button(text='📝 Подробнее', callback_data=TourData(id=tour.id,
                                                              action=TourActionENUM.DETAILS))
    builder.button(text='🖼️ Фотографии', callback_data=TourData(id=tour.id,
                                                                action=TourActionENUM.PHOTOS))

    nav_row_len = 1
    if tag_page.number != 0:
        nav_row_len += 1
        builder.button(text='⬅️ Назад', callback_data=TourData(action=TourActionENUM.PAGE,
                                                               page=max(tag_page.number - 1, 0)))
    builder.button(text=f'{tag_page.number + 1}/{tag_page.total_pages}', callback_data='none')
    if tag_page.number != tag_page.total_pages - 1:
        nav_row_len += 1
        builder.button(text='Далее ➡️', callback_data=TourData(action=TourActionENUM.PAGE,
                                                               page=min(tag_page.number + 1, 0)))

    builder.button(text='🗑️ Сбросить фильтры 🗑️', callback_data=TourData(action=TourActionENUM.RESET))
    builder.button(text='✅ Выбрать ✅', callback_data=TourData(id=tour.id,
                                                              action=TourActionENUM.ACCEPT))
    builder.button(text='🔄 В начало 🔄', callback_data='start')
    builder.adjust(2, nav_row_len, 1, 1, 1)
    return builder.as_markup()
