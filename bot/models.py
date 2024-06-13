from pydantic import BaseModel


class TourFilters(BaseModel):
    country_ids: list[int] | None = None
    hotel_ids: list[int] | None = None
    resort_ids: list[int] | None = None
    tag_ids: list[int] | None = None
    tour_stars: list[str] | None = None
    hospital_ids: list[int] | None = None
    tour_types: list[str] | None = None


class UserState(BaseModel):
    username: str | None
    is_authorized: bool = False
    is_wait_phone: bool = False
    is_agent: bool = False
    access_token: str | None = None
    refresh_token: str | None = None

    filters: TourFilters | None = TourFilters()

    def clear_filters(self) -> None:
        self.filters = TourFilters()

    def clear_auth(self):
        self.access_token = None
        self.refresh_token = None
        self.is_authorized = False


