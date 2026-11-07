# Tools and how they were used

| Tool | Used for | How |
|---|---|---|
| `time.perf_counter()` | every client-side timing | wrap one call; median over repeats |
| vLLM Prometheus `/metrics` | server-side truth: prefill and decode seconds, prompt and cached tokens, request counts, speculative-decoding drafts and acceptances | scrape before and after a request, take the difference; sum labelled series by name |
| vLLM flags `--enable-mfu-metrics --kv-cache-metrics` | extra counters (estimated FLOPs, bytes read/written, KV usage, prefix-cache queries and hits) | added to `serve-qwen.sh` |
| vLLM `/tokenize` | find the first token where two agent requests differ | send `messages` + `tools`, compare token lists |
| vLLM torch profiler | per-kernel GPU time for one prefill and one decode | `--profiler-config '{"profiler":"torch","torch_profiler_dir":...}'`, then `POST /start_profile` and `POST /stop_profile` around one request; read `rank0.profiler_out.txt` (Self CUDA) |
| Chrome trace viewer / Perfetto | look at the profiler timeline | open `data/profiler/*/trace.pt.trace.json.gz` in https://ui.perfetto.dev |
| `nvidia-smi --query-gpu=... -lms 250` | GPU utilization, memory, power, SM and memory clocks at 4 Hz | background loop until a stop file disappears (`gpu_fast.sh`) |
| safetensors headers | bytes of weights per component (layers, `lm_head`, embeddings, vision, MTP) for the bandwidth roofline | read the 8-byte header length and the JSON header of each shard; sum `data_offsets` |
| logging reverse proxy (`capture_proxy.py`) | see exactly what Kiro and OpenCode send to the model | stdlib `http.server` on :8110 forwarding to llama-swap; point OpenCode's `baseURL` at it temporarily |
| `ssh` with `ControlMaster` | reuse one connection for many commands | `-o ControlPath=... -o ControlMaster=yes -o ControlPersist=120 -fN` |
| MCP over stdio | time MCP calls without a client library | write `initialize` and `tools/call` JSON-RPC lines into `crew.py mcp` |
| `claude -p --output-format json` | Claude Code timing, tokens and cost | read `duration_api_ms`, `usage`, `total_cost_usd` |
| `opencode run --format json` | OpenCode steps and tokens | read `step_start`, `tool_use` (with start/end times), `step_finish` (tokens) |
| `codex exec --json --sandbox read-only` | planner runs and their token usage | read the last `agent_message` and `turn.completed.usage` |
| `kirocrew chat -m` | one gateway turn from the shell | with `KIROCREW_HOME`/`KIROCREW_PORT` for the `@qwen` gateway |
| crewd ledger and job logs | stage seconds and cost per job; per-round commits (`round_heads`) | `~/latte-crew/var/ledger.jsonl`, `var/jobs/<id>/` |
| `git worktree`, `git archive` | isolated jobs; scoring a commit without touching any worktree | `git archive <sha> \| tar -x -C <tmp>` then pytest |
| `flock` on `~/latte-models/gpu.lock` | keep bots from swapping models during a measurement | `exec 9>>gpu.lock; flock 9` in shell, `fcntl.flock` in Python |
| `setsid` + `kill -- -<pgid>` | start and fully stop a vLLM server per configuration | avoids `pkill -f` matching your own ssh command |
| conda (`cuda-nvcc=13.0`) | a CUDA compiler without sudo, for FlashInfer JIT | `conda create -p ~/latte-models/cuda13 -c conda-forge cuda-nvcc=13.0 ...`; add `lib64 → targets/x86_64-linux/lib`; set `CUDA_HOME` |
| headless Chrome | render the report and export figures to PNG | `--headless=new --screenshot --window-size=W,H` |
| `node scripts/validate_palette.js` (dataviz skill) | check chart colors for color-blind safety in both themes | categorical slots 1–4 passed light and dark |
| `latexmk` | build the paper draft | not in this repo |
