from typing import AsyncIterator

from aioredis import from_url, Redis


async def init_redis_pool(url: str) -> AsyncIterator[Redis]:
    pool = await from_url(url)
    yield pool
    pool.close()
    await pool.wait_closed()