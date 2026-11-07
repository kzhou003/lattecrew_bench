I found no real problems, so the change passes.

I ran `python3 -m pytest -q` in the worktree: 19 passed.

I read `ledgerkit/cache.py` against each requirement in the task:
- **Expiry boundary:** an entry is live only while `now - stored_time < ttl`, so it counts as expired at exactly `ttl`.
- **Eviction order:** `put` of a new key inserts it, and only if the cache is then over `maxsize` does it drop all expired entries first. It evicts the LRU entry only if the cache is still over `maxsize`. The new key sits at the end of the order, so it can't evict itself, and dropping expired entries is not counted as an eviction.
- **Replacing an existing key:** `put` replaces the value, restarts its ttl, refreshes its order and counts no eviction.
- **Reads:**
  - `get` counts a miss for a missing or expired key and removes the expired entry.
  - A hit refreshes LRU order but leaves the stored time alone.
  - `__len__` counts only live entries.
  - `__contains__` changes neither order nor stats.
- **Validation and thread safety:** both `ValueError` checks are present, and every method takes the same lock. The clock is only read inside it.

I did not read `tests/test_cache.py` line by line. It is 228 lines and passes.

VERDICT: PASS