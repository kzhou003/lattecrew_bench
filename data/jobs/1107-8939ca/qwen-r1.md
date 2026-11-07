Done.

- `ledgerkit/durations.py`: `parse(text)` (strict tokenizer over `NUMBER+UNIT` parts, d→h→m→s order, each unit once, optional leading `-`, `Decimal` accumulation, int for whole values / float otherwise) and `format(seconds)` (canonical `1h30m` form, zero parts omitted, `0s` for zero, `-` prefix, `ValueError` for fractional/non-finite/non-numeric input).
- `tests/test_durations.py`: 71 tests covering valid/invalid parsing, formatting, and round trips.
- Verified round trip `parse(format(x)) == x` over ~50k values including negatives.

Command: `python3 -m pytest -q` → `71 passed in 0.05s` (pytest 7.4.4 was already available, contrary to the plan's baseline note).

Committed as `be22e55` on branch `crew/1107-8939ca`; not pushed.