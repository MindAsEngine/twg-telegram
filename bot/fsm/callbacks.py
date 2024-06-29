from enum import Enum

from aiogram.filters.callback_data import CallbackData

from backend_api.models import TourTypeENUM


class TourTypeData(CallbackData, prefix='tt'):
    type: TourTypeENUM | None = None
    is_custom: bool = False


class TagActionENUM(Enum):
    ADD = 'Add'
    REMOVE = 'Remove'
    ACCEPT = 'Accept'
    REJECT = 'Reject'
    PAGE = 'Page'


class TagData(CallbackData, prefix='tag'):
    id: int | None = None
    page: int | None = None
    action: TagActionENUM | None = None


class TourActionENUM(Enum):
    ADD = 'Add'
    REMOVE = 'Remove'
    ACCEPT = 'Accept'
    PAGE = 'Page'
    DETAILS = 'Details'
    PHOTOS = 'Photos'
    RESET = 'Reset'


class TourData(CallbackData, prefix='tour'):
    id: int | None = None
    page: int | None = None
    action: TourActionENUM | None = None
