#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MS-499 Term Paper - Marine Fish Marketing System, Chattogram (March 2026)
PUBLICATION FIGURE SUITE (v2)
=================================

Style specification (applied to every figure):
  * Typography      : Times New Roman (rendered with Tinos, the
                      metrically identical open substitute; R/ggplot2 on
                      Windows uses the real Times New Roman).
  * Resolution      : 1000 dpi PNG.
  * Title           : top centre, bold, extra padding above the axes.
  * Legend          : bottom centre, OUTSIDE the plot area, extra
                      breathing space below the axes.
  * Axes            : full X and Y axis titles with complete parameter
                      names (e.g. "Marketing margin (BDT per kilogram)").
  * Grid            : major grid lines (solid, light grey) plus minor
                      sub-grid lines (dotted, lighter).
  * Value labels    : printed on the data wherever they fit without
                      overlapping any other text; label collision is
                      avoided by construction (staggered offsets, leader
                      lines, or direct labelling instead of legends).

Figure set (main text, 8 figures):
  F1  Average Marketing Margin by Chain Intermediary        (bar chart)
  F2  Distribution of Retail Selling Prices by Species      (box plot)
  F3  Average Price Progression along the Marketing Chain   (line chart)
  F4  Decomposition of the Average Consumer Price           (donut chart)
  F5  Payment Method Composition by Market Actor            (stacked bar)
  F6  Market Infrastructure Quality Profile                 (radar chart)
  F7  Most Frequently Reported Marketing Problems           (rose chart)
  F8  Average Retail Selling Price by Market                (bar chart)
Appendix (2 figures):
  A1  Daily Trading Capacity by Actor Group                 (box plot, log)
  A2  Producer Share of the Consumer Price by Species       (horizontal bar)

Run:
    python scripts/make_charts_v2.py                # after run_analysis.py
    python scripts/make_charts_v2.py --data <xlsx>
Outputs -> analysis_outputs/charts_v2/  (F*.png, A*.png, FIGURE_INDEX.csv)

