# Figures

Every chart and diagram from the report, as standalone light-theme SVG (and PNG). Regenerate with `python3 report/gen.py && python3 tools/extract_figures.py --png`.

## 01. LatteCrew request path with measured latency per layer

![LatteCrew request path with measured latency per layer](01-lattecrew-request-path-with-measured-latency-per.svg)

图 1：一条请求经过的各层，以及每层实测的延迟。悬停查看详情。下文每一节对应其中一层。

## 02. Connection layer latency

![Connection layer latency](02-connection-layer-latency.svg)

图 2：连接层各操作的中位延迟（毫秒）。蓝色是已经在用的方式，黄色是要避免的方式。  
Legend: 当前做法, 应避免的做法

## 03. Agent fixed overhead

![Agent fixed overhead](03-agent-fixed-overhead.svg)

图 3：一句话回复的耗时拆分（秒）。Claude Code 的模型时间是 API 耗时；Kiro 的模型时间是 vLLM 记录的预填充时间。OpenCode 的事件流不给 API 耗时，只画总长。  
Legend: 模型时间, 其余开销

## 04. Kiro prompt prefix that vLLM can reuse

![Kiro prompt prefix that vLLM can reuse](04-kiro-prompt-prefix-that-vllm-can-reuse.svg)

图 4：Kiro qwen 网关的提示里，vLLM 能复用的部分。蓝色可复用，橙色是每轮都变的 bash 工具描述，灰色每轮重算。工具重排后，前 37,439 个 token 每轮相同，vLLM 按 784 的块对齐复用其中 36,848 个。  
Legend: 可复用前缀, 每轮会变的工具描述, 每轮重算

## 05. TTFT vs prompt length

![TTFT vs prompt length](05-ttft-vs-prompt-length.svg)

图 5：首 token 延迟和提示长度。冷启动时预填充约 3,549 tok/s，近似线性；命中缓存时几乎是常数。  
Legend: 冷启动, 命中缓存

## 06. TPOT vs context

![TPOT vs context](06-tpot-vs-context.svg)

图 6：解码速度和上下文长度。上下文越长，每步要读的 KV 越多，TPOT 从 12.8 ms 涨到 15.4 ms。

## 07. GPU kernel time prefill

![GPU kernel time prefill](07-gpu-kernel-time-prefill.svg)

图 7：预填充（约 2 万 token 的提示）时各类 kernel 占 GPU 时间的比例（torch profiler，Self CUDA）。

## 08. GPU kernel time decode

![GPU kernel time decode](08-gpu-kernel-time-decode.svg)

图 8：解码（64 个 token）时各类 kernel 占 GPU 时间的比例（torch profiler，Self CUDA）。

## 09. MTP decode speed

![MTP decode speed](09-mtp-decode-speed.svg)

图 9：单个请求的解码速度（tok/s），t5 题目的真实回答，1,500 个 token，每格 2–3 次的中位数。  
Legend: 开思考, 不开思考

## 10. Model swap cost

![Model swap cost](10-model-swap-cost.svg)

图 10：切换到某个模型的代价（秒），即首个请求比之后的请求多花的时间。包括停掉上一个模型、加载权重、torch.compile 和 CUDA graph 捕获。

## 11. Z-Image latency

![Z-Image latency](11-z-image-latency.svg)

图 11：Z-Image 生成一张图的时间。每步约 0.55 秒（1024²），时间和步数、像素数都近似线性。  
Legend: 改变步数, 改变分辨率

## 12. Wan GPU utilization

![Wan GPU utilization](12-wan-gpu-utilization.svg)

图 12a：生成 5 秒视频（121 帧、30 步）时 GPU 的利用率，每 2 秒一个点。

## 13. Wan GPU power

![Wan GPU power](13-wan-gpu-power.svg)

图 12b：同一次生成的功耗。去噪阶段一直顶在 575 W 的功耗上限，SM 时钟被压到约 2520 MHz（最高 3,090 MHz）。

## 14. Who passes what to whom in one collaborative task

![Who passes what to whom in one collaborative task](14-who-passes-what-to-whom-in-one-collaborative-tas.svg)

图 13：一道题的完整流程。每条箭头是一次实际传递的内容和它的大小。审查者故意看不到作者的自述，只看任务和 diff，自己跑测试。

## 15. Wall time per task

![Wall time per task](15-wall-time-per-task.svg)

图 14：每道题的总耗时（对数坐标）。Claude 单独 24–43 秒；有 Qwen 参与的方式 1–39 分钟。  
Legend: Claude 单独, Qwen + Claude 审查, Codex 规划 + Qwen + Claude 审查

## 16. Claude cost per task

![Claude cost per task](16-claude-cost-per-task.svg)

图 15：每道题消耗的 Claude 额度（按 API 价格折算，美元）。一次审查约 $0.10，和 Claude 直接写完一道小题差不多。  
Legend: Claude 单独, Qwen + Claude 审查, Codex 规划 + Qwen + Claude 审查

## 17. Timeline of two runs of task t4

![Timeline of two runs of task t4](17-timeline-of-two-runs-of-task-t4.svg)

图 16：t4 两次运行的时间线。每个色块是 Qwen 的一步（一次模型调用加它触发的工具）。橙色是思考超过 1,000 token 的步骤，黄色是动作步骤。审查条按账本记录的时长放置。  
Legend: Codex 规划, Qwen 思考步骤, Qwen 动作步骤, Claude 审查

## 18. Qwen time split

![Qwen time split](18-qwen-time-split.svg)

图 17a：所有 Qwen 作业的时间拆分。模型生成 95.9%，工具执行 0.8%，步间间隔 3.3%。  
Legend: 模型生成, 工具执行, 步间间隔

## 19. Qwen generated tokens

![Qwen generated tokens](19-qwen-generated-tokens.svg)

图 17b：Qwen 生成的 534K 个 token 中，80% 是思考。  
Legend: 思考, 输出

## 20. Where the time goes

![Where the time goes](20-where-the-time-goes.svg)

图 18：协作实验的时间分布（两种协作方式、第二轮、12 次作业合计，加上同一批作业的审查和规划）。  
Legend: Qwen 生成, Claude, Codex, 其余
