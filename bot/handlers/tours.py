import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from backend_api.handlers.tags import get_tags
from bot.fsm.callbacks import TourTypeData
from bot.fsm.states import get_state_data, set_state_data
from bot.keyboards.tours_kbs import get_tags_keyboard
from config import CUSTOM_TAG_ID
from utils import render_template

router = Router()


@router.callback_query(TourTypeData.filter())
async def handle_tour_types(callback: CallbackQuery,
                            callback_data: TourTypeData,
                            state: FSMContext) -> None:
    user = await get_state_data(state)
    if callback_data.is_custom:
        if CUSTOM_TAG_ID not in user.filters.tag_ids:
            user.filters.tag_ids.append(CUSTOM_TAG_ID)
    else:
        if CUSTOM_TAG_ID in user.filters.tag_ids:
            user.filters.tag_ids.remove(CUSTOM_TAG_ID)

    if callback_data.type is not None:
        user.filters.tour_type = callback_data.type.name
    else:
        user.filters.tour_type = None

    tags_page = await get_tags(0, user.local)
    selected_tags = [tag for tag in tags_page.content if tag.id in user.filters.tag_ids]
    text = await render_template('tags.html', tags=selected_tags)
    await callback.message.edit_caption(
        caption=text,
        reply_markup=get_tags_keyboard(tags_page, user.filters)
    )
    await set_state_data(state, user)
    await callback.answer()
