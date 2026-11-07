Done.

- `ledgerkit/durations.py`: `parse(text)` handles `d/h/m/s` (largest→smallest, each once, optional spaces, decimals, leading `-`), returns `int` for whole values else `float`, raises `ValueError` on empty/bare-number/unitless/repeated/out-of-order input. `format(seconds)` returns canonical form (`'1h30m'`, `'0s'`, `-` prefix), and `parse(format(x)) == x` holds.
- `tests/test_durations.py`: 51 tests covering all the above.
- Command: `python3 -m pytest -q` → `51 passed in 0.05s`
- Committed to `crew/1107-c20793`: `70502f9 Add durations module with parse/format for durations`