Review of the `split()` change against the task.

I ran `python3 -m pytest -q` in the worktree. It passed with `11 passed in 0.01s`, so pytest is installed here despite the planner's note.

Checks against the task:
- **Algorithm:** `split()` in `ledgerkit/money.py` takes `divmod(amount * w, weight_sum)` for each weight, so quotients are exact floors. It ranks parties by `(-remainder, index)` and gives the leftover cents to the first `leftover` of them. That is the largest remainder method with lower-index tie-breaking, and it uses only integer arithmetic.
- **Negative totals:** it works on `abs(total_cents)` and negates every result at the end. That gives `[-2, -2, -1]` for `split(-5, [1,1,1])`, as the task specifies.
- **Validation:** empty weights, any negative weight, and all-zero weights each raise `ValueError`. The weights are copied into a list first, so a generator input is not consumed twice.
- **Leftover count:** `leftover` always falls between 0 and `len(ws) - 1`, because the quotients sum to at least `amount - (n - 1)`. The slice `order[:leftover]` is therefore safe.
- **Tests:** `tests/test_money.py` covers every case the plan listed: the five allocation cases, zero total, the three error cases, and sum preservation for positive and negative totals. The expected values are correct.

I found no problems, and the diff contains nothing unrelated to the task.

VERDICT: PASS