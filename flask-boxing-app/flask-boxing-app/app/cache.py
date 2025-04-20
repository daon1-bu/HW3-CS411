import time
from .models import Boxer

class BoxerCache:
    def __init__(self, ttl_seconds=60):
        self._cache = {}
        self._ttl = {}
        self.ttl_seconds = ttl_seconds

    def get_boxer(self, boxer_id):
        now = time.time()
        if boxer_id in self._cache and now < self._ttl[boxer_id]:
            return self._cache[boxer_id]
        boxer = Boxer.query.get(boxer_id)
        if boxer:
            self._cache[boxer_id] = boxer
            self._ttl[boxer_id] = now + self.ttl_seconds
        return boxer
