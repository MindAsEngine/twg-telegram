from aiogram.fsm.storage.redis import RedisStorage, Redis

import env_config as config

storage = RedisStorage(
    Redis(
        host=config.REDIS_HOST,
        port=config.REDIS_PORT,
        db=0)
)

