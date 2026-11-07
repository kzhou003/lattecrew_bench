Both changes match the task, and I found no real problems.

I ran `python3 -m pytest -q`: 14 passed.

- **Algorithm:** `split` in `ledgerkit/money.py` uses only integer arithmetic. It takes the floor of each exact share, ranks parties by remainder (largest first, lower index on ties) and gives one extra cent to each of the first `leftover` of them. A party with weight 0 never receives a leftover cent, because the leftover is at most the number of parties with a nonzero remainder.
- **Negative totals:** these recurse on the absolute value and negate each result.
- **Validation:** empty, negative and all-zero weights raise `ValueError`. Weights are copied with `list(weights)`, so generators work.
- **Tests:** they cover ties, largest-remainder ordering, negative totals, large integers, the sum invariant over random inputs and the three error cases.

One cosmetic point, not blocking: `test_tie_broken_by_lower_index` in `tests/test_money.py` isn't a tie. Its remainders are 2/3 and 1/3, so it really tests that the larger remainder wins. The `[1, 1, 1]` test is the one that covers the tie rule.

VERDICT: PASS