I ran `python3 -m pytest -q` in the worktree: 38 passed in 16.33s. I also ran my own probe script (`/tmp/p.py`), which passed. It covered:
- Wait-then-acquire cycles at rates 0.1, 3, 7, 1e-3 and 13.7, with clock offsets of 0, 1e6 and 12345.678, over 5000 cycles each. Every `try_acquire(n)` after waiting exactly `wait_time(n)` succeeded.
- A clock that goes backwards. No tokens were added or removed, and refill resumed from the new time.
- `ValueError` for rate ≤ 0, capacity ≤ 0, and n ≤ 0 or n > capacity, on both `try_acquire` and `wait_time`.

The code matches the task. It does all token arithmetic in exact `Fraction`s, so floating point error can't build up. It holds a lock around refill and acquire, so concurrent threads can't take more tokens than exist. `wait_time` returns the smallest float delay that lands the clock at or past the required time, which is what makes the exact-wait property hold. The nested search loops in `wait_time` are verbose, but I found no failing case.

VERDICT: PASS