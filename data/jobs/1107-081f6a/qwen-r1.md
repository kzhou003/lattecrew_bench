Done.

- **ledgerkit/durations.py**: `parse(text)` strictly tokenizes `NUMBER UNIT` parts (manual scan, no permissive regex), enforces largest-to-smallest order (`d>h>m>s`), each unit at most once, optional whitespace only between complete parts, one leading `-` for the whole value; accumulates with `Decimal` and returns `int` for whole values, `float` otherwise, raising `ValueError` on empty/bare-number/missing-number/repeated/out-of-order/malformed input. `format(seconds)` validates integral finite input, decomposes via `divmod`, omits zero parts, returns `0s` for zero, `-` prefix for negatives.
- **tests/test_durations.py**: valid/invalid parse, int vs float return types, format cases, bad-input rejection, and round-trip `parse(format(x)) == x` for 20 values including 0, negatives, and multi-day.

Verification: `python3 -m pytest -q` → `87 passed in 0.06s` (86 new + 1 pre-existing).

Committed as `8b81597` on branch `crew/1107-081f6a` ("Add durations module with parse and format for d/h/m/s durations"); no push, no branch switch.