The legacy working charts (analysis_outputs/charts/C1-C8) remain untouched;
this suite is the publication set referenced by docs/WRITING_GUIDE.md.
"""
import argparse
import os
import sys
import textwrap
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_analysis import (load_data, find_default_data, num, MAUND,
                          LANDING_MARKETS, MIN_CONS,
                          C_PRODUCER, C_ARATDAR, C_BEPARI, C_RETAIL,
                          C_CONSUMER)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CH2 = os.path.join(ROOT, "analysis_outputs", "charts_v2")

# ---------------------------------------------------------------------------
# Typography: Times New Roman via Liberation Serif (metric-compatible
# replacement: identical glyph advance widths, so the layout is unchanged
# when the real Times New Roman renders the same figure elsewhere, e.g.
# in the R/ggplot2 pipeline on Windows).
# ---------------------------------------------------------------------------
for _f in ("LiberationSerif-Regular.ttf", "LiberationSerif-Bold.ttf",
           "LiberationSerif-Italic.ttf", "LiberationSerif-BoldItalic.ttf"):
    _p = f"/usr/share/fonts/truetype/liberation/{_f}"
    if os.path.exists(_p):
        fm.fontManager.addfont(_p)
fm.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "figure.dpi": 100, "savefig.dpi": 1000,
    "font.size": 11.5,
    "axes.titlesize": 15, "axes.titleweight": "bold", "axes.titlepad": 16,
    "axes.labelsize": 12.5, "axes.labelpad": 11,
    "xtick.labelsize": 10.5, "ytick.labelsize": 10.5,
    "xtick.direction": "out", "ytick.direction": "out",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.9,
    "legend.frameon": False, "legend.fontsize": 10.5,
    "legend.handlelength": 1.6, "legend.columnspacing": 1.4,
})

GRID_MAJOR = dict(which="major", color="#c8cdd3", lw=0.7, alpha=0.95,
                  linestyle="-")
GRID_MINOR = dict(which="minor", color="#e4e7ea", lw=0.5, alpha=0.9,
                  linestyle=":")

TOL6 = ["#0077BB", "#33BBEE", "#009988", "#EE7733", "#CC3311", "#EE3377"]
SLATE = "#4C5468"          # totals / reference
BARBLUE = "#5B7DA3"        # single-series bars
BOXFILL = "#DCE4EE"        # box interiors
EDGE = "#33415C"           # box / bar edges


def style_axis(ax):
    """Major grid + minor sub-grid, drawn below the data."""
    ax.minorticks_on()
    ax.grid(True, **GRID_MAJOR)
    ax.grid(True, **GRID_MINOR)
    ax.set_axisbelow(True)


def save(fig, fname, w=9.0, h=6.4):
    fig.set_size_inches(w, h)
    out = os.path.join(CH2, fname)
    fig.savefig(out, dpi=1000)
    plt.close(fig)
    print(f"  figure  {fname}  ({os.path.getsize(out)/1e6:.1f} MB)")


# ---------------------------------------------------------------------------
# Data blocks shared by several figures
# ---------------------------------------------------------------------------
def chain_species_stats(d):
    """Per-species chain means (run_analysis Table-3 conventions:
    producer/aratdar at landing markets; chain-complete additionally
    requires >= MIN_CONS consumer-paid quotes)."""
    po = d["PO"]
    cpf_yes = [r for r in d["CPF"] if r.get("Purchased_today") == "Yes"]

    def mean_of(code, actor, field, markets=None):
        vals = [r[field] for r in po
                if r.get("Species_code") == code
                and r.get("Actor_type") == actor and r[field] is not None
                and (markets is None or r.get("Market") in markets)]
        return round(float(np.mean(vals)), 2) if vals else None

    rows = {}
    for code in sorted(d["SP"]):
        cons_v = [r["price_kg"] for r in cpf_yes
                  if r.get("Species_code") == code and r["price_kg"] is not None]
        prod = mean_of(code, "Aratdar", "buy_kg", LANDING_MARKETS)
        arat = mean_of(code, "Aratdar", "sell_kg", LANDING_MARKETS)
        bep = mean_of(code, "Bepari_Faria", "sell_kg")
        cons = round(float(np.mean(cons_v)), 2) if cons_v else None
        rows[code] = {"producer": prod, "aratdar": arat, "bepari": bep,
                      "consumer": cons, "consumer_n": len(cons_v),
                      "complete": (None not in (prod, arat, bep, cons)
                                   and len(cons_v) >= MIN_CONS)}
    return rows


def pooled_chain(chain):
    """Unweighted mean of species means over chain-complete species."""
    full = [v for v in chain.values() if v["complete"]]
    out = {k: round(float(np.mean([v[k] for v in full])), 2)
           for k in ("producer", "aratdar", "bepari", "consumer")}
    out["n_species"] = len(full)
    return out


# ---------------------------------------------------------------------------
# F1 - Average marketing margin by chain intermediary (bar chart)
# ---------------------------------------------------------------------------
def fig1_margin_bar(d):
    chain = chain_species_stats(d)
    p = pooled_chain(chain)
    cons = p["consumer"]
    labels = ["Aratdar\n(auction)", "Bepari/Faria\n(wholesale)",
              "Retailer\n(retail)", "Total marketing\nspread"]
    vals = [p["aratdar"] - p["producer"], p["bepari"] - p["aratdar"],
            cons - p["bepari"], cons - p["producer"]]
    pcts = [100.0 * v / cons for v in vals]
    colors = [C_ARATDAR, C_BEPARI, C_RETAIL, SLATE]

    fig, ax = plt.subplots(constrained_layout=True)
    x = np.arange(len(vals))
    bars = ax.bar(x, vals, width=0.58, color=colors, edgecolor=EDGE,
                  linewidth=0.8, zorder=3)
    for xi, (v, pc) in enumerate(zip(vals, pcts)):
        ax.text(xi, v + max(vals) * 0.025, f"{v:,.1f}",
                ha="center", va="bottom", fontsize=12, fontweight="bold",
                color="#1a1a1a")
        ax.text(xi, v + max(vals) * 0.085, f"({pc:.1f}% of consumer price)",
                ha="center", va="bottom", fontsize=9.5, color="#555f6e")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(vals) * 1.22)
    ax.yaxis.set_major_locator(MultipleLocator(50))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_xlabel("Marketing chain intermediary")
    ax.set_ylabel("Marketing margin (BDT per kilogram)")
    ax.set_title(f"Average Marketing Margin by Chain Intermediary\n"
                 f"(mean of {p['n_species']} chain-complete species, March 2026)",
                 loc="center")
    style_axis(ax)
    save(fig, "F1_margin_by_intermediary.png", 9.2, 6.6)


# ---------------------------------------------------------------------------
# F2 - Distribution of retail selling prices by species (box plot)
# ---------------------------------------------------------------------------
def fig2_price_box(d):
    po = d["PO"]
    data, names, ns = [], [], []
    for code in sorted(d["SP"]):
        vals = [r["sell_kg"] for r in po
                if r["Species_code"] == code and r["Actor_type"] == "Khuchra"
                and r["sell_kg"] is not None]
        if len(vals) >= 5:
            data.append(vals)
            names.append(f"{d['SP'][code]['Local_name']}\n(n = {len(vals)})")
            ns.append(len(vals))
    order = np.argsort([np.median(v) for v in data])[::-1]
    data = [data[i] for i in order]
    names = [names[i] for i in order]

    fig, ax = plt.subplots(constrained_layout=True)
    bp = ax.boxplot(data, patch_artist=True, widths=0.55, zorder=3,
                    medianprops=dict(color="#B4472A", lw=1.6),
                    boxprops=dict(facecolor=BOXFILL, edgecolor=EDGE, lw=0.9),
                    whiskerprops=dict(color=EDGE, lw=0.9),
                    capprops=dict(color=EDGE, lw=0.9),
                    flierprops=dict(marker="o", markersize=4.5,
                                    markerfacecolor="#9AA7B8",
                                    markeredgecolor="none", alpha=0.85))
    for i, vals in enumerate(data):
        med = float(np.median(vals))
        ax.text(i + 1, med, f"{med:,.0f}", ha="center", va="center",
                fontsize=8.8, color="#B4472A", fontweight="bold", zorder=5,
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.88, pad=1.1))
    ax.set_xticks(range(1, len(data) + 1))
    ax.set_xticklabels(names, fontsize=9.8)
    ax.set_xlabel("Species (local name; n = number of retail sell quotes)")
    ax.set_ylabel("Retail selling price (BDT per kilogram)")
    ax.set_ylim(0, max(max(v) for v in data) * 1.12)
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_title("Distribution of Retail Selling Prices by Species\n"
                 "(boxes: median and interquartile range; dots: Tukey outliers)",
                 loc="center")
    style_axis(ax)
    save(fig, "F2_retail_price_boxplot.png", 10.2, 6.8)


# ---------------------------------------------------------------------------
# F3 - Price progression along the marketing chain (line chart)
# ---------------------------------------------------------------------------
def fig3_chain_line(d):
    chain = chain_species_stats(d)
    picks = ["S01", "S02", "S05", "S09"]
    stages = ["Producer\n(fisher first sale)", "Aratdar\n(auction hammer)",
              "Bepari/Faria\n(wholesale)", "Retailer\n(vendor quote)",
              "Consumer\n(price paid)"]
    offsets = {"S01": -14, "S02": 14, "S05": 14, "S09": -14}

    fig, ax = plt.subplots(constrained_layout=True)
    for code, col in zip(picks, [TOL6[0], TOL6[3], TOL6[2], TOL6[5]]):
        v = chain[code]
        ys = [v["producer"], v["aratdar"], v["bepari"],
              _retail_quote(d, code), v["consumer"]]
        ax.plot(range(5), ys, marker="o", markersize=6, lw=1.8, color=col,
                label=f"{d['SP'][code]['Local_name']} "
                      f"({d['SP'][code]['English_common_name']})", zorder=3)
        for xi, y in enumerate(ys):
            va = "bottom" if offsets[code] > 0 else "top"
            ax.annotate(f"{y:,.0f}", (xi, y), textcoords="offset points",
                        xytext=(0, offsets[code]), ha="center", va=va,
                        fontsize=9.2, color=col)
    ax.set_xticks(range(5))
    ax.set_xticklabels(stages, fontsize=10.2)
    ax.set_xlabel("Marketing chain stage")
    ax.set_ylabel("Average price (BDT per kilogram)")
    ax.set_ylim(0, max(chain[c]["consumer"] for c in picks) * 1.15)
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_title("Average Price Progression along the Marketing Chain\n"
                 "(four representative species, March 2026)", loc="center")
    style_axis(ax)
    fig.legend(loc="outside lower center", ncol=2)
    save(fig, "F3_price_chain_progression.png", 9.4, 6.9)


def _retail_quote(d, code):
    po = d["PO"]
    vals = [r["sell_kg"] for r in po
            if r["Species_code"] == code and r["Actor_type"] == "Khuchra"
            and r["sell_kg"] is not None]
    return round(float(np.mean(vals)), 2) if vals else None


# ---------------------------------------------------------------------------
# F4 - Decomposition of the consumer price (donut chart)
# ---------------------------------------------------------------------------
def fig4_price_donut(d):
    chain = chain_species_stats(d)
    p = pooled_chain(chain)
    cons = p["consumer"]
    vals = [100.0 * p["producer"] / cons,
            100.0 * (p["bepari"] - p["aratdar"]) / cons,
            100.0 * (cons - p["bepari"]) / cons,
            100.0 * (p["aratdar"] - p["producer"]) / cons]
    bdt = [p["producer"], p["bepari"] - p["aratdar"],
           cons - p["bepari"], p["aratdar"] - p["producer"]]
    labels = ["Producer (fisher) share", "Bepari/Faria margin",
              "Retailer margin", "Aratdar margin"]
    colors = [C_PRODUCER, C_BEPARI, C_RETAIL, C_ARATDAR]

    fig, ax = plt.subplots(constrained_layout=True)
    wedges, _ = ax.pie(vals, colors=colors, startangle=90, counterclock=False,
                       wedgeprops=dict(width=0.42, edgecolor="white",
                                       linewidth=1.5))
    for w, lab, pct, bd in zip(wedges, labels, vals, bdt):
        ang = np.deg2rad((w.theta1 + w.theta2) / 2)
        x, y = np.cos(ang), np.sin(ang)
        ha = "left" if x >= 0 else "right"
        ax.annotate(f"{lab}\n{pct:.1f}%  ({bd:,.1f} BDT/kg)",
                    xy=(0.99 * x, 0.99 * y), xytext=(1.32 * x, 1.32 * y),
                    ha=ha, va="center", fontsize=11,
                    arrowprops=dict(arrowstyle="-", color="#8a93a3", lw=0.9,
                                    connectionstyle="arc3,rad=0"))
    ax.text(0, 0.07, "Consumer price", ha="center", va="center",
            fontsize=12.5, fontweight="bold")
    ax.text(0, -0.10, f"{cons:,.1f}\nBDT per kilogram", ha="center",
            va="center", fontsize=11.5)
    # widen axes limits so the outside labels are never clipped
    ax.set_xlim(-1.95, 1.95)
    ax.set_ylim(-1.75, 1.75)
    ax.set_title("Decomposition of the Average Consumer Price\n"
                 f"(mean of {p['n_species']} chain-complete species, March 2026)",
                 loc="center", pad=20)
    save(fig, "F4_consumer_price_decomposition.png", 8.6, 8.0)

# ---------------------------------------------------------------------------
# F5 - Payment method composition by market actor (stacked bar)
# ---------------------------------------------------------------------------
def fig5_payment_stack(d):
    groups, cash, mfs, credit = [], [], [], []
    for label, rs in (("Aratdar", d["A"]), ("Bepari/Faria", d["B"]),
                      ("Retailer", d["R"])):
        groups.append(label)
        cash.append(float(np.mean([num(r["Payment_cash_pct"]) for r in rs
                                   if num(r["Payment_cash_pct"]) is not None])))
        mfs.append(float(np.mean([num(r["Payment_MFS_pct"]) for r in rs
                                  if num(r["Payment_MFS_pct"]) is not None])))
        credit.append(float(np.mean([num(r["Payment_credit_pct"]) for r in rs
                                     if num(r["Payment_credit_pct"]) is not
                                     None])))
    # consumer: bKash + Nagad pooled into MFS
    pm = Counter(r.get("Payment_method") for r in d["C"])
    n_c = len(d["C"])
    groups.append("Consumer")
    cash.append(100.0 * (pm.get("Cash", 0)) / n_c)
    mfs.append(100.0 * (pm.get("bKash", 0) + pm.get("Nagad_app", 0)) / n_c)
    credit.append(100.0 * (pm.get("Credit", 0)) / n_c)

    y = np.arange(len(groups))[::-1]
    fig, ax = plt.subplots(constrained_layout=True)
    left = np.zeros(len(groups))
    for vals, col, lab in ((cash, "#8FA9C4", "Cash"),
                           (mfs, C_ARATDAR,
                            "Mobile financial services (bKash/Nagad)"),
                           (credit, "#B4472A", "Credit")):
        ax.barh(y, vals, left=left, height=0.55, color=col,
                edgecolor=EDGE, linewidth=0.7, label=lab, zorder=3)
        for yi, v, lf in zip(y, vals, left):
            if v >= 6.0:
                ax.text(lf + v / 2, yi, f"{v:.1f}%", ha="center",
                        va="center", fontsize=10, color="white",
                        fontweight="bold")
        left += np.asarray(vals)
    ax.set_yticks(y)
    ax.set_yticklabels(groups)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_locator(MultipleLocator(20))
    ax.xaxis.set_minor_locator(AutoMinorLocator(4))
    ax.set_xlabel("Share of transactions (%)")
    ax.set_ylabel("Market actor")
    ax.set_title("Payment Method Composition by Market Actor\n"
                 "(traders: mean share of receipts; consumers: last purchase)",
                 loc="center")
    style_axis(ax)
    fig.legend(loc="outside lower center", ncol=3)
    save(fig, "F5_payment_method_mix.png", 9.2, 6.2)


# ---------------------------------------------------------------------------
# F6 - Market infrastructure quality profile (radar chart)
# ---------------------------------------------------------------------------
FACILITY_DIMS = [("Transport_access", "Transport\naccess"),
                 ("Platform", "Trading\nplatform"),
                 ("Roofing", "Roofing"),
                 ("Drainage", "Drainage"),
                 ("Electricity", "Electricity\nsupply"),
                 ("Sanitation", "Sanitation"),
                 ("Water_supply", "Water\nsupply")]
FACILITY_SCORE = {"Good": 3, "Complete": 3, "Regular": 3, "Available": 3,
                  "Medium": 2, "Partial": 1, "Poor": 1, "Irregular": 1,
                  "None": 0}


def fig6_infra_radar(d):
    mk = {r["Market"]: r for r in d["M"]}
    picks = [("M1", "Fishery Ghat (M1, landing)"),
             ("M4", "Karnaphuli Complex (M4, retail)"),
             ("M6", "Patenga (M6, landing)")]
    cols = [TOL6[0], TOL6[3], TOL6[2]]
    n = len(FACILITY_DIMS)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True),
                           constrained_layout=True)
    for (mcode, mlabel), col in zip(picks, cols):
        scores = [FACILITY_SCORE.get(str(mk[mcode].get(k)), np.nan)
                  for k, _ in FACILITY_DIMS]
        scores += scores[:1]
        ax.plot(angles, scores, lw=1.9, color=col, label=mlabel, zorder=3)
        ax.fill(angles, scores, color=col, alpha=0.25, zorder=2)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([lab for _, lab in FACILITY_DIMS], fontsize=11)
    ax.set_rlim(0, 3.4)
    ax.set_rgrids([1, 2, 3], angle=13, fontsize=9.5, color="#667")
    ax.grid(color="#c8cdd3", lw=0.7, alpha=0.9)
    ax.spines["polar"].set_color("#c8cdd3")
    ax.set_title("Market Infrastructure Quality across Facility Dimensions\n"
                 "(score: 1 = poor / partial / irregular, 2 = medium, "
                 "3 = good / complete / regular)", loc="center", pad=26)
    fig.legend(loc="outside lower center", ncol=2)
    save(fig, "F6_infrastructure_radar.png", 8.4, 8.2)


# ---------------------------------------------------------------------------
# F7 - Most frequently reported marketing problems (rose chart)
# ---------------------------------------------------------------------------
def fig7_problems_rose(d):
    cnt = Counter()
    for key in ("A", "B", "R"):
        for r in d[key]:
            for c in ("Problem_1", "Problem_2", "Problem_3"):
                v = r.get(c)
                if v not in (None, ""):
                    cnt[str(v).replace("_", " ")] += 1
    top = cnt.most_common(10)
    n_traders = len(d["A"]) + len(d["B"]) + len(d["R"])
    labels = [k for k, _ in top]
    vals = np.array([v for _, v in top], dtype=float)
    total = vals.sum()
    radius = np.sqrt(vals)          # sector AREA proportional to frequency
    rmax = radius.max()

    n = len(vals)
    width = 2 * np.pi / n
    theta = [i * width for i in range(n)]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True),
                           constrained_layout=True)
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    for i, (th, r, v, lab) in enumerate(zip(theta, radius, vals, labels)):
        col = "#C4835B" if i == 0 else "#8EA9C8"
        ax.bar(th, r, width=width * 0.96, bottom=0, color=col,
               edgecolor="white", linewidth=1.2, zorder=3)
        mid = th + width / 2
        ax.text(mid, r * 0.78, f"{int(v)}", ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#22282f")
        deg = np.rad2deg(mid)
        wrapped = "\n".join(textwrap.wrap(lab, 18))
        rot = deg
        if 90 < deg < 270:
            rot = deg + 180
            ha = "right"
        else:
            ha = "left"
        ax.text(mid, rmax * 1.16, f"{wrapped}\n({100.0*v/total:.1f}% of mentions)",
                ha=ha, va="center", rotation=rot, rotation_mode="anchor",
                fontsize=9.2, color="#333940")
    ax.set_ylim(0, rmax * 1.62)
    ax.set_xticks([])
    ax.grid(color="#dfe3e8", lw=0.6, alpha=0.9)
    ax.spines["polar"].set_visible(False)
    ax.set_title("Most Frequently Reported Marketing Problems\n"
                 f"(top 10; {int(total)} mentions by {n_traders} traders; "
                 "sector area proportional to frequency)",
                 loc="center", pad=24)
    save(fig, "F7_problems_rose.png", 9.6, 8.6)


# ---------------------------------------------------------------------------
# F8 - Average retail selling price by market (bar chart)
# ---------------------------------------------------------------------------
def fig8_market_price_bar(d):
    po = d["PO"]
    means, labels = [], []
    for m in ("M1", "M2", "M3", "M4", "M5", "M6"):
        sp_means = {}
        for code in sorted(d["SP"]):
            vals = [r["sell_kg"] for r in po
                    if r["Species_code"] == code and r["Actor_type"] == "Khuchra"
                    and r["Market"] == m and r["sell_kg"] is not None]
            if vals:
                sp_means[code] = float(np.mean(vals))
        means.append(float(np.mean(list(sp_means.values()))))
        labels.append(f"{d['MK'][m]}\n({len(sp_means)} species)")

    fig, ax = plt.subplots(constrained_layout=True)
    x = np.arange(len(means))
    ax.bar(x, means, width=0.6, color=BARBLUE, edgecolor=EDGE,
           linewidth=0.8, zorder=3)
    for xi, v in zip(x, means):
        ax.text(xi, v + max(means) * 0.025, f"{v:,.1f}", ha="center",
                va="bottom", fontsize=11.5, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10)
    ax.set_ylim(0, max(means) * 1.2)
    ax.yaxis.set_major_locator(MultipleLocator(200))
    ax.yaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_xlabel("Market (number of species with retail quotes)")
    ax.set_ylabel("Average retail selling price (BDT per kilogram)")
    ax.set_title("Average Retail Selling Price by Market\n"
                 "(unweighted mean of species-level mean quotes, March 2026)",
                 loc="center")
    style_axis(ax)
    save(fig, "F8_retail_price_by_market.png", 9.2, 6.4)


# ---------------------------------------------------------------------------
# A1 - Daily trading capacity by actor group (box plot, log scale) [appendix]
# ---------------------------------------------------------------------------
def figa1_capacity_box(d):
    data, names = [], []
    for label, rs in (("Aratdar", d["A"]), ("Bepari/Faria", d["B"]),
                      ("Retailer", d["R"])):
        vals = [num(r.get("Daily_capacity_kg")) for r in rs]
        vals = [v for v in vals if v is not None]
        data.append(vals)
        names.append(f"{label}\n(n = {len(vals)})")

    fig, ax = plt.subplots(constrained_layout=True)
    ax.boxplot(data, patch_artist=True, widths=0.5, zorder=3,
               medianprops=dict(color="#B4472A", lw=1.6),
               boxprops=dict(facecolor=BOXFILL, edgecolor=EDGE, lw=0.9),
               whiskerprops=dict(color=EDGE, lw=0.9),
               capprops=dict(color=EDGE, lw=0.9),
               flierprops=dict(marker="o", markersize=4.5,
                               markerfacecolor="#9AA7B8",
                               markeredgecolor="none", alpha=0.85))
    ax.set_yscale("log")
    ax.set_yticks([10, 100, 1000])
    ax.set_yticklabels(["10", "100", "1,000"])
    for i, vals in enumerate(data):
        med = float(np.median(vals))
        ax.text(i + 1, med, f"{med:,.0f}", ha="center", va="center",
                fontsize=8.8, color="#B4472A", fontweight="bold", zorder=5,
                bbox=dict(facecolor="white", edgecolor="none",
                          alpha=0.9, pad=1.1))
    ax.set_xticks(range(1, len(data) + 1))
    ax.set_xticklabels(names)
    ax.set_xlabel("Market actor")
    ax.set_ylabel("Daily trading capacity (kilograms, logarithmic scale)")
    ax.set_title("Daily Trading Capacity by Actor Group\n"
                 "(log scale; boxes: median and interquartile range)",
                 loc="center")
    ax.yaxis.grid(True, which="major", color="#c8cdd3", lw=0.7, alpha=0.95)
    ax.yaxis.grid(True, which="minor", color="#e4e7ea", lw=0.5, alpha=0.9,
                  linestyle=":")
    ax.set_axisbelow(True)
    save(fig, "A1_daily_capacity_boxplot.png", 8.8, 6.2)


# ---------------------------------------------------------------------------
# A2 - Producer share of consumer price by species (horizontal bar) [appendix]
# ---------------------------------------------------------------------------
def figa2_producer_share(d):
    chain = chain_species_stats(d)
    rows = []
    for code, v in chain.items():
        # share reported only where MIN_CONS consumer quotes exist
        if v["producer"] is not None and v["consumer"] \
                and v["consumer_n"] >= MIN_CONS:
            rows.append((f"{d['SP'][code]['Local_name']} ({code})",
                         100.0 * v["producer"] / v["consumer"]))
    rows.sort(key=lambda t: t[1])
    p = pooled_chain(chain)
    pooled_ps = 100.0 * p["producer"] / p["consumer"]

    fig, ax = plt.subplots(constrained_layout=True)
    names = [r[0] for r in rows]
    vals = [r[1] for r in rows]
    y = np.arange(len(vals))
    ax.barh(y, vals, height=0.6, color=BARBLUE, edgecolor=EDGE,
            linewidth=0.7, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 0.7, yi, f"{v:.1f}%", ha="left", va="center",
                fontsize=10, fontweight="bold")
    ax.axvline(pooled_ps, color="#B4472A", lw=1.3, linestyle="--", zorder=4)
    ax.text(pooled_ps - 1.2, len(vals) - 0.28,
            f"Chain mean: {pooled_ps:.1f}%", ha="right", va="top",
            fontsize=10, color="#B4472A", fontweight="bold")
    ax.set_yticks(y)
    ax.set_yticklabels(names)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_minor_locator(AutoMinorLocator(2))
    ax.set_xlabel("Producer share of the consumer price (%)")
    ax.set_ylabel("Species (local name)")
    ax.set_title("Producer Share of the Consumer Price by Species\n"
                 "(dashed line: mean over chain-complete species)",
                 loc="center")
    style_axis(ax)
    save(fig, "A2_producer_share_by_species.png", 9.0, 6.6)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
FIGURES = [
    ("F1", "Average Marketing Margin by Chain Intermediary", "bar chart",
     "Main text, section 4.4 (margins)", fig1_margin_bar),
    ("F2", "Distribution of Retail Selling Prices by Species", "box plot",
     "Main text, section 4.3 (price levels and dispersion)", fig2_price_box),
    ("F3", "Average Price Progression along the Marketing Chain", "line chart",
     "Main text, section 4.3 (price chain)", fig3_chain_line),
    ("F4", "Decomposition of the Average Consumer Price", "donut chart",
     "Main text, section 4.4 (producer share)", fig4_price_donut),
    ("F5", "Payment Method Composition by Market Actor", "stacked bar",
     "Main text, section 4.6 (payment methods)", fig5_payment_stack),
    ("F6", "Market Infrastructure Quality Profile", "radar chart",
     "Main text, section 4.8 (market infrastructure)", fig6_infra_radar),
    ("F7", "Most Frequently Reported Marketing Problems", "rose chart",
     "Main text, section 4.7 (constraints)", fig7_problems_rose),
    ("F8", "Average Retail Selling Price by Market", "bar chart",
     "Main text, section 4.3 (spatial price comparison)", fig8_market_price_bar),
    ("A1", "Daily Trading Capacity by Actor Group", "box plot (log)",
     "Appendix (business scale)", figa1_capacity_box),
    ("A2", "Producer Share of the Consumer Price by Species", "horizontal bar",
     "Appendix (producer share detail)", figa2_producer_share),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=None)
    args = ap.parse_args()
    path = args.data or find_default_data()
    print(f"figures from: {path}")
    d = load_data(path)
    os.makedirs(CH2, exist_ok=True)
    for code, title, ctype, where, fn in FIGURES:
        fn(d)
    idx = pd.DataFrame([{"Figure": c, "File": f"{c.lower()}_*.png",
                         "Title": t, "Chart type": ty, "Placement": w}
                        for c, t, ty, w, _ in FIGURES])
    # actual file names
    files = {f.split("_")[0]: f for f in sorted(os.listdir(CH2))
             if f.endswith(".png")}
    idx["File"] = idx["Figure"].map(files)
    idx.to_csv(os.path.join(CH2, "FIGURE_INDEX.csv"), index=False,
               encoding="utf-8-sig")
    print(f"DONE - {len(FIGURES)} figures + FIGURE_INDEX.csv in {CH2}")


if __name__ == "__main__":
    main()
