from pydantic import BaseModel, Field


class TourFilters(BaseModel):
    country_ids: list[int] | None = Field(None, alias="countryIds")
    hotel_ids: list[int] | None = Field(None, alias="hotelIds")
    resort_ids: list[int] | None = Field(None, alias="resortIds")
    tag_ids: list[int] | None = Field(None, alias="tagIds")
    tour_stars: list[str] | None = Field(None, alias="stars")
    hospital_ids: list[int] | None = Field(None, alias="hospitalIds")
    tour_types: list[str] | None = Field(None, alias="tourTypes")


class UserState(BaseModel):
    is_linked: bool = Field(False, alias="is_linked")
    is_authorized: bool = Field(False, alias="is_authorized")
    is_wait_phone: bool = Field(False, alias="is_wait_phone")
    is_agent: bool = Field(False, alias="is_agent")
    access_token: str | None = Field(None, alias="access_token")
    refresh_token: str | None = Field(None, alias="refresh_token")

    filters: TourFilters | None = TourFilters()

    def clear_filters(self) -> None:
        self.filters = TourFilters()

    def clear_auth(self):
        self.access_token = None
        self.refresh_token = None
        self.is_authorized = False


