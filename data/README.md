# Data dictionary

All times in milliseconds unless the field name says otherwise. Personal paths are rewritten to `/home/user` and `/Users/user`.

## `raw/`

| File | Rows | Fields |
|---|---|---|
| `stack.jsonl` | one per probe | `probe`, `n`, `p50`, `p95`, `min`, `samples` (all values) |
| `harness.jsonl` | one per run | `probe` (`claude`/`opencode`), `wall_ms`, Claude: `api_ms`, `cost`, `input`, `cache_write`, `cache_read`, `output`; OpenCode: `steps`, `tokens` |
| `kiro.jsonl` | one per gateway turn | deltas of `prompt_tokens_total`, `prompt_tokens_cached_total`, `generation_tokens_total`, `request_success_total`, `request_prefill_time_seconds_sum`, `request_decode_time_seconds_sum`; `wall` (s), `turn`, `label` |
| `llm-grid.jsonl` | one per request | `ttft_ms`, `e2e_ms`, `tpot_ms`, `gap_p99_ms`, `prompt_tokens`, `completion_tokens`, `label` (`cold`/`hit`), `target`, `rep`, `srv` (all `/metrics` deltas) |
| `llm-conc.jsonl` | one per concurrency level | `concurrency`, `wall_s`, `ttft_ms` (mean), `ttft_max`, `tpot_ms`, `throughput` (tok/s) |
| `llm-paths.jsonl`, `mac-paths.jsonl` | one per request | as grid; `label` = `direct`, `swap`, `tunnel` |
| `kernel.jsonl`, `spec.jsonl` | one per test | `label` (config), `test` (`prefill`, `decode`, `c2`, `code_think`, `code_nothink`), `chars`, `prompt`, `out`, `ttft_ms`, `tpot_ms`, `tok_s`; spec adds `num_draft_tokens`, `num_accepted_tokens`, `accept_rate` |
| `media.jsonl` | one per request | `kind` (`zimage`/`tts`/`wan`), `secs`, `start`/`end` (Unix s); Z-Image `steps`, `size`; TTS `text`, `chars`, `audio` (s), `rtf`; Wan `frames`, `steps`, `bytes` |
| `media-gpu.csv` | 4 Hz | timestamp, util %, mem util %, memory MiB, power W, SM MHz, mem MHz, PCIe gen |
| `llm-gpu.csv` | 1 Hz | Unix time, util %, mem util %, memory MiB, power W, SM MHz, mem MHz, temp °C, PCIe gen |
| `llm-metrics.txt` | – | one full Prometheus scrape of vLLM after E1–E2 |
| `ledger.jsonl` | one per agent run | crewd ledger for benchmark jobs: `job`, `provider`, `role`, `tag`, `cost_usd`, `seconds`, `tokens` |
| `spec.log`, `media.log` | – | console logs of those runs |

## `jobs/<id>/`

One directory per collaboration job (ids in `collab/results.jsonl`): `job.json` (state, rounds, `round_heads`, findings), `qwen-r<N>.log` (OpenCode JSON events), `qwen-r<N>.md` (coder's self-report), `local_reviewer-r<N>.log` / `worker*.log` (Claude Code stream-json), `review-r<N>.md`.

## `profiler/{prefill,decode}/`

`rank0.profiler_out.txt`: torch profiler key averages (Self CUDA per kernel). `trace.pt.trace.json.gz`: the full trace; open in https://ui.perfetto.dev.

## `../collab/`

`results.jsonl`: one row per job (arm, trial, task, state, wall, cost, Codex plan text and usage). `scored.json`: hidden-test and edge-test results per job and per round, plus token usage extracted from the logs.
