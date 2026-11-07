Done.

- `ledgerkit/money.py:1` — `split` now materializes weights once, validates (empty / negative / all-zero → `ValueError`), allocates via `divmod(abs(total) * w, weight_sum)`, ranks by descending remainder with lower-index tiebreak, and negates results for negative totals. Pure integer arithmetic.
- `tests/test_money.py` — 12 tests covering all planned cases plus sum-preservation and iterable input.

Verification: `python3 -m pytest -q` → **12 passed in 0.02s** (pytest was in fact available, despite the environment note).

Committed as `169537b` on `crew/1107-98c9d8`; not pushed, no branch switch.