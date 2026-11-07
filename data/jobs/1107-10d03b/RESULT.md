I added `free_slots` in `ledgerkit/slots.py` with tests in `tests/test_slots.py`, and committed both on `crew/1107-10d03b` as 33c6266. `python3 -m pytest -q` gives 12 passed, which covers the 11 new slot tests and the existing money test file. I haven't pushed anything.

The tests cover these cases:
- unsorted and overlapping busy intervals
- touching intervals, which leave no zero-length gap
- clipping to the window, and intervals entirely outside it
- the `min_minutes` filter
- zero-length busy intervals
- mixed UTC offsets, with output in `day_start`'s timezone
- every `ValueError` case

One behaviour to be aware of: busy intervals are validated even when they fall outside the window. A naive datetime or an interval with `end < start` raises `ValueError` regardless of where it sits.