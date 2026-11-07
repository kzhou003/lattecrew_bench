Done. Fixed at the root cause in `ledgerkit/durations.py`:

- `parse` now accumulates with exact `Fraction` arithmetic (ledgerkit/durations.py:32,46) and returns `int(total)` when `total.denominator == 1`, else `float(total)` — so `parse('0.7d')` → `60480` (int), `parse('0.1d')` → `8640`, `parse('2.3h')` → `8280`, `parse('1.1h2.3m')` → `4098` (int).
- Also applied the minor regex fix: `\d` → `[0-9]` (ledgerkit/durations.py:12), so `parse('٣s')` now raises `ValueError`.
- Added the suggested tests plus the `1.1h2.3m` sum and a non-ASCII-digit rejection case in `tests/test_durations.py`.

Verification: `python3 -m pytest -q` → **16 passed in 0.03s**.

Committed as `20d36bf` on `crew/1107-f3a4f5`. Left the optional `'- 5s'` case as-is since the task doesn't define whether that should be allowed.