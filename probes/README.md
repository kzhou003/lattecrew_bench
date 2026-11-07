# Probes

| Script | Where | Usage |
|---|---|---|
| `stack_probe.py` | Mac | `python3 stack_probe.py out.jsonl` (needs `ssh latte` and `~/latte-crew/crew.py mcp` there; for the scp test first run `ssh latte 'head -c 1M /dev/urandom > /tmp/lc-1m'`) |
| `harness_probe.py` | GPU host | `NODE_BIN=$(dirname $(which node)) python3 harness_probe.py` → `~/latte-bench/out/harness.jsonl` |
| `llm_probe.py` | either | `python3 llm_probe.py <base_url> <out.jsonl> grid\|conc\|paths [--metrics <url>/metrics] [--label name]` |
| `capture_proxy.py` | GPU host | `[REORDER=1] python3 capture_proxy.py capture.jsonl`, then point OpenCode's `baseURL` at `http://127.0.0.1:8110/v1`; restore it afterwards |
| `kprobe.py`, `run_kernel.sh` | GPU host | `bash run_kernel.sh` (holds the GPU lock, restarts vLLM per config, then the profiler run) |
| `kprobe2.py`, `run_spec.sh`, `task_t5.txt` | GPU host | `bash run_spec.sh` (base + MTP k = 1..3) |
| `media_probe.py` | GPU host | `touch out/.m; ./gpu_fast.sh out/media-gpu.csv out/.m & python3 media_probe.py; rm out/.m` |
| `gpu_trace.sh`, `gpu_fast.sh` | GPU host | `<out.csv> <stopfile>`: sample until the stop file is removed (1 Hz / 4 Hz) |

The scripts expect the LatteCrew layout on the GPU host: `~/latte-models` (serve scripts, `env/`, `gpu.lock`), llama-swap on :8100 and vLLM on :8101. They write to `~/latte-bench/out/`.
