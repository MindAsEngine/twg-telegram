import asyncio
import logging

from backend_api.utils import get_client
from backend_api.models import Tag, Page
from backend_api.exceptions import BackendError, NotFoundError


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
