`parse('0.7d')` returns `60479.99999999999` instead of `60480`. That breaks the requirement that a whole value comes back as an int. I ran `python3 -m pytest -q` and all 15 tests pass, but none of them cover this case.

**Problem: float rounding in `ledgerkit/durations.py:46`**
- The line `total += float(match.group(1)) * _UNITS[...]` accumulates in binary floating point.
- `parse('0.7d')` gives `60479.99999999999`, a float, where the task says to return `60480` as an int.
- Other decimal inputs can drift the same way, for example `parse('0.1d')` and sums such as `1.1h2.3m`.
- The fix is to do the arithmetic exactly:
  1. Add `from fractions import Fraction` (or use `Decimal`).
  2. Replace `total = 0.0` with `total = Fraction(0)`.
  3. Use `total += Fraction(match.group(1)) * _UNITS[match.group(2)]`.
  4. At the end, return `int(total)` if `total.denominator == 1`, otherwise `float(total)`.
- The `total == int(total)` check on line 52 can then go.
- Add a test to `tests/test_durations.py`, for example `assert parse('0.7d') == 60480` and `isinstance(parse('0.7d'), int)`. Also add `parse('0.1d') == 8640` and `parse('2.3h') == 8280`.

**Minor, optional:**
- `\d` in the regex at line 12 also matches non-ASCII digits, so `parse('٣s')` returns `3`. Use `[0-9]` instead.
- `parse('- 5s')` is accepted, because spaces after the `-` are skipped. The task didn't say whether that should be allowed, so this is optional.

VERDICT: CHANGES