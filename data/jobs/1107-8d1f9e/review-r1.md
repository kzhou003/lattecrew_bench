The background stress script (`/tmp/f.py`) was stopped after it reached its time limit. This is the same slow `wait_time` behavior I described in the review. I won't restart it.

My review stands: the change needs fixes before it passes.

**`ledgerkit/limiter.py:55-66`: `wait_time` is far too slow when the clock value is large.**
- The correction loop raises `seconds` by one ulp (the smallest float step) at a time.
- When `last_time` is around 1e6 and the wait is a fraction of a second, the clock values it can reach are much further apart than the ulp steps of `seconds`. That takes about 1e6 iterations, and each one does `Fraction` arithmetic.
- Example: rate=3, capacity=5, clock at 1000091.6666666677, tokens=2**-32, `wait_time(1.5)`. It was still running after 10 seconds.
- Fix: step over candidate clock times with `target = math.nextafter(target, math.inf)`, starting from `last_time + seconds`. Check `tokens + Fraction(target - last_time) * rate >= amount`, and return `target - last_time` when it passes.
- Add a test with clock starts of 1e6 and 1e9, rates 3, 7 and 0.1, partial balances and fractional `n`, over a few thousand cycles. `wait_time` should return quickly each time, and `try_acquire(n)` should then succeed.

VERDICT: CHANGES