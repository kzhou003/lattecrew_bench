I found no real problems.

I ran `python3 -m pytest -q` and got 16 passed.

- **Method:** `split()` in `ledgerkit/money.py` does the largest remainder method as specified. It uses integer `//` and `%` only, with no floats. Ties go to the lower index through the `(-remainder, index)` sort key.
- **Sum is exact:** the leftover can never exceed the number of parties with a non-zero remainder. That means a zero-weight party never receives an extra cent, and the results always add up to `total_cents`.
- **Negative totals:** the code splits on the absolute value and negates every result.
- **Validation:** it raises `ValueError` for empty weights, any negative weight, and all-zero weights.
- **Tests:** they cover ties, negative totals, zero weights, the three error cases and a randomized check. The hand-computed expectations I checked, such as `split(10, [1,2,3]) == [2,3,5]` and `split(3, [1000000,1]) == [3,0]`, are correct.

VERDICT: PASS