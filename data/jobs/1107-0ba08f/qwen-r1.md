Done.

- `ledgerkit/slots.py`: `free_slots(busy, day_start, day_end, min_minutes=0)` — validates awareness (ValueError on naive), `end < start`, `day_end <= day_start`; clips busy to the window, drops zero-length/outside intervals, sorts, merges overlapping+touching intervals, walks the window to emit gaps ≥ `min_minutes`, all converted to `day_start`'s timezone.
- `tests/test_slots.py`: 26 tests covering clipping, overlap/merge, unsorted input, mixed UTC offsets, timezone conversion, `min_minutes`, and all ValueError cases.

Command and result: `python3 -m pytest -q` → `26 passed in 0.03s`.

Committed as `be1d15b` on `crew/1107-0ba08f` (no push, no branch switch).