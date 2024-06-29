import asyncio
import logging

from backend_api.utils import get_client
from backend_api.models import Tag, Page, Tour
from backend_api.exceptions import BackendError, NotFoundError
from bot.fsm.states import TourFilters, UserState


async def get_tags(page: int = 0,
                   local: str = 'RU') -> Page[Tag]:
    client = await get_client()

    response = await client.get(
        f'/travel/{local}/tags',
        params={
            'page': page,
            'size': 5
        }
    )

    if response.status_code == 404:
        logging.log(logging.ERROR, response.json())
        raise NotFoundError(f'Tags with local {local} for page {page} not found')

    if response.status_code != 200:
        logging.log(logging.ERROR, response.json())
        raise BackendError('Something went wrong')

    return Page[Tag].parse_obj(response.json())


async def get_tours(page: int = 0,
                    user: UserState = UserState()) -> Page[Tour]:
    client = await get_client()
    filters = user.filters

    params = {
        'page': page,
        'size': 1
    }
    if filters.country_ids is not None:
        params['countryIds'] = filters.country_ids
    if filters.tag_ids is not None:
        params['tagIds'] = filters.tag_ids
    if filters.hospital_ids is not None:
        params['hospitalIds'] = filters.hospital_ids
    if filters.tour_type is not None:
        params['types'] = [filters.tour_type]
    if filters.tour_stars is not None:
        params['stars'] = filters.tour_stars
    if filters.resort_ids is not None:
        params['resortIds'] = filters.resort_ids
    if filters.hotel_ids is not None:
        params['hotelsIds'] = filters.hotel_ids

    response = await client.get(
        f'/travel/{user.local}/tours/find/filters',
        params=params
    )

    if response.status_code == 404:
        logging.log(logging.ERROR, response.json())
        raise NotFoundError(f'Tours with local {user.local} for page {page} not found')

    if response.status_code != 200:
        logging.log(logging.ERROR, response.json())
        raise BackendError('Something went wrong')

    return Page[Tour].parse_obj(response.json())
