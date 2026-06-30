import redis
class CacheService:
    def __init__(self,url="redis://localhost:6379/0"):
        self.client=redis.from_url(url)
cache_service=CacheService()
