import bson.json_util


class CacheService:
    def __init__(self, cache) -> None:
        self._cache = cache

    async def set(self, key, value, ex) -> str:
        await self._cache.set(key, bson.json_util.dumps(value), ex)
        return await self.get(key)

    async def get(self, key) -> str:
        return await self._cache.get(key)

    async def remember(self, key, callback, ex) -> str:
        val = await self.get(key)

        if not val:
            val = await callback()
            return await self.set(key, val, ex)

        return val
