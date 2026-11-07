# Collaboration benchmark

| Path | Contents |
|---|---|
| `tasks.json` | six tasks: `level`, `title`, `prompt` (t1 money.split, t2 durations, t3 TTLCache, t4 free_slots, t5 TokenBucket, t6 CsvStream) |
| `repo/` | the starting `ledgerkit` repository (one buggy module, one test) |
| `ref/` | reference solutions; they pass all hidden tests |
| `run.py` | driver: `python3 run.py claude\|local\|codex [t1 ...]`; `TRIAL=2` labels a rerun; Codex plans are reused across trials |
| `score.sh`, `score_remote.py` | copy hidden tests to the GPU host only for scoring; score each job's final and round-1 commits with `git archive` + pytest; extract token usage from logs |
| `results.jsonl`, `scored.json` | published results of trials 1 and 2 |

Hidden tests (`hidden/test_t<N>.py`, 175 cases) and reviewer-derived edge tests (`extra/`) are not published; see the top-level README.

To set up on the GPU host: copy `repo/` to `~/development/ledgerkit`, `git init -b main`, commit, and make sure `~/development` is in crewd's `repo_roots`.
