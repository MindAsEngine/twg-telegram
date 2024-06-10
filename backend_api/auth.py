import logging

from backend_api.exceptions import AuthError, LinkError
from backend_api.utils import get_client
from bot.models import UserState


async def link_account(user: UserState, tg_id: int) -> UserState:
    client = await get_client(user.access_token)

    response = await client.post(
        '/profile/telegram/connect/set_id',
        json={
            'username': user.username,
            'telegramId': str(tg_id)
        }
    )
    if response.status_code != 200:
        raise LinkError('Account link request failed')

    return user


async def auth_user(user: UserState, tg_id: int) -> UserState:
    client = await get_client(user.access_token)

    response = await client.get(
        '/auth/users/bot-auth',
        params={'tgId': str(tg_id)}
    )
    if response.status_code != 200:
        raise AuthError(f'No valid token for user with tg id: {tg_id}')

    user.refresh_token = response.json()['refreshToken']
    user.access_token = response.json()['token']
    user.is_authorized = True

    user = await check_for_agent(user)

    return user


async def check_for_agent(user: UserState) -> UserState:
    client = await get_client(user.access_token)

    response = await client.get('/profile/me')
    if response.status_code == 200:
        if response.json()['role'] != 'USER':
            user.is_agent = True

    return user


async def _refresh_token(user: UserState) -> UserState:
    client = await get_client(user.access_token)
    response = await client.post(
        '/auth/users/refresh-token',
        json={'refreshToken': user.refresh_token}
    )
    if response.status_code != 200:
        raise AuthError(f'Refresh token not valid')

    user.access_token = response.json()['token']
    return user


async def validate_token(user: UserState) -> UserState:
    client = await get_client(user.access_token)
    response = await client.get('/profile/me')
    if response.status_code != 200:
        user = await _refresh_token(user)
    return user
