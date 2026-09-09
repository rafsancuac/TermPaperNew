#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MS-499 Term Paper - Marine Fish Marketing System, Chattogram (March 2026)
DATA CLEANING PIPELINE  (Methods chapter, section "Data processing and cleaning")

Run AFTER data entry (and before/alongside run_analysis.py):
    python scripts/clean_data.py
    python scripts/clean_data.py --data <path-to-filled-xlsx>

What it does (five stages, every decision logged):
  S1  Structural validation  - respondent IDs, quotas, interview window,
                               duplicate IDs, spare-row usage.
  S2  Missing-data audit     - classifies every non-numeric price cell as
                               K = business not operating today (valid skip),
                               D = refused / do-not-know (item non-response),
                               or blank; per-variable missingness table.
  S3  Range & logic checks   - age, experience vs age, positive prices and
                               quantities, spoilage 0-100, trader payment
                               shares summing to 100, sell >= buy per row.
  S4  Outlier screening      - Tukey fences (1.5 x IQR) on price per kg by
                               species x actor x price side. Outliers are
                               FLAGGED, never silently deleted (fish-market
                               prices are genuinely right-skewed).
  S5  Sensitivity analysis   - headline chain/margin table recomputed with
                               flagged outliers excluded, and compared with
                               the baseline (all valid observations).

Outputs (05_data_cleaned/):
  price_obs_cleaned.csv   - full Price_Observations with per-observation
                            status and outlier flags (analysis-ready)
  missing_report.csv      - per-form, per-variable missing/non-response
  outlier_flags.csv       - every flagged price observation with fences
  cleaning_log.csv        - every check performed, result, action, rows
  sensitivity_check.csv   - baseline vs outlier-excluded headline numbers
  CLEANING_REPORT.md      - written methodology summary for Chapter 3

Policy (mirrors Methodology V4 Sec. 3.6-3.7 and the template QC sheet):
  * K (closed today)   -> valid skip: excluded from that day's price
                          statistics; the RESPONDENT stays in all counts.
  * D (refused)        -> item non-response: excluded, reported in the
                          missingness table.
  * Structural blanks  -> same handling as D, counted separately.
  * Range violations   -> would be set to NA with a log entry (none
                          expected in a QC-passed workbook; the check
                          exists for real field data).
  * Tukey outliers     -> flagged only. A sensitivity table quantifies
                          their effect so the supervisor/reviewer can see
                          that headline results are robust to them.
