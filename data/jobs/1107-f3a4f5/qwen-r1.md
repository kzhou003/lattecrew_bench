Done. Created `ledgerkit/durations.py` (parse/format) and `tests/test_durations.py`, committed as `32ce83a` on branch `crew/1107-f3a4f5`.

Verification: `python3 -m pytest -q` → **15 passed in 0.03s** (including the pre-existing money test).

Key behaviors verified: `parse('1.5h')` → `5400` (int), `parse('2d 3h')` → `183600`, `parse('-0.5s')` → `-0.5` (float), `format(5400)` → `'1h30m'`, `format(0)` → `'0s'`, `format(-5400)` → `'-1h30m'`, and `parse(format(x)) == x` roundtrips for all tested values. ValueError raised for empty text, bare numbers, unit-without-number, repeated units, and out-of-order units.