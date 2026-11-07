I added `ledgerkit/durations.py` with `parse` and `format`, plus `tests/test_durations.py`. `python3 -m pytest -q` ran 64 tests and all passed. The work is committed on `crew/1107-c79f82` as `64ade20`, and nothing is pushed.

I made a few choices where your spec was open:
- **Spaces:** Spaces are allowed between parts, and leading or trailing spaces are ignored. A space inside a part is an error, so `'1 h'` and `'- 1h'` raise `ValueError`.
- **Decimals:** `parse` does its arithmetic with `Decimal`, so `'1.1m'` gives exactly `66` rather than `66.00000000000001`. Values that aren't whole come back as `float`.
- **Zero:** `'-0s'` parses to `0`.
- **`format` input:** `format` accepts a whole-valued float such as `5400.0`. It raises `ValueError` for `1.5`, for strings, and for `None`.
- **`parse` input:** `parse` raises `ValueError` for non-string input.

The tests cover the valid examples from your spec, each invalid case, and `parse(format(x)) == x` for positive, negative and large values.