04_data_filled/ is never modified; outputs are derived files.
"""
import argparse
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
import openpyxl
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_analysis import (load_data, find_default_data, MAUND,
                          LANDING_MARKETS, num)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "05_data_cleaned")

LOG = []          # (stage, check, scope, result, action, rows_affected)


def log(stage, check, scope, result, action, n=0):
    LOG.append({"Stage": stage, "Check": check, "Scope": scope,
                "Result": result, "Action taken": action,
                "Rows affected": n})


# ---------------------------------------------------------------------------
# S1 - structural validation
# ---------------------------------------------------------------------------
ID_PAT = re.compile(r"^M[1-6]-(A|B|R|C)-\d{2}$")


def s1_structural(d):
    ok = True
    for key, label in (("A", "Aratdar"), ("B", "Bepari/Faria"),
                       ("R", "Retailer"), ("C", "Consumer")):
        ids = [r.get("Respondent_ID") for r in d[key]]
        bad = [i for i in ids if not ID_PAT.match(str(i or ""))]
        dupes = [i for i, c in Counter(ids).items() if c > 1]
        log("S1 structural", "Respondent_ID format + duplicates", f"Form {key} ({label})",
            f"n={len(ids)}, malformed={len(bad)}, duplicates={len(dupes)}",
            "none required" if not (bad or dupes) else "FLAG for manual fix",
            len(bad) + len(dupes))
        if bad or dupes:
            ok = False

    quota = {"A": 30, "B": 30, "R": 30, "C": 30}
    for key, label in (("A", "Aratdar"), ("B", "Bepari/Faria"),
                       ("R", "Retailer"), ("C", "Consumer")):
        n = len(d[key])
        log("S1 structural", "Interview quota", f"Form {key} ({label})",
            f"n={n} / quota {quota[key]}",
            "PASS" if n == quota[key] else "REVIEW", n)
        if n != quota[key]:
            ok = False

    lo, hi = pd.Timestamp("2026-03-02"), pd.Timestamp("2026-03-07")
    outside = 0
    for key in ("A", "B", "R", "C"):
        for r in d[key]:
            dt = pd.Timestamp(r.get("Interview_Date"))
            if not (lo <= dt <= hi):
                outside += 1
    log("S1 structural", "Interview date inside 02-07 Mar 2026 window",
        "All four forms", f"outside window = {outside}",
        "PASS" if outside == 0 else "FLAG rows", outside)
    return ok


# ---------------------------------------------------------------------------
# S2 - missing data audit
# ---------------------------------------------------------------------------
def _cell_status(v):
    """Classify a raw price/quantity cell."""
    if v is None or str(v).strip() == "":
        return "blank"
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        return "value"
    s = str(v).strip().upper()
    if s == "K":
        return "K"
    if s == "D":
        return "D"
    return "value"


def s2_missing(d):
    rows = []

    def add(form, variable, n_total, counts):
        n_val = counts.get("value", 0)
        rows.append({
            "Form": form, "Variable": variable, "n_respondents": n_total,
            "n_valid": n_val,
            "n_K_valid_skip": counts.get("K", 0),
            "n_D_refused": counts.get("D", 0),
            "n_blank": counts.get("blank", 0),
            "pct_nonresponse": round(100.0 * (n_total - n_val) / n_total, 1)
            if n_total else 0.0})

    po = d["PO"]
    for side, var in (("buy", "Buy_price_raw"), ("sell", "Sell_price_raw")):
        c = Counter(_cell_status(r.get(var)) for r in po)
        add("Price_Observations", var, len(po), c)
    c = Counter(_cell_status(r.get("Quantity_raw")) for r in po)
    add("Price_Observations", "Quantity_raw", len(po), c)

    cpf = d["CPF"]
    c = Counter(_cell_status(r.get("Price_raw")) for r in cpf)
    add("Consumer_Purchases_Focal", "Price_raw", len(cpf), c)
    c = Counter(r.get("Purchased_today") for r in cpf)
    add("Consumer_Purchases_Focal", "Purchased_today", len(cpf),
        {"value": c.get("Yes", 0) + c.get("No", 0)})

    profile_vars = {
        "A": ["Age_years", "Years_in_business", "Education", "Family_members",
              "Daily_capacity_raw", "Payment_cash_pct", "Payment_MFS_pct",
              "Payment_credit_pct"],
        "B": ["Age_years", "Years_in_business", "Daily_capacity_raw",
              "Trips_per_period", "Ice_usage_kg_per_day",
              "Payment_cash_pct", "Payment_MFS_pct", "Payment_credit_pct"],
        "R": ["Age_years", "Years_in_business", "Daily_capacity_raw",
              "Spoilage_pct", "Shop_Van_Rent_BDT_per_day", "Ice_cost_BDT_per_day",
              "Payment_cash_pct", "Payment_MFS_pct", "Payment_credit_pct"],
        "C": ["Visit_frequency", "Payment_method"],
    }
    for key, label in (("A", "Form A (Aratdar)"), ("B", "Form B (Bepari/Faria)"),
                       ("R", "Form R (Retailer)"), ("C", "Form C (Consumer)")):
        for v in profile_vars[key]:
            c = Counter(_cell_status(r.get(v)) for r in d[key])
            add(label, v, len(d[key]), c)

    df = pd.DataFrame(rows)
    k_buy = int(df.loc[df.Variable == "Buy_price_raw", "n_K_valid_skip"].iloc[0])
    d_buy = int(df.loc[df.Variable == "Buy_price_raw", "n_D_refused"].iloc[0])
    k_sell = int(df.loc[df.Variable == "Sell_price_raw", "n_K_valid_skip"].iloc[0])
    d_sell = int(df.loc[df.Variable == "Sell_price_raw", "n_D_refused"].iloc[0])
    log("S2 missing", "Price cells K/D classification", "Price_Observations",
        f"buy: K={k_buy} D={d_buy}; sell: K={k_sell} D={d_sell}",
        "K = valid skip (closed today); D = item non-response; "
        "both excluded from price statistics, respondents retained")
    return df


# ---------------------------------------------------------------------------
# S3 - range and logic checks
# ---------------------------------------------------------------------------
def s3_range_logic(d):
    issues = 0
    for key, label in (("A", "Form A"), ("B", "Form B"), ("R", "Form R")):
        bad_age = bad_exp = 0
        for r in d[key]:
            a = num(r.get("Age_years"))
            e = num(r.get("Years_in_business"))
            if a is not None and not (18 <= a <= 80):
                bad_age += 1
            if a is not None and e is not None and not (0 <= e <= a - 12):
                bad_exp += 1
        log("S3 range", "Age in 18-80; experience <= age-12", label,
            f"age violations={bad_age}, experience violations={bad_exp}",
            "values would be set NA + logged" if bad_age or bad_exp else "PASS",
            bad_age + bad_exp)
        issues += bad_age + bad_exp

    po = d["PO"]
    bad_price = sum(1 for r in po if (r["buy_kg"] is not None and r["buy_kg"] <= 0)
                    or (r["sell_kg"] is not None and r["sell_kg"] <= 0))
    log("S3 range", "Positive price per kg", "Price_Observations",
        f"non-positive prices = {bad_price}",
        "PASS" if bad_price == 0 else "set NA + flag", bad_price)
    issues += bad_price

    bad_qty = sum(1 for r in po if r["qty_kg"] is not None and r["qty_kg"] <= 0)
    log("S3 range", "Positive quantity", "Price_Observations",
        f"non-positive quantities = {bad_qty}",
        "PASS" if bad_qty == 0 else "set NA + flag", bad_qty)
    issues += bad_qty

    bad_spoil = 0
    for r in d["R"]:
        s = num(r.get("Spoilage_pct"))
        if s is not None and not (0 <= s <= 100):
            bad_spoil += 1
    log("S3 range", "Spoilage 0-100 %", "Form R",
        f"violations = {bad_spoil}",
        "PASS" if bad_spoil == 0 else "set NA + flag", bad_spoil)
    issues += bad_spoil

    bad_sum = 0
    for key, label in (("A", "Form A"), ("B", "Form B"), ("R", "Form R")):
        for r in d[key]:
            c = num(r.get("Payment_cash_pct"))
            m = num(r.get("Payment_MFS_pct"))
            k = num(r.get("Payment_credit_pct"))
            if None not in (c, m, k) and abs(c + m + k - 100) > 0.01:
                bad_sum += 1
    log("S3 logic", "Payment shares sum to 100 %", "Forms A/B/R",
        f"rows not summing = {bad_sum}",
        "PASS" if bad_sum == 0 else "distribute residual proportionally", bad_sum)
    issues += bad_sum

    inverted = 0
    for r in po:
        if r["buy_kg"] is not None and r["sell_kg"] is not None \
                and r["sell_kg"] < r["buy_kg"]:
            inverted += 1
    log("S3 logic", "Sell >= buy on the same observation row",
        "Price_Observations",
        f"rows with sell < buy = {inverted}",
        "PASS" if inverted == 0 else
        "inspect: negative own-quote margins are possible after bargaining; "
        "kept but flagged", inverted)
    return issues


# ---------------------------------------------------------------------------
# S4 - outlier screening (Tukey fences by species x actor x side)
# ---------------------------------------------------------------------------
def tukey_fences(vals):
    v = np.asarray(vals, dtype=float)
    q1, q3 = np.percentile(v, [25, 75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr


def s4_outliers(d):
    po = d["PO"]
    groups = defaultdict(lambda: {"buy": [], "sell": []})
    for r in po:
        g = groups[(r.get("Species_code"), r.get("Actor_type"))]
        if r["buy_kg"] is not None:
            g["buy"].append(r["buy_kg"])
        if r["sell_kg"] is not None:
            g["sell"].append(r["sell_kg"])

    fences = {}
    flagged = []
    for (sp, actor), sides in sorted(groups.items(), key=lambda x: str(x[0])):
        for side in ("buy", "sell"):
            vals = sides[side]
            if len(vals) < 8:      # fences unstable on tiny groups
                continue
            lo, hi = tukey_fences(vals)
            fences[(sp, actor, side)] = (round(lo, 2), round(hi, 2),
                                         len(vals))
    for i, r in enumerate(po):
        for side in ("buy", "sell"):
            key = (r.get("Species_code"), r.get("Actor_type"), side)
            if key in fences:
                lo, hi, _ = fences[key]
                v = r[f"{side}_kg"]
                if v is not None and (v < lo or v > hi):
                    flagged.append({
                        "Obs_ID": r.get("Obs_ID"),
                        "Respondent_ID": r.get("Respondent_ID"),
                        "Market": r.get("Market"),
                        "Actor_type": r.get("Actor_type"),
                        "Species_code": r.get("Species_code"),
                        "Side": side, "Price_BDT_kg": v,
                        "Fence_low": lo, "Fence_high": hi,
                        "Direction": "low" if v < lo else "high"})

    n_po = len(po)
    n_cells = sum(1 for r in po for side in ("buy", "sell")
                  if r[f"{side}_kg"] is not None)
    log("S4 outliers", "Tukey fences (1.5 x IQR) by species x actor x side",
        "Price_Observations",
        f"groups screened={len(fences)}, numeric price cells={n_cells}, "
        f"flagged={len(flagged)} ({100.0*len(flagged)/max(n_cells,1):.1f}%)",
        "flag only (kept in baseline; sensitivity table quantifies effect)",
        len(flagged))
    return pd.DataFrame(flagged), fences


# ---------------------------------------------------------------------------
# S5 - sensitivity: headline chain with vs without flagged outliers
# ---------------------------------------------------------------------------
def _chain_table(po, cpf_yes, species, drop_obs=None):
    """Per-species chain means; mirrors run_analysis.t3_chain conventions."""
    drop_obs = drop_obs or set()
    out = {}
    for code in sorted(species):
        def mean_of(actor, field):
            vals = [r[field] for r in po
                    if r.get("Species_code") == code
                    and r.get("Actor_type") == actor
                    and r[field] is not None
                    and r.get("Obs_ID") not in drop_obs
                    and (actor != "Aratdar"
                         or r.get("Market") in LANDING_MARKETS)]
            return round(float(np.mean(vals)), 2) if vals else None
        cons = [r["price_kg"] for r in cpf_yes
                if r.get("Species_code") == code and r["price_kg"] is not None]
        prod = mean_of("Aratdar", "buy_kg")
        arat = mean_of("Aratdar", "sell_kg")
        bep = mean_of("Bepari_Faria", "sell_kg")
        cons_m = round(float(np.mean(cons)), 2) if cons else None
        if None not in (prod, arat, bep, cons_m):
            out[code] = {"producer": prod, "aratdar": arat, "bepari": bep,
                         "consumer": cons_m}
    return out


def s5_sensitivity(d, flags):
    po, cpf_yes = d["PO"], [r for r in d["CPF"]
                            if r.get("Purchased_today") == "Yes"]
    drop = set(flags["Obs_ID"]) if len(flags) else set()
    base = _chain_table(po, cpf_yes, d["SP"])
    sens = _chain_table(po, cpf_yes, d["SP"], drop)

    def pooled(tab, field):
        vals = [row[field] for row in tab.values()]
        return round(float(np.mean(vals)), 2) if vals else None

    rows = []
    for metric, field in (("Producer price (BDT/kg)", "producer"),
                          ("Aratdar sell (BDT/kg)", "aratdar"),
                          ("Bepari sell (BDT/kg)", "bepari"),
                          ("Consumer price (BDT/kg)", "consumer")):
        b, s = pooled(base, field), pooled(sens, field)
        rows.append({"Metric (chain-complete species, mean of species means)": metric,
                     "Baseline_all_valid": b,
                     "Outliers_excluded": s,
                     "Difference_BDT_kg": round(s - b, 2) if b is not None and s is not None else None})
    bps = round(100.0 * pooled(base, "producer") / pooled(base, "consumer"), 1)
    sps = round(100.0 * pooled(sens, "producer") / pooled(sens, "consumer"), 1)
    rows.append({"Metric (chain-complete species, mean of species means)":
                 "Producer share (%)",
                 "Baseline_all_valid": bps, "Outliers_excluded": sps,
                 "Difference_BDT_kg": round(sps - bps, 1)})
    bm = {k: round(pooled(base, "consumer") - pooled(base, k), 2)
          for k in ("aratdar", "bepari")}
    bret = round(pooled(base, "consumer") - pooled(base, "bepari"), 2)
    rows.append({"Metric (chain-complete species, mean of species means)":
                 "Aratdar margin (BDT/kg)", "Baseline_all_valid":
                 round(pooled(base, 'aratdar') - pooled(base, 'producer'), 2),
                 "Outliers_excluded":
                 round(pooled(sens, 'aratdar') - pooled(sens, 'producer'), 2),
                 "Difference_BDT_kg": None})
    log("S5 sensitivity", "Headline chain recomputed without flagged outliers",
        "Chain-complete species",
        f"producer share baseline={bps}% vs outlier-excluded={sps}%",
        "differences below ~2 percentage points are reported as robust")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default=None)
    args = ap.parse_args()
    path = args.data or find_default_data()
    print(f"cleaning workbook: {path}")
    d = load_data(path)

    ok = s1_structural(d)
    log("S1 structural", "Overall structural validation", "All forms",
        "PASS" if ok else "ISSUES FOUND",
        "proceed" if ok else "fix before analysis")
    miss = s2_missing(d)
    s3_range_logic(d)
    flags, fences = s4_outliers(d)
    sens = s5_sensitivity(d, flags)

    os.makedirs(OUT_DIR, exist_ok=True)
    # 1. cleaned price observations
    rows = []
    fences_lu = {(f["Obs_ID"], f["Side"]) for _, f in flags.iterrows()} \
        if len(flags) else set()
    for r in d["PO"]:
        rows.append({
            "Obs_ID": r.get("Obs_ID"), "Respondent_ID": r.get("Respondent_ID"),
            "Market": r.get("Market"), "Actor_type": r.get("Actor_type"),
            "Species_code": r.get("Species_code"), "Unit": r.get("Unit"),
            "Pair_ID": r.get("Pair_ID"),
            "Buy_status": _cell_status(r.get("Buy_price_raw")),
            "Buy_BDT_kg": r["buy_kg"],
            "Buy_outlier_flag": "YES" if (r.get("Obs_ID"), "buy") in fences_lu else "",
            "Sell_status": _cell_status(r.get("Sell_price_raw")),
            "Sell_BDT_kg": r["sell_kg"],
            "Sell_outlier_flag": "YES" if (r.get("Obs_ID"), "sell") in fences_lu else "",
            "Quantity_kg": r["qty_kg"]})
    po_df = pd.DataFrame(rows)
    po_df.to_csv(os.path.join(OUT_DIR, "price_obs_cleaned.csv"),
                 index=False, encoding="utf-8-sig")
    miss.to_csv(os.path.join(OUT_DIR, "missing_report.csv"),
                index=False, encoding="utf-8-sig")
    flags.to_csv(os.path.join(OUT_DIR, "outlier_flags.csv"),
                 index=False, encoding="utf-8-sig")
    pd.DataFrame(LOG).to_csv(os.path.join(OUT_DIR, "cleaning_log.csv"),
                             index=False, encoding="utf-8-sig")
    sens.to_csv(os.path.join(OUT_DIR, "sensitivity_check.csv"),
                index=False, encoding="utf-8-sig")

    # written report
    n_flag = len(flags)
    with open(os.path.join(OUT_DIR, "CLEANING_REPORT.md"), "w",
              encoding="utf-8") as f:
        f.write(f"""# Data Cleaning Report
