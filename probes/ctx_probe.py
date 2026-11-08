#!/usr/bin/env python3
"""ctx_probe.py <label> <out.jsonl>: long-context checks for one server config.
Needle recall at ~100K tokens, cold prefill time at that size, and decode speed on a real coding answer."""
import json, random, sys, time, urllib.request as u
B = "http://127.0.0.1:8101"; LABEL, OUT = sys.argv[1], sys.argv[2]
def chat(messages, n, think=False, stream=False):
    body = {"model": "qwen3.8", "messages": messages, "max_tokens": n, "temperature": 0.0,
            "chat_template_kwargs": {"enable_thinking": think}}
    t = time.time()
    r = json.loads(u.urlopen(u.Request(B + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=900).read())
    return r, time.time() - t
def rec(**k):
    k["label"] = LABEL; open(OUT, "a").write(json.dumps(k) + "\n"); print(k, flush=True)
words = "ledger cache token bucket stream window offset compile kernel tensor shard replica schedule".split()
random.seed(7)
def filler(n_lines):
    return "\n".join(f"log {i:06d}: " + " ".join(random.choice(words) for _ in range(9)) for i in range(n_lines))
for target_lines, pos in ((6800, 0.3), (6800, 0.8)):   # ~100K tokens
    lines = filler(target_lines).split("\n")
    secret = f"{random.randint(1000,9999)}-{random.choice(words)}"
    lines.insert(int(len(lines) * pos), f"IMPORTANT: the release code is {secret}.")
    msg = [{"role": "user", "content": "\n".join(lines) + "\n\nWhat is the release code? Answer with the code only."}]
    r, secs = chat(msg, 30)
    ans = r["choices"][0]["message"]["content"].strip()
    rec(test="needle", pos=pos, prompt=r["usage"]["prompt_tokens"], secs=round(secs, 1), ok=secret in ans, answer=ans[:40], secret=secret)
TASK = open(__file__.replace("ctx_probe.py", "task_t5.txt")).read()
body = {"model": "qwen3.8", "messages": [{"role": "user", "content": TASK}], "max_tokens": 1200, "ignore_eos": True, "stream": True,
        "temperature": 0.6, "top_p": 0.95, "top_k": 20, "chat_template_kwargs": {"enable_thinking": True}, "stream_options": {"include_usage": True}}
first = last = None; n = 0
for line in u.urlopen(u.Request(B + "/v1/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}), timeout=600):
    if not line.startswith(b"data: ") or line.strip() == b"data: [DONE]": continue
    d = json.loads(line[6:])
    if d.get("usage"): n = d["usage"]["completion_tokens"]
    if d.get("choices") and any(d["choices"][0]["delta"].get(k) for k in ("content", "reasoning", "reasoning_content")):
        now = time.time(); first = first or now; last = now
rec(test="decode", out=n, tok_s=round(n / (last - first), 1))
