import asyncio

from httpx import AsyncClient

import env_config as config


async def get_client(access_token: str | None = None) -> AsyncClient:
    headers = {'Content-Type': 'application/json'}
    if access_token is not None:
        headers["Authorization"] = f"Bearer {access_token}"
    return AsyncClient(
        base_url=config.BACKEND_URL,
        headers=headers
    )
