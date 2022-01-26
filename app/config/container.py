from dependency_injector import containers, providers

from app.config.config import settings
from app.config.redis import init_redis_pool
from app.services.cache import CacheService


class Container(containers.DeclarativeContainer):
    redis_pool = providers.Resource(
        init_redis_pool,
        url=settings.REDIS_URL,
    )

    cache_service = providers.Factory(
        CacheService,
        cache=redis_pool,
    )
