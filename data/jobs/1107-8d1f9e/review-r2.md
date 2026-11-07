I found no real problems in the change.

- **Tests:** `python3 -m pytest -q` gives 88 passed.
- **Stress run (my own script):** I ran 5000 drain, wait and acquire cycles per combination, with start clocks of 0, 1e6, 1e9 and 123456.789 and rates of 0.1, 3, 7, 1e-3 and 1e3. `try_acquire(n)` succeeded after `wait_time(n)` every time. Each combination took under 0.2s.
- **Clock rollback:** the balance did not change, and refill resumed from the new timestamp.
- **Accounting:** it uses exact `Fraction` arithmetic under a single lock. Refill is capped at capacity, and the validation errors are raised for both methods.

VERDICT: PASS