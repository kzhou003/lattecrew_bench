Done.

- **ledgerkit/cache.py**: `TTLCache(maxsize, ttl, clock=time.monotonic)` — OrderedDict-based LRU (`key -> (value, stored_time)`), `threading.RLock` around every operation, single `clock()` sample per op, `_purge_expired` (expired when `now - stored_time >= ttl`, never counted as evictions) runs before `put`/`get`/`len`/`__contains__`/`stats`. `put` on existing key replaces value, restarts TTL, refreshes order, no eviction; fresh `put` at capacity evicts leftmost live entry (+1 eviction). `get` refreshes recency only. `__contains__` touches no counters/order. `stats()` returns a fresh `{"hits", "misses", "evictions"}` dict. `ValueError` for `maxsize < 1` / `ttl <= 0`.
- **tests/test_cache.py**: 12 tests covering constructor validation, basic put/get with defaults and hit/miss accounting, inclusive expiry boundary via a fake clock, expired-entry behavior (miss, absent from len/in, not an eviction), LRU eviction ordering, expired-before-eviction rule, existing-key put (value/order/TTL/no eviction), `__contains__` non-effects, zeroed stats, and an 8-thread concurrency smoke test.

Verification command and result:

```
$ python3 -m pytest -q
13 passed in 0.04s
```

Committed as `b89f298` on branch `crew/1107-d68dcf`; nothing pushed, no branch switched.