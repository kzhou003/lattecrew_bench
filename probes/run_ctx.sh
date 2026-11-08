#!/usr/bin/env bash
# Long-context configs for claude-qwen. Holds the GPU lock; leaves the server stopped (llama-swap restarts it on demand).
cd ~/latte-bench; exec 9>>~/latte-models/gpu.lock; flock 9
OUT=out/ctx.jsonl; rm -f $OUT out/ctx.log
curl -s -m 30 "http://127.0.0.1:8100/unload" > /dev/null; sleep 5
up(){ for i in $(seq 1 120); do curl -sf -m 2 http://127.0.0.1:8101/health > /dev/null && return 0; kill -0 $1 2>/dev/null || return 1; sleep 5; done; return 1; }
run(){ local label=$1; shift
  echo "== $label $(date +%T)" >> out/ctx.log
  env "$@" setsid ~/latte-models/bin/serve-qwen.sh & local p=$!
  if up $p; then grep -E "KV cache size|qwen start" ~/latte-models/logs/qwen.log | tail -2 >> out/ctx.log; python3 ctx_probe.py $label $OUT >> out/ctx.log 2>&1
  else echo "$label FAILED" >> out/ctx.log; grep -iE "error|larger than|KV cache" ~/latte-models/logs/qwen.log | tail -4 >> out/ctx.log; fi
  kill -- -$p 2>/dev/null; sleep 3; pkill -f "vllm serve"; sleep 10
}
C13=$HOME/latte-models/cuda13
run fp8-128k CTX=131072 CUDA_HOME=$C13 PATH=$C13/bin:$PATH 'EXTRA=--kv-cache-dtype fp8'
run fp8-128k-mtp3 CUDA_HOME=$C13 PATH=$C13/bin:$PATH CTX=131072 'EXTRA=--kv-cache-dtype fp8 --speculative-config {"method":"qwen3_5_mtp","num_speculative_tokens":3}'
run bf16-96k CTX=98304
echo FINISHED > out/ctx.done
