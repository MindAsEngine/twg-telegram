from aiogram.filters.callback_data import CallbackData

from backend_api.models import TourTypeENUM


class TourTypeData(CallbackData, prefix='tt'):
    type: TourTypeENUM | None = None
    is_custom: bool = False


class TourPageData(CallbackData, prefix='tp'):
    page: int = 0
