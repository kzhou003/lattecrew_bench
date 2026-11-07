# Report generators

| File | Output |
|---|---|
| `gen.py` | `lattecrew-report.html`: the analysis report (Chinese); every number is computed from `../data` and `../collab` |
| `gen_methods.py` | `lattecrew-methods.html` and `-standalone.html`: how each measurement works, quoting the scripts |
| `charts.py` | inline-SVG bar, stacked bar, line (with crosshair), dot plot, tables; colors from CSS tokens, tooltips via `data-tip` |
| `diagrams.py` | layer stack, prompt-prefix layout, sequence diagram, Gantt timeline |

`lattecrew-report.html` is a page fragment (published as a claude.ai artifact); `lattecrew-report-standalone.html` opens directly in a browser. `../tools/extract_figures.py --png` cuts the figures out into `../figures/`; `../tools/results_md.py` writes `../docs/results.md`.

Chart colors use the dataviz reference categorical palette, validated for color-vision deficiency in light and dark themes.
