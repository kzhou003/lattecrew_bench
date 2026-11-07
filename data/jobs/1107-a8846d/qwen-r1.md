Done.

- Created `ledgerkit/slots.py` with `free_slots(busy, day_start, day_end, min_minutes=0)`: validates aware endpoints / reversed intervals / `day_end <= day_start` (all `ValueError`), normalizes to UTC for clipping, merging (touching intervals merge via `<=`), and duration checks, then converts retained gaps back to `day_start`'s timezone. Zero-length busy intervals are ignored.
- Created `tests/test_slots.py` with 15 tests covering all planned cases, including a DST fall-back regression (2025-11-02 LA) verifying `min_minutes` filtering uses actual elapsed UTC minutes (485 min gap kept at threshold 480, wall clock would read 425) with output in `America/Los_Angeles`.

Test command and actual result:
```
$ python3 -m pytest -q
15 passed in 0.03s
```

Committed as `5fbf079` on branch `crew/1107-a8846d` (not pushed).