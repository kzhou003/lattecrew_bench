`TokenBucket` is in `ledgerkit/limiter.py`, with tests in `tests/test_limiter.py`. I committed both on `crew/1107-b985ad` as `2822600`. `python3 -m pytest -q` gives 20 passed, which covers the existing money tests and the new ones.

What the new tests check:
- **Basics:** the bucket starts full, a failed `try_acquire` takes nothing, and `wait_time` is pure.
- **Refill:** refill is capped at capacity, and a backwards clock adds and removes nothing while later refill continues from the new time.
- **Validation:** `ValueError` is raised for bad `rate`, `capacity` and `n` in both methods.
- **Exact wait:** over 5000 cycles with rates 0.1, 3 and 7, at clock starts 0 and 12345.678, waiting exactly `wait_time(n)` from empty always lets `try_acquire(n)` succeed.
- **Threads:** 16 threads making 8000 attempts against 1000 tokens acquired exactly 1000 in total.

To keep floating point error from building up, balances are exact `Fraction`s, and a lock guards every method.

**Tolerance:** the clock reading itself is a float, so `(now + w) - now` can come out slightly short of `w`. To absorb that, the code treats a balance within 1e-6 tokens of `n` as enough. In practice a request can succeed up to 1e-6 tokens early.