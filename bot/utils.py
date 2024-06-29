from aiogram.fsm.storage.redis import RedisStorage, Redis

import config

storage = RedisStorage(
    Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0)
)

