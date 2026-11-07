I found no problems. I did not read `tests/test_durations.py` line by line.

I ran `python3 -m pytest -q` in the worktree and got 71 passed.

I read `ledgerkit/durations.py` against the spec and the planner's traps:
- **Parsing:** `parse` walks the whole string by hand, so trailing junk, a bare number like `5`, a unit with no number and `1 h` (space before the unit) all raise `ValueError`.
- **Ordering and repeats:** unit order is checked by rank, independent of the numbers. Repeated units, out-of-order units and any `-` after the first character are rejected.
- **Sign and exactness:** `Decimal` makes `1.5h` give exactly `5400` as an `int`, with no float artifacts. A fractional-second result such as `1.5s` comes back as a `float`. The leading `-` applies to the whole total.
- **Formatting:** `format` gives `0s` for zero, drops zero parts (`86401` gives `1d1s`), puts `-` in front for negatives, and raises `ValueError` for fractional, non-finite or non-numeric input. Because it emits the canonical form, `parse(format(x)) == x`.

One minor point, not worth blocking on: `format(True)` returns `1s`, because `bool` is a subclass of `int`.

VERDICT: PASS