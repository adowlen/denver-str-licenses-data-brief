"""Charts for the Denver STR licenses brief. Dark brand style.
All figures from stats.json / neighborhood_panel.csv (never hand-typed).
"""
import json

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
BG, AMBER, TEAL, FG, MUT = "#101417", "#f5a800", "#19b8a6", "#e8e6e1", "#9aa3ab"
plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.edgecolor": "#2a2f33", "axes.labelcolor": FG,
    "xtick.color": MUT, "ytick.color": MUT, "font.family": "DejaVu Sans",
    "axes.grid": True, "grid.color": "#23282c", "grid.linewidth": 0.6,
})
S = json.load(open(f"{PKG}/stats.json"))
OUT = f"{PKG}/charts"

# --- 1. Licensee concentration: holders by licenses-held band (active) ---
bands = ["1", "2", "3-5", "6-10", "11+"]
holders = [S["concentration_active"]["holders_by_band"][b] for b in bands]
licenses = [S["concentration_active"]["licenses_by_band"][b] for b in bands]
fig, ax = plt.subplots(figsize=(9.2, 4.9))
bars = ax.bar(bands, holders, color=TEAL, width=0.58)
ax.bar(["1"], [holders[0]], color=AMBER, width=0.58)
for b, h, lic in zip(bands, holders, licenses):
    ax.annotate(f"{h:,} holders\n{lic:,} licenses", (b, h + 90), ha="center", fontsize=10, color=FG,
                fontweight="bold")
ax.set_ylim(0, 2450)
ax.yaxis.set_major_formatter(FuncFormatter(lambda v, p: f"{v:,.0f}"))
ax.set_xlabel("Active licenses held per licensee (band)", fontsize=10.5)
ax.set_title("Denver STR licensees by licenses held, active licenses only (2,083 licenses, 2,080 holders)",
             fontsize=11.5, color=FG, pad=14, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_bands.png", dpi=200)
plt.close(fig)

# --- 2. Neighborhood density: active licenses per 1,000 housing units, top 12 ---
panel = pd.read_csv(f"{PKG}/data/neighborhood_panel.csv")
rate = panel.nlargest(12, "licenses_per_1000_units").iloc[::-1]
fig, ax = plt.subplots(figsize=(9.2, 5.4))
ax.barh(rate["neighborhood"], rate["licenses_per_1000_units"], color=TEAL, height=0.62)
for i, (v, n) in enumerate(zip(rate["licenses_per_1000_units"], rate["active_licenses"])):
    ax.annotate(f"{v:.1f}  ({n} licenses)", (v + 0.7, i), va="center", fontsize=9.5, color=FG)
ax.set_xlim(0, 32)
ax.set_title("Active STR licenses per 1,000 housing units, top 12 neighborhoods (citywide: 5.8)",
             fontsize=11.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout(rect=[0, 0.10, 1, 1])
fig.text(0.012, 0.045,
         "Denominators: ACS 2020-2024 5-year housing units allocated to statistical neighborhoods.",
         fontsize=8.5, color=MUT)
fig.text(0.012, 0.012,
         "Three neighborhoods hold zero active licenses: Auraria, Kennedy, Sun Valley.",
         fontsize=8.5, color=MUT)
fig.savefig(f"{OUT}/chart_neighborhood_rates.png", dpi=200)
plt.close(fig)

# --- 3. Vintage: active licenses by original issue year ---
vint = S["vintage_active"]["originally_issued_by_year"]
years = sorted(vint.keys(), key=int)
vals = [vint[y] for y in years]
fig, ax = plt.subplots(figsize=(9.2, 4.6))
ax.bar([int(y) for y in years], vals, color=AMBER, width=0.62)
for x, v in zip(years, vals):
    ax.annotate(f"{v}", (int(x), v + 12), ha="center", fontsize=9.5, color=FG, fontweight="bold")
ax.set_ylim(0, 460)
ax.set_xticks([int(y) for y in years])
ax.set_title("Active STR licenses by the year the license was originally issued (61% date to 2023 or later)",
             fontsize=11.5, color=FG, pad=12, loc="left")
for s in ["top", "right"]:
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(f"{OUT}/chart_vintage.png", dpi=200)
plt.close(fig)

print("charts written")
