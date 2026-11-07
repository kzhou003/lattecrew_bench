I read `ledgerkit/cache.py` and ran the tests. I did not read `tests/test_cache.py` beyond its line count (181 lines).

- **Test run:** `python3 -m pytest -q` gave 14 passed.
- **Spec check:** the implementation matches every point in the task:
  - Constructor validation raises `ValueError` for `maxsize < 1` or `ttl <= 0`.
  - The expiry check is `now - stored_time >= ttl`.
  - `put` and `get` drop expired entries before any LRU eviction, and dropping them is not counted as an eviction.
  - Only a live LRU entry evicted on a full `put` increments `evictions`.
  - `put` on an existing key replaces the value, restarts the TTL and moves the key to the end.
  - `get` refreshes LRU order without changing the stored time.
  - A `get` on a missing or expired key counts a miss.
  - `__contains__` does not touch order or the hit/miss counters.
  - Every method takes an `RLock`, and `now` is sampled once per operation.

I found no real problems.

VERDICT: PASS