I reviewed the diff and ran `python3 -m pytest -q` in the worktree. It gave 12 passed in 0.01s, so pytest is installed here despite the plan's note.

The change does what the task asked:
- `split` materializes `weights` once and raises `ValueError` for empty weights, a negative weight, or an all-zero sum.
- It uses only integer arithmetic (`divmod`), with no floats.
- Leftover cents go to the largest remainders, with ties broken by the lower index.
- A negative total is allocated as its absolute value and then negated.
- The new tests cover the task's cases: the largest-remainder and tie-break examples, the negative mirror, a zero total, sum preservation, and each invalid input.

I found no correctness bugs and nothing unrelated to the task.

VERDICT: PASS