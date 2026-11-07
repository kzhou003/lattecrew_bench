I added `TTLCache` in `ledgerkit/cache.py` and its tests in `tests/test_cache.py`, and committed both as e2b2dc6 on `crew/1107-616f79`. `python3 -m pytest -q` reports 10 passed, covering the existing `test_money.py` and the new cache tests.

The cache follows your spec. Details worth knowing:
- **Locking:** every method takes an `RLock`, which makes it safe under concurrent threads.
- **Cost of the expiry sweep:** `put` of a new key and `__len__` scan all entries to drop expired ones, so they are O(n) in the number of entries. That is fine at small sizes but would be slow for very large caches.
- **Thread-safety test:** it runs 8 threads of mixed `put`, `get` and `len` calls. It checks that the cache stays within `maxsize` and that hits plus misses add up. It is a smoke test, not proof that there are no races.

I did not push anything.