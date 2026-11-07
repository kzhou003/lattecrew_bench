The change does what the task asked and I found no real problems.

I ran `python3 -m pytest -q` in the worktree: 87 passed in 0.05s.

By reading `ledgerkit/durations.py` I checked these cases:
- **Valid input:** `1h30m`, `2d 3h` and `1.5h` are accepted, and `-0s` returns `0`.
- **Invalid input:** `""`, `"-"`, `"- 1h"`, `"--1h"`, `"1 h"` and `"1h-30m"` raise `ValueError`. A bare number, a unit with no number and a malformed decimal like `1.` also raise `ValueError`. So do repeated units and units out of order, including `0h1d`.
- **Return types:** the code uses `Decimal`, so whole values come back as `int` and fractional values as `float`.
- **`format`:** it omits zero parts, gives `0s` for zero and a leading `-` for negatives, and rejects fractional, non-finite and non-numeric input with `ValueError`.
- **Round trip:** the tests cover `parse(format(x)) == x`, including negative values.

I didn't run any inputs of my own beyond the test suite. The diff only touches `ledgerkit/durations.py` and `tests/test_durations.py`.

VERDICT: PASS