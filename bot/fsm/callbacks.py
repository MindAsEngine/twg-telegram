from enum import Enum

from aiogram.filters.callback_data import CallbackData

from backend_api.models import TourTypeENUM


class TourTypeData(CallbackData, prefix='tt'):
    type: TourTypeENUM | None = None
    is_custom: bool = False


class TourPageData(CallbackData, prefix='tp'):
    page: int = 0


class ActionENUM(Enum):
    ADD = 'Add'
    REMOVE = 'Remove'
    ACCEPT = 'Accept'
    REJECT = 'Reject'


class TagData(CallbackData, prefix='tag'):
    id: int | None = None
    page: int | None = None
    action: ActionENUM | None = None
