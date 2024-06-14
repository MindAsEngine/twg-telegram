from backend_api.exceptions import AuthError, LinkError
from backend_api.utils import get_client
from bot.fsm.states import UserState


async def link_account(user: UserState, tg_id: int, link_uuid: str) -> UserState:
    """
    Link telegram account with backend account of user by telegram id and uuid of link request
    :param user: UserState - state of user
    :param tg_id: int - telegram id of user
    :param link_uuid: str - string with uuid of link request
    :return:
    """
    client = await get_client()

    response = await client.post(
        '/profile/telegram/connect/set_id',
        json={
            'uuid': link_uuid,
            'telegramId': str(tg_id)
        }
    )
    if response.status_code != 200:
        raise LinkError('Account link request failed')
    user.is_linked = True
    return user


async def auth_user(user: UserState, tg_id: int) -> UserState:
    """
    Get refresh token from backend, and fill user state fields
    :param user: UserState - state of user
    :param tg_id: int - telegram id of user
    :return:
    """
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
    """
    Send request to backend to check agent status of user
    :param user: UserState - state of user
    :return:
    """
    client = await get_client(user.access_token)

    response = await client.get('/profile/me')
    if response.status_code == 200:
        if response.json()['role'] != 'USER':
            user.is_agent = True

    return user


async def _refresh_token(user: UserState) -> UserState:
    """
    Get new access token from backend by refresh token from state
    :param user: UserState - state of user
    :return:
    """
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
    """
    Check access token for efficiency and refresh it if it's necessary
    :param user: UserState - state of user
    :return:
    """
    client = await get_client(user.access_token)
    response = await client.get('/profile/me')
    if response.status_code != 200:
        user = await _refresh_token(user)
    return user
