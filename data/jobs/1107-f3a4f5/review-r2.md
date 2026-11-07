I found no real problems in the change.

I ran `python3 -m pytest -q` and got `16 passed in 0.02s`. I also read `ledgerkit/durations.py` against each requirement in the task:
- **`parse`:** it uses exact `Fraction` arithmetic, so decimals like `0.7d` come back as whole ints and fractional values come back as floats. It enforces largest-to-smallest order with each unit at most once. It rejects empty text, a bare number, a unit with no number, repeated units and out-of-order units.
- **`format`:** it gives the canonical form, omits zero parts, returns `0s` for zero and puts a leading `-` on negatives. `parse(format(x)) == x` holds for the round-trip values the tests cover.

One minor leniency, not worth blocking on: `parse("- 5s")` is accepted, because whitespace after the leading `-` is skipped. The task doesn't forbid it.

VERDICT: PASS