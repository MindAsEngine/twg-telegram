from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from pydantic import BaseModel, Field

from backend_api.models import StarsENUM, TourTypeENUM


class TourFilters(BaseModel):
    country_ids: list[int] | None = Field(default_factory=list, alias="countryIds")
    hotel_ids: list[int] | None = Field(default_factory=list, alias="hotelIds")
    resort_ids: list[int] | None = Field(default_factory=list, alias="resortIds")
    tag_ids: list[int] | None = Field(default_factory=list, alias="tagIds")
    tour_stars: list[str] | None = Field(default_factory=list, alias="stars")
    hospital_ids: list[int] | None = Field(default_factory=list, alias="hospitalIds")
    tour_type: str | None = Field(None, alias="tourTypes")
    

class UserState(BaseModel):
    is_linked: bool = Field(False, alias="is_linked")
    is_authorized: bool = Field(False, alias="is_authorized")
    is_agent: bool = Field(False, alias="is_agent")
    access_token: str | None = Field(None, alias="access_token")
    refresh_token: str | None = Field(None, alias="refresh_token")

    filters: TourFilters | None = TourFilters()
    local: str = Field('RU', alias="local")

    def clear_filters(self) -> None:
        """
        Clear all filters in state
        :return:
        """
        self.filters = TourFilters()

    def clear_auth(self):
        """
        Clear all auth data in state
        :return:
        """
        self.access_token = None
        self.refresh_token = None
        self.is_authorized = False


async def get_state_data(state: FSMContext) -> UserState:
    """
    Get state data from state and transform them to UserState class
    :param state: FSMContext instance
    :return: UserState instance
    """
    data = await state.get_data()
    if data is None:
        await set_state_data(state, UserState())
    return UserState.parse_obj(await state.get_data())


async def set_state_data(state: FSMContext, data: UserState) -> None:
    """
    Get state data as UserState class, transform and put them to state
    :param state: FSMContext instance
    :param data: UserState instance
    :return:
    """
    await state.set_data(data.model_dump())

