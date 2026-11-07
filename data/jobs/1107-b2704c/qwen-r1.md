Done. Created `ledgerkit/slots.py` with `free_slots(busy, day_start, day_end, min_minutes=0)` (validates aware datetimes and ordering, normalizes to `day_start`'s tz, clips/merges busy intervals, filters gaps by `min_minutes`) and `tests/test_slots.py` with 22 tests covering clipping, merging, touching intervals, mixed offsets, zero-length busy, `min_minutes` boundaries, and all `ValueError` cases.

- Command: `python3 -m pytest -q` → `22 passed in 0.03s`
- Committed `0a201aa` on `crew/1107-b2704c`, not pushed.