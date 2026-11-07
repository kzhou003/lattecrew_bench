# Measurement techniques

Small habits that made the numbers trustworthy.

## Isolate the layer
Measure each layer by going through it and nothing above it: vLLM directly on :8101, then llama-swap on :8100, then the SSH tunnel from the Mac on :18100. The differences between those three medians are the cost of each hop (+1.4 ms for llama-swap, +29 ms for the tunnel).

## Control the cache
- **Force a miss**: start every "cold" prompt with a random uuid. With prefix caching, any shared prefix would otherwise turn a prefill measurement into a cache measurement.
- **Force a hit**: send the identical prompt again immediately.
- **Verify, don't assume**: vLLM's response leaves `usage.prompt_tokens_details.cached_tokens` empty, so read `vllm:prompt_tokens_cached_total` before and after.

## Fix the output length
`ignore_eos: true` with `max_tokens` makes every request produce the same number of tokens, so TPOT and throughput compare across configurations. Use `temperature: 0` for repeatability when sampling is not under test; use the model's recommended `top_p/top_k` when it is (otherwise the top-k/top-p kernel never runs).

## Define the metrics in code
- TTFT = time from sending the request to the first content or reasoning delta.
- TPOT = (last token time − first token time) / (output tokens − 1).
- Also record the p99 gap between tokens to catch stalls.
- Throughput under concurrency = all output tokens / wall time of the batch.

## Cross-check client and server
Every number that matters has two sources that must agree: client TTFT vs. `request_prefill_time_seconds`, client TPOT vs. `request_decode_time_seconds / generated tokens`, OpenCode's token counts vs. vLLM's counters.

## Take the GPU
Experiments that restart servers or load models hold the same `flock` that the bots and crewd use, ask llama-swap to `/unload`, start the server with `setsid`, poll `/health`, and kill the whole process group at the end.

## Split time with event timestamps
OpenCode's JSON events carry millisecond timestamps for each step and each tool call. Model time = step duration − tool time; gap = time between one step's end and the next step's start. Summed over all coder runs this gave the 96 / 0.8 / 3.3 split, without any instrumentation inside the agent.

## Find why a cache misses
1. Capture two real requests with a logging proxy.
2. Compare messages and tools; find the first differing field.
3. Tokenize both with `/tokenize` and find the first differing token (here: 184 of 47,024, inside the `bash` tool description, which embeds a per-session path).
4. Test the hypothesis with a control: on this hybrid model (Gated DeltaNet + attention, `mamba_cache_mode=align`), changing the middle of a 28K prompt gave 0 cached tokens; changing only the end gave 28,224.
5. Fix in the proxy (`REORDER=1`: move volatile tools last) and measure again.

## Bound before you tune
Compute the roofline before trying kernels: bytes of weights read per token (from safetensors headers) / memory bandwidth = 9.3 ms. Measured 13.0 ms means at most ~28% headroom for kernels, and the profiler showed attention and sampling at ~4% of decode. That predicted, correctly, that FlashInfer would not help, and pointed to MTP speculative decoding instead.

## Score blind
Hidden tests stay on the Mac until every job has finished, go to a temp dir on the GPU machine for scoring, and are deleted right after. Each round's commit is recorded (`round_heads`) so round 1 and the final answer are scored separately. Review findings are reproduced before being counted, and turned into extra edge tests run on every arm.

## Pitfalls hit during this study
- `pkill -f <pattern>` over ssh killed the ssh session itself (its command line contained the pattern). Put kills in a script file.
- Raising OpenCode's global output limit to 32K made the Kiro gateway loop on context compaction; the limit must be per process.
- An 8K output limit truncated half the coder runs in a single reasoning step; the first collaboration trial is kept as a reference only.
- FlashInfer JIT compiled but failed to link (`-lcudart`) until a `lib64` symlink was added to the conda CUDA toolkit.
- A desktop browser held ~2 GB of VRAM and made a fixed `--gpu-memory-utilization 0.90` fail; size it from free memory.
