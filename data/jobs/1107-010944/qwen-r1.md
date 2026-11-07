Done.

- `ledgerkit/cache.py`: `TTLCache(maxsize, ttl, clock=time.monotonic)` using `OrderedDict` + `RLock`. Purge-before-mutate on every operation; expiry is inclusive (`clock() - stored_time >= ttl`); evictions counted only for live entries; `__contains__`/`stats()` side-effect free; `ValueError` on `maxsize < 1` or `ttl <= 0`.
- `tests/test_cache.py`: 14 tests covering constructor validation, put/get/hit/miss, inclusive expiry boundary (fake clock), expired-entry semantics, LRU ordering, expired-before-eviction, existing-key put (value/order/TTL restart), `__contains__` neutrality, stats shape, and a concurrent smoke test.

Command: `python3 -m pytest -q`
Result: `14 passed in 0.07s` (committed as `6351301` on branch `crew/1107-010944`)