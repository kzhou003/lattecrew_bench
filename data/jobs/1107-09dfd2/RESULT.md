I rewrote `split` in `ledgerkit/money.py` to use the largest remainder method with integer arithmetic only. `python3 -m pytest -q` passes (9 passed), and I committed the change as `b6ed0dd`.

- **How it works:** each party gets the floor of its exact share, using `//` and `%` on integers. The leftover cents go to the largest remainders, with ties going to the lower index.
- **Negative totals:** these split like the absolute value, with every result negated.
- **Errors:** it raises `ValueError` for empty weights, any negative weight, or all-zero weights.
- **Tests:** I added tests to `tests/test_money.py` for:
  - exact sums and remainder ordering
  - negative totals
  - zero weights and a zero total
  - a very large total
  - the three error cases

I assumed the weights are integers. Float weights would probably still work, but they wouldn't be exact.