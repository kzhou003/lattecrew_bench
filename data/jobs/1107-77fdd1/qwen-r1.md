Done.

- **ledgerkit/money.py:1** — rewrote `split()` with exact integer arithmetic: each party gets the floor of its exact share (`amount * w // total_weight`), then the leftover cents go to the largest fractional remainders (`amount * w % total_weight`), ties broken by lower index. Negative totals split like their absolute value with results negated; `ValueError` raised for empty weights, negative weights, or all-zero weights.
- **tests/test_money.py** — 16 tests: largest remainder, tie-breaking, negative totals, zero weights, float-precision case (`split(3, [1000000, 1]) == [3, 0]`), all three error cases, plus a 200-iteration randomized property test (sum exactly equals total, each share within 1 of exact share).

Verified: `python3 -m pytest -q` → `16 passed in 0.03s`.

Committed to branch `crew/1107-77fdd1` as `7318a0b` (not pushed).