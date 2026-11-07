#!/usr/bin/env python3
"""Cut every chart and diagram out of the generated report into figures/NN-<slug>.svg (light theme, standalone)
and write figures/README.md with each caption. Optional PNGs: pass --png (needs Google Chrome)."""
import html, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "report", "lattecrew-report.html"); OUT = os.path.join(ROOT, "figures")
page = open(SRC).read()
css = re.search(r"<style>(.*?)</style>", page, re.S).group(1)
root = re.search(r":root\{(.*?)\}", css, re.S).group(1)              # light tokens
svg_rules = "\n".join(l for l in css.splitlines() if l.strip().startswith("svg"))
style = f"<style>svg{{{root} font-family:'Noto Sans SC','PingFang SC',sans-serif; background:var(--panel)}}\n{svg_rules}\nsvg .hair{{display:none}}</style>"
figs = re.findall(r"<figure[^>]*>(.*?)</figure>", page, re.S)
os.makedirs(OUT, exist_ok=True)
index = ["# Figures", "", "Every chart and diagram from the report, as standalone light-theme SVG (and PNG). Regenerate with `python3 report/gen.py && python3 tools/extract_figures.py --png`.", ""]
n = 0
for f in figs:
    m = re.search(r"(<svg class=\"chart\".*?</svg>)", f, re.S)
    if not m:
        continue
    n += 1
    svg = m.group(1)
    cap = html.unescape(re.sub(r"<[^>]+>", "", re.search(r"<figcaption>(.*?)</figcaption>", f, re.S).group(1))).strip()
    label = re.search(r'aria-label="([^"]+)"', svg).group(1)
    slug = re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")[:48]
    vb = re.search(r'viewBox="0 0 ([0-9.]+) ([0-9.]+)"', svg)
    w, h = vb.group(1), vb.group(2)
    svg = svg.replace('<svg class="chart"', f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" class="chart"', 1)
    svg = svg.replace(">", ">" + style, 1)
    leg = re.search(r'<div class="legend">(.*?)</div>', f, re.S)
    legend = ", ".join(html.unescape(x) for x in re.findall(r"</i>(.*?)</span>", leg.group(1))) if leg else ""
    name = f"{n:02d}-{slug}"
    open(os.path.join(OUT, name + ".svg"), "w").write(svg)
    index += [f"## {n:02d}. {label}", "", f"![{label}]({name}.svg)", "", cap + (f"  \nLegend: {legend}" if legend else ""), ""]
    if "--png" in sys.argv:
        chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        tmp = os.path.join(OUT, name + ".tmp.html")
        open(tmp, "w").write(f'<html><body style="margin:0;background:#fff">{svg}</body></html>')
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                        f"--window-size={int(float(w))},{int(float(h))}", f"--screenshot={os.path.join(OUT, name + '.png')}", "file://" + tmp],
                       capture_output=True)
        os.remove(tmp)
open(os.path.join(OUT, "README.md"), "w").write("\n".join(index))
print(n, "figures")
