Done.

- `ledgerkit/cache.py`: `TTLCache(maxsize, ttl, clock=time.monotonic)` with `put`, `get`, `__len__`, `__contains__`, `stats()`. LRU via `OrderedDict`; expired entries (`clock() - stored_time >= ttl`) are dropped before any eviction (not counted as evictions), `get` refreshes order but not expiry, `__contains__` is side-effect-free, all ops under a single `threading.Lock`, `ValueError` on `maxsize < 1` or `ttl <= 0`.
- `tests/test_cache.py`: 19 tests covering hits/misses/evictions, exact-TTL boundary, LRU refresh, expired-dropped-before-eviction, param validation, default clock, and a 8-thread concurrency test.

Command: `python3 -m pytest -q` → `19 passed in 0.14s`

Committed on `crew/1107-aef866`: `fc4b238 Add TTLCache: thread-safe LRU cache with per-entry TTL expiry` (not pushed).