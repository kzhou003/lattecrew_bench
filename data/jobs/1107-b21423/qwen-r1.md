Done. `split()` (ledgerkit/money.py:1) now uses the largest remainder method with pure integer arithmetic: floor shares, leftover cents to largest remainders (ties → lower index), negative totals negated, and `ValueError` on empty/negative/all-zero weights. Added 14 tests in tests/test_money.py covering ties, negatives, large values, a 200-case property test, and error cases.

- Command: `python3 -m pytest -q`
- Result: `14 passed in 0.03s`
- Committed as `ace9b02` on the current branch.