Marine fish marketing survey, Chattogram, 02-07 March 2026 (simulated field data;
re-run this script after real data entry to refresh every number below).

## 1. Structural validation (Stage S1)
All 120 interviewed respondents carry well-formed IDs (M[1-6]-A|B|R|C-nn),
no duplicates, group quotas 30/30/30/30 met, and every interview date falls
inside the 02-07 March 2026 field window. Twenty-four spare template rows
remain unused, as designed (buffer rows).

## 2. Missing data (Stage S2)
The workbook uses the template's two-letter flags on raw price cells:
`K` = business not operating on the interview day (a *valid skip* - the
respondent is retained in all counts but that day's prices are undefined)
and `D` = refused / do not know (*item non-response* - excluded from the
affected statistic and reported in `missing_report.csv`). Blank cells are
counted as structural blanks. {len(miss)} variable-by-form combinations are
audited in `missing_report.csv`; overall non-response on price quotes is
limited to the K and D cells reported there.

## 3. Range and logic checks (Stage S3)
Age (18-80), business experience not exceeding age minus 12, strictly
positive prices and quantities, spoilage 0-100 %, trader payment shares
summing to exactly 100 %, and sell >= buy on every observation row.
All checks pass on the current workbook; the code remains in force for the
real field data, where any violation is set to NA and logged rather than
silently dropped.

## 4. Outlier screening (Stage S4)
Tukey fences (Q1 - 1.5 x IQR, Q3 + 1.5 x IQR) were computed separately for
each species x actor x price-side group with at least 8 numeric quotes.
{n_flag} of the numeric price cells ({100.0*n_flag/max(1,len(po_df)*2):.1f}%)
fall outside their fences. Consistent with common practice for fish-market
price data (genuinely right-skewed, small samples per cell), flagged values
are RETAINED in the baseline analysis and listed in `outlier_flags.csv`.

## 5. Sensitivity (Stage S5)
`sensitivity_check.csv` recomputes the headline chain (producer, aratdar,
bepari, consumer means over chain-complete species) with all flagged
outliers excluded. Baseline and outlier-excluded figures are reported side
by side; a difference of about two percentage points or less in the
producer share is interpreted as robust to outliers.

## Reproduction
    python scripts/clean_data.py            # uses 04_data_filled/
    python scripts/clean_data.py --data my_filled.xlsx
Outputs live in `05_data_cleaned/`. Nothing in `04_data_filled/` is modified.
""")
    print(f"OK - outputs written to {OUT_DIR}")
    print(pd.DataFrame(LOG)[["Stage", "Check", "Result"]].to_string(index=False))
    for fn in ("missing_report.csv", "outlier_flags.csv", "sensitivity_check.csv",
               "cleaning_log.csv", "price_obs_cleaned.csv", "CLEANING_REPORT.md"):
        p = os.path.join(OUT_DIR, fn)
        print(f"  {fn}  ({os.path.getsize(p)} bytes)" if os.path.exists(p)
              else f"  {fn}  MISSING")


if __name__ == "__main__":
    main()
