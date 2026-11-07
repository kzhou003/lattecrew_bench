Tests pass: `python3 -m pytest -q` gives 22 passed. The code follows the spec on validation, clipping, merging, ignoring zero-length intervals, and sorted output in `day_start`'s timezone. It has one real bug, on days with a DST change.

**Problem: wall-clock arithmetic in a DST-aware zone, `ledgerkit/slots.py` (the `min_seconds` filter on the last line, and the `max`/`min`/comparisons above it)**

All datetimes are converted to `day_start.tzinfo`. Python then compares and subtracts datetimes that share a `tzinfo` by wall-clock time and ignores the UTC offset. With a `ZoneInfo` timezone, a fall-back day therefore gets the wrong duration.

I reproduced it with `ny = ZoneInfo('America/New_York')` and the window 2025-11-02 00:00 to 2025-11-03 00:00. That window is 25 real hours.
- `free_slots([], ds, de, min_minutes=24*60+30)` returns `[]`. It should return the full 25-hour gap, because `(e - s)` evaluates to 24h.
- The same wall-clock comparison can order or clip times wrongly around the repeated 01:00–02:00 hour.

**Fix:**
- Keep the interval logic in UTC. Convert `day_start`, `day_end` and each busy `start`/`end` with `.astimezone(timezone.utc)`, then do the clip, sort, merge and gap computation there.
- Convert the resulting gap endpoints back with `.astimezone(day_start.tzinfo)` only when building the return value.
- Measure the `min_minutes` filter on the UTC gaps, so the durations are real elapsed time.
- Add a test for the fall-back day above: a `min_minutes` of 24*60+30 must still return the 25-hour gap.
- Add a test for a busy interval inside the repeated hour.

VERDICT: CHANGES