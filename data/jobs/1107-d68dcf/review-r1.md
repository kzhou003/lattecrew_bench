I found no problems in `ledgerkit/cache.py`. I read it against each requirement in the task and ran `python3 -m pytest -q`, which gave `13 passed`. I only skimmed `tests/test_cache.py` (13 tests, all passing); I didn't read each test.

- **Validation:** `maxsize < 1` and `ttl <= 0` raise `ValueError`.
- **Expiry:** entries are expired when `now - stored_time >= ttl`. Every public method purges expired entries first, so they are never returned and never counted in `len`. Purging does not touch the eviction counter.
- **Eviction order:** `put` purges before checking capacity, so a live entry is not evicted while an expired one exists. When the cache is still full, it evicts the leftmost (least recently used) entry and counts one eviction.
- **Existing key:** `put` replaces the value, restarts the stored time, moves the key to the end, and does not grow the cache.
- **`get`:** a hit moves the key to the end but leaves the stored time alone. A missing or expired key counts a miss and returns the default.
- **`__contains__`:** it changes neither LRU order nor the hit/miss counters.
- **Stats:** `stats()` returns a fresh dict with exactly `hits`, `misses` and `evictions`.
- **Thread safety:** every method holds the `RLock`, and each takes a single clock reading.

VERDICT: PASS