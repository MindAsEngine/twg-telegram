from enum import Enum

from pydantic import BaseModel


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
    properties: list[str]
    resort: str


class TourTypeENUM(Enum):
    TOURISM = 'Туризм'
    MEDICAL = 'Медицинские туры'
    BUS_TOUR = 'Автобусные туры'


class Tour(BaseModel):
    id: int
    slug: str
    title: str
    type: str
    introduction: str
    description: str
    additional: str
    country: str
    header: str
    medias: list[str]
    tags: list[str]
    price: int

