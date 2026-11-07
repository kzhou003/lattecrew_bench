Done. The bug is fixed at the root cause and committed.

- **Fix** (`ledgerkit/limiter.py`): replaced the capacity-scaled float tolerance with exact `Fraction` arithmetic, so the bucket can never grant tokens that don't exist. `wait_time` now searches the representable float clock to guarantee the returned delay makes the request affordable.
- **Tests** (`tests/test_limiter.py`): added large-capacity drain regression (10⁶, 10⁷), multi-rate/capacity cycle affordability, and large-capacity concurrency (no over-acquisition).
- **Verification**: 38 tests pass. Working tree clean, branch `crew/1107-41e94c`, commit `7c40081` (not pushed).