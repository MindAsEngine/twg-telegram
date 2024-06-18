import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from backend_api.handlers.travel import get_tags, get_tours
from bot.fsm.callbacks import TourTypeData, TagData, TagActionENUM
from bot.fsm.states import get_state_data, set_state_data, UserState
from bot.keyboards.tours_kbs import get_tags_keyboard, get_tour_keyboard
from config import CUSTOM_TAG_ID
from utils import render_template

router = Router()


async def answer_tags(callback: CallbackQuery,
                      user: UserState,
                      page_number: int):
    tags_page = await get_tags(page_number, user.local)
    selected_tags = [tag for tag in tags_page.content if tag.id in user.filters.tag_ids]
    text = await render_template('tags.html', tags=selected_tags)
    keyboard = get_tags_keyboard(tags_page, user.filters)
    if text == callback.message.text:
        try:
            await callback.message.edit_reply_markup(
                reply_markup=keyboard
            )
        finally:
            pass
    else:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard
        )
    await callback.answer()


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

    await set_state_data(state, user)

    await answer_tags(callback, user, 0)


@router.callback_query(TagData.filter(),
                       F.data.func(lambda data: TagData.unpack(data))
                       .action.in_({TagActionENUM.ADD, TagActionENUM.REMOVE, TagActionENUM.PAGE}))
async def handle_tags(callback: CallbackQuery,
                      callback_data: TagData,
                      state: FSMContext) -> None:
    user = await get_state_data(state)
    if callback_data.action is not None:
        if callback_data.action == TagActionENUM.ADD:
            user.filters.tag_ids.append(callback_data.id)
        if callback_data.action == TagActionENUM.REMOVE:
            user.filters.tag_ids.remove(callback_data.id)
    await set_state_data(state, user)

    await answer_tags(callback, user, callback_data.page)


async def answer_tours(callback: CallbackQuery,
                       user: UserState,
                       page_number: int):
    tour_page = await get_tours(page_number, user)

    text = await render_template('tour.html', tour=tour_page.content[0])
    keyboard = get_tour_keyboard(tour_page)
    if text == callback.message.text:
        await callback.message.edit_reply_markup(
            reply_markup=keyboard
        )
    else:
        await callback.message.edit_caption(
            caption=text,
            reply_markup=keyboard
        )
    await callback.answer()
