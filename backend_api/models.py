from enum import Enum

from pydantic import BaseModel, Field


class Tag(BaseModel):
    id: int
    name: str


class Country(BaseModel):
    id: int
    title: str
    media: str


class Hospital(BaseModel):
    id: int
    slug: str
    name: str
    city: str
    introduction: str
    description: str
    address: str
    header: str
    medias: list[str]


class StarsENUM(Enum):
    NULL = ''
    ONE = '⭐️'
    TWO = '⭐️⭐️'
    THREE = '⭐️⭐️⭐️'
    FOUR = '⭐️⭐️⭐️⭐️'
    FIVE = '⭐️⭐️⭐️⭐️⭐️'


class Resort(BaseModel):
    id: int
    name: str
    country: str


class Property(BaseModel):
    id: int
    name: str


class Hotel(BaseModel):
    id: int
    slug: str
    name: str
    city: str
    stars: StarsENUM
    introduction: str
    description: str
    header: str
    medias: list[str]
    properties: list[Property]
    resort: Resort


class TourTypeENUM(Enum):
    TOURISM = 'Туризм'
    MEDICAL = 'Медицинские туры'
    BUS_TOUR = 'Автобусные туры'


class Tour(BaseModel):
    id: int
    slug: str
    title: str
    type: TourTypeENUM
    introduction: str
    description: str
    additional: str
    country: Country
    header: str
    medias: list[str]
    tags: list[Tag]
    price: int


class Page[T](BaseModel):
    number: int
    size: int
    total_pages: int = Field(..., alias='totalPages')
    total_elements: int = Field(..., alias='totalElements')
    content: list[T]
