# lattecrew_bench

Benchmarks, raw data and figures from a full-stack study of [LatteCrew](https://github.com/kzhou003/LatteCrew): a local-first AI team in which Claude Code and Codex plan and review, a local Qwen3.8-27B on one RTX 5090 writes code, and image, speech and video models share the same GPU.

The study asked three questions:

1. **Does the collaboration work?** Codex plans, Qwen codes, Claude reviews, compared with Claude working alone.
2. **Does capability drop or improve?** Measured with hidden tests and with edge tests derived from review findings.
3. **Where is the end-to-end bottleneck?** Measured layer by layer: Slack/Kiro Crew → harness → MCP/SSH → crewd → llama-swap → vLLM/vLLM-Omni → kernels → GPU.

## Main results

| Finding | Number | Figure |
|---|---|---|
| Local coder time spent decoding | 96% (tools 0.8%, gaps 3.3%) | [18](figures/README.md#18-qwen-time-split) |
| Share of decoded tokens that are reasoning | 80% | [19](figures/README.md#19-qwen-generated-tokens) |
| All three arms pass the 175 hidden tests | 6/6 each | [15](figures/README.md#15-wall-time-per-task) |
| Wall time: Claude alone vs. Qwen + Claude vs. Codex + Qwen + Claude | 3.4 / 70.1 / 53.9 min | [15](figures/README.md#15-wall-time-per-task) |
| Claude cost (API-equivalent): same three arms | $0.80 / $0.94 / $1.03 | [16](figures/README.md#16-claude-cost-per-task) |
| Daylight-saving edge tests (reviewer-derived) | Claude alone 0/2, Qwen + Claude 1/2, with Codex plan 2/2 | – |
| Kiro `@qwen` turn, before → after moving a volatile tool definition last | 20.7 s → 10.8 s | [04](figures/README.md#04-kiro-prompt-prefix-that-vllm-can-reuse) |
| Cold vs. cached TTFT at 65K tokens | 20.7 s vs. 0.30 s | [05](figures/README.md#05-ttft-vs-prompt-length) |
| Decode vs. memory-bandwidth bound | 13.0 ms vs. 9.3 ms/token (Marlin GEMMs at 84% of peak) | [08](figures/README.md#08-gpu-kernel-time-decode) |
| FlashInfer sampler / attention | < 0.5% change | – |
| MTP speculative decoding, k = 3, coding answer | 77 → 117 tok/s with reasoning, → 155 without | [09](figures/README.md#09-mtp-decode-speed) |
| Model swap cost | 36–66 s per model | [10](figures/README.md#10-model-swap-cost) |
| Wan 5 s video: idle GPU after denoising | 81 s | [12](figures/README.md#12-wan-gpu-utilization) |

Full analysis (Chinese, interactive charts): download and open [`report/lattecrew-report-standalone.html`](report/lattecrew-report-standalone.html). How each number was measured, with the code quoted: [`report/lattecrew-methods-standalone.html`](report/lattecrew-methods-standalone.html).

## Layout

| Path | Contents |
|---|---|
| [`probes/`](probes/) | one script per layer; see [docs/experiments.md](docs/experiments.md) for how each was run |
| [`collab/`](collab/) | the collaboration benchmark: tasks, starting repo, reference solutions, driver, scorer, results |
| [`data/`](data/) | every raw result: JSON lines, GPU traces, profiler tables and traces, job logs. Schemas in [data/README.md](data/README.md) |
| [`report/`](report/) | generators for the analysis report and the methods page; small chart and diagram libraries |
| [`figures/`](figures/) | all 20 figures as standalone SVG and PNG, with captions |
| [`tools/`](tools/) | `extract_figures.py` |
| [`docs/`](docs/) | [experiments](docs/experiments.md) (what was run, in order, including what went wrong), [tools](docs/tools.md), [techniques](docs/techniques.md), [results](docs/results.md) |

## Reproduce

Hardware and software: RTX 5090 32 GB, Ubuntu 24.04, torch 2.13 + CUDA 13.0, vLLM 0.32.0, vLLM-Omni 0.32.0, Qwen3.8-27B AWQ INT4; a Mac with Claude Code, Codex CLI and Kiro Crew. Set up the system with [LatteCrew](https://github.com/kzhou003/LatteCrew), then:

```bash
# on the GPU machine
python3 probes/llm_probe.py http://127.0.0.1:8101 data/raw/llm-grid.jsonl grid --metrics http://127.0.0.1:8101/metrics
python3 probes/harness_probe.py
bash probes/run_kernel.sh && bash probes/run_spec.sh
python3 probes/media_probe.py
# on the Mac
python3 probes/stack_probe.py data/raw/stack.jsonl
cd collab && python3 run.py claude && python3 run.py local && python3 run.py codex && ./score.sh
# anywhere
python3 report/gen.py && python3 report/gen_methods.py && python3 tools/extract_figures.py --png
```

The probes write to `~/latte-bench/out/` on the GPU machine; copy results into `data/raw/` before generating.

**Hidden tests are not published.** The 175 hidden test cases and the 4 reviewer-derived edge tests stay off this repo so that agents working in a clone cannot read them. `collab/scored.json` holds their results. To rerun scoring, write your own tests per task in `collab/tasks.json`, validate them against `collab/ref/`, and put them in `collab/hidden/test_t<N>.py`.

## Caveats

One run per arm and task in the collaboration experiment, six small tasks, one machine. Claude cost is the API-equivalent reported by Claude Code, used against a subscription. See the limits section of the report.

## License

Code: MIT. Data and figures: CC BY 4.0.
