The limiter hands out tokens that don't exist when the capacity is large, so I'm sending it back. `python3 -m pytest -q` passes (23 passed), but the tests don't cover this case.

**Bug: the tolerance scales with capacity, `ledgerkit/limiter.py:24, 42, 52`.** `self._tolerance = _EPS * capacity` means a request is accepted whenever `tokens + 1e-6*capacity >= n`. For large capacities that tolerance is whole tokens, not floating-point noise.

I reproduced it with `rate=1, capacity=10**6` and a fixed clock:
- `try_acquire(10**6)` returns True and empties the bucket.
- `try_acquire(1)` then returns True twice more, and `wait_time(1)` returns 0.0.

With `capacity=10**7`, after draining the bucket, 100 further `try_acquire(1)` calls all succeed with no time passing. This breaks the requirement that N threads can never acquire more than the tokens that exist.

**Fix:** Don't use a tolerance to hide accumulated error. Either of these works:
1. **Exact arithmetic.** Store the tokens as `fractions.Fraction`, or as integer ticks (for example `Fraction(rate)` and a `Fraction` time delta). Then `wait_time` is exact and `try_acquire` after exactly `wait_time` succeeds with no epsilon. Convert the float clock values with `Fraction(now)`, which is exact.
2. **Tiny relative epsilon.** If you keep floats, use a tolerance of about `1e-9 * max(1.0, n)` or `4 * sys.float_info.epsilon * max(n, tokens)`. This is rounding-scale and never a meaningful fraction of a token. Also make `wait_time` return a value that, when added to the time, reaches `n`. For example, round it up with `math.nextafter` until `tokens + wait*rate >= n`.

**Tests to add** (the existing ones miss this):
- For a large capacity such as 10**6 or 10**7, after draining, `try_acquire(1)` must return False and `wait_time(1)` must be about `1/rate`.
- The cycle test (rates 0.1, 3 and 7, thousands of cycles) must still pass.
- A concurrency test on a large-capacity bucket with a fixed clock, asserting the total acquired is at most `capacity`.

VERDICT: CHANGES