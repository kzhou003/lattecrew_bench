I added `CsvStream` in `ledgerkit/csvstream.py` with tests in `tests/test_csvstream.py`. `python3 -m pytest -q` passes (79 passed, which includes the existing money tests). The work is committed on `crew/1107-000096` as `8ea038e`.

**What the tests cover:**
- **Record ends:** LF, CRLF, lone CR, and a CRLF split across two chunks counting as one record end.
- **Chunk splits:** a split-equivalence test feeds a mixed input at every chunk size from 1 up to the full length and checks the rows are identical each time. A quote pair split across chunks is tested directly.
- **Fields and blank lines:** blank lines, `'a,'` giving `['a', '']`, and `'""'` giving `['']`.
- **Quotes:** quoted fields containing delimiters and newlines, and a quote inside an unquoted field being an ordinary character.
- **Errors:** a `ValueError` for characters after a closing quote and for an unterminated quote at `finish()`.
- **Reuse:** the parser can be reused after `finish()`, and after a `ValueError`.

**Behaviours the spec left open:**
- `finish()` returns the final row as a single `list[str]`, or `None` if there is none. Your spec says "returns any final row", so I read it as one row and not a list of rows. If you wanted a list (`[]` or `[row]`), that's a small change.
- `feed()` raises `ValueError` and resets the parser. Any rows already completed in that same chunk are lost.
- The constructor raises `ValueError` if the delimiter isn't a single character, or is `"`, CR or LF.