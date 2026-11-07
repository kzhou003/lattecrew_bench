# Experiments, in the order they were run

Dates are November 6–7, 2026. Each entry gives the goal, the exact way it was run, where the data is, and what happened, including runs that failed.

## E1. Model serving grid
- **Goal**: TTFT and TPOT vs. prompt length, cold and cached.
- **Run**: `probes/llm_probe.py http://127.0.0.1:8101 out/llm-grid.jsonl grid --metrics http://127.0.0.1:8101/metrics` with `gpu_trace.sh` in the background. Prompt lengths 500–60K target (506–65,401 actual), 4 reps, each cold then repeated.
- **Data**: `data/raw/llm-grid.jsonl` (each row has a `srv` dict of `/metrics` deltas), `llm-gpu.csv`, `llm-metrics.txt` (a full scrape at the end).
- **Result**: cold prefill ≈ 3,500 tok/s; cached TTFT 0.14–0.30 s at any length; TPOT 12.8 → 15.4 ms.
- **Note**: Qwen first failed to start: a desktop browser held ~2 GB VRAM and a fixed `--gpu-memory-utilization 0.90` did not fit. `serve-qwen.sh` now sizes it from free memory.

## E2. Concurrency and paths
- **Run**: `llm_probe.py ... conc` (1–4 parallel 4K-token prompts, 300 output tokens); `llm_probe.py ... paths --label direct|swap` on latte against :8101 and :8100, and `--label tunnel` on the Mac against the SSH tunnel :18100.
- **Data**: `llm-conc.jsonl`, `llm-paths.jsonl`, `mac-paths.jsonl`.
- **Result**: 2-way 1.55× throughput at +14% TPOT; c=3–4 queue (2 sequences max). llama-swap +1.4 ms, tunnel +29 ms.

## E3. Connection layer
- **Run** (Mac): `probes/stack_probe.py out/stack.jsonl`.
- **Data**: `stack.jsonl`. The `claude_p_once` rows are invalid (`--tools ""` broke the CLI on the Mac) and are ignored; E4 replaces them.
- **Result**: SSH 357 → 38 ms with connection reuse; MCP 459 ms new session, 10 ms live.

## E4. Agent harness and Kiro
- **Run**: `probes/harness_probe.py` on latte (first version failed because `~` was not expanded in `PATH`); Kiro turns with an inline script that diffs `/metrics` around `kirocrew chat -m "reply with exactly: ok"`.
- **Data**: `harness.jsonl`, `kiro.jsonl` (`label` = `kiro-qwen-8k` before, `kiro-qwen-reorder` after the fix).
- **Result**: Claude Code 3.6 s (API 0.65 s); OpenCode 2.1 s; Kiro `@qwen` 20.7 s with 0 cached tokens out of 47,024.

## E5. Why Kiro misses the cache
- **Run**: `probes/capture_proxy.py` on :8110 with OpenCode's `baseURL` pointed at it for two turns; diff of the two request bodies; `/tokenize` on both; a control with a synthetic 28K prompt changed in the middle vs. at the end; then `REORDER=1`.
- **Data**: request captures are **not** published (they contain the gateway's full system prompt and memory); the numbers are in `kiro.jsonl` and the report.
- **Result**: first differing token 184, inside the OpenCode `bash` tool description (per-session scratch path). Hybrid model checkpoints: middle change → 0 cached; tail change → 28,224 cached. With the volatile tool last: 37,439 identical tokens, 36,848 reused (47 × 784), turn 20.7 → 10.8 s from the third turn on.
- **Side finding**: raising OpenCode's global output limit to 32,768 made the gateway loop on context compaction (36 requests for 2 turns). Global limit restored to 8,192; crewd raises it per process.

## E6. Media models
- **Run**: `probes/media_probe.py` holding the GPU lock, with `gpu_fast.sh` at 4 Hz.
- **Data**: `media.jsonl`, `media.log`, `media-gpu.csv`.
- **Result**: Z-Image 0.55 s/step at 1024²; TTS RTF 0.43–0.58, non-streaming; Wan 121 frames: 244 s denoising at the 575 W power cap, then 81 s near-idle; swaps 36–66 s.

## E7. Collaboration, trial 1
- **Run** (Mac): `collab/run.py claude`, `run.py local`, `run.py codex`; ledgerkit repo initialised on latte; `score.sh`.
- **Result**: Claude 6/6. Both Qwen arms 3/6: in the other 6 jobs Qwen spent 8,192 reasoning tokens in one step and was cut off (`finish_reason: length`). crewd correctly failed them.
- **Scoring fix**: task t6's spec said `finish()` "returns any final row"; Claude returned a row, the tests expected a list of rows. The hidden test was changed to accept both readings before any arm was compared.

## E8. Collaboration, trial 2
- **Change**: crewd's OpenCode output limit 32,768 (per process). Codex plans reused from trial 1 so only the coder side changed.
- **Run**: `TRIAL=2 run.py local; TRIAL=2 run.py codex; ./score.sh`.
- **Data**: `collab/results.jsonl`, `collab/scored.json`, `data/jobs/<id>/` (all logs, plans, reviews), `data/raw/ledger.jsonl`.
- **Result**: 6/6 for both; 70.1 and 53.9 minutes vs. 3.4 for Claude alone. 5 CHANGES in 22 reviews, all reproduced as real bugs. Reviewer findings turned into 4 edge tests (not published) and run on all arms.

## E9. Kernel configurations
- **Run**: `probes/run_kernel.sh`: base; `FI_SAMPLER=1` with a conda CUDA 13.0 toolchain; plus `--attention-backend FLASHINFER`. Each restarts vLLM and runs `kprobe.py`.
- **Failures**: `kprobe.py` first requested a 66K-token prompt (over the 65,536 limit) → 400; sizes reduced. FlashInfer sampler JIT failed to link `-lcudart` until `lib64` was symlinked in the conda toolkit. A restart with `pkill -f run_kernel.sh` over ssh killed the ssh session itself.
- **Data**: `kernel.jsonl`.
- **Result**: all within 0.5%.

## E10. Profiler
- **Run**: last part of `run_kernel.sh`: vLLM with `--profiler-config`, `/start_profile` … `/stop_profile` around one ~20K-token prefill and one 64-token decode.
- **Data**: `data/profiler/{prefill,decode}/rank0.profiler_out.txt` and `trace.pt.trace.json.gz` (open in Perfetto).
- **Result**: decode 11.17 ms/step on the GPU; Marlin INT4 GEMM 72%, bf16 `lm_head` 12.5%, attention 2.6%, linear attention 3.0%, sampling 1.2%. Prefill: 13 chunks of 1,568 tokens, Marlin 85%, FlashAttention 9.5%.

## E11. MTP speculative decoding
- **Run**: `probes/run_spec.sh` (started automatically when E9/E10 finished): base and `--speculative-config {"method":"qwen3_5_mtp","num_speculative_tokens":k}` for k = 1, 2, 3, each with `kprobe2.py` (adds a 1,500-token answer to task t5, with and without reasoning, and acceptance counters). The base run also tokenized the reordered Kiro requests (E5).
- **Data**: `spec.jsonl`, `spec.log`.
- **Result**: k = 3: 77 → 117 tok/s with reasoning (acceptance 52%), 155 tok/s without (≈ 90%); KV cache 139,810 → 78,372 tokens.

## Not yet run (see the paper draft's agenda)
MTP in the full collaboration loop; reasoning budgets; two concurrent coder jobs; quantized `lm_head`; vLLM sleep mode for swaps; streaming TTS; the Wan idle tail; a larger task set with replicates.
