#!/usr/bin/env python3
"""Re-embed the CURRENT dataset reference values into scripts/R/run_analysis.R
chk() calls (Python pipeline outputs are the source of truth).

Value-independent: anchors on the chk() call's check NAME, so the script can be
re-run after every dataset change (v1 -> v2 -> REAL -> future real data).
Counts are recomputed directly from the data workbook; every other value comes
from analysis_outputs/tables/*.csv.

Usage:
    python scripts/update_r_refs.py [--data path/to/filled.xlsx]
"""
import argparse
import os
import re

import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RFILE = os.path.join(ROOT, "scripts", "R", "run_analysis.R")
DEFAULT_DATA = os.path.join(
    ROOT, "04_data_filled",
    "Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx")

ap = argparse.ArgumentParser()
ap.add_argument("--data", default=DEFAULT_DATA, help="filled workbook (.xlsx)")
args = ap.parse_args()

T = lambda name: pd.read_csv(os.path.join(ROOT, "analysis_outputs", "tables", name + ".csv"))

src = open(RFILE, encoding="utf-8").read()
orig = src

# ---------------- source values ----------------
t1 = T("T1_Respondent_Profile")
t2 = T("T2_Business_Scale")
t5 = T("T5_Payment_Methods")
t3 = T("T3_Price_Chain")
t11 = T("T11_Retail_Price_by_Market")
t12b = T("T12b_Wilcoxon_Result")
t16 = T("T16_Stratum_Margin_MannWhitney")
t17 = T("T17_Retailer_MC_Profit_Spearman")
t15 = T("T15_Payment_Actor_ChiSquare")

chi_row = t15[t15["Actor"].astype(str).str.startswith("chi-square")]["MFS_share_pct"].iloc[0]
m = re.match(r"chi2=([\d.]+), df=(\d+), p=([\d.]+)", str(chi_row))
chi2, df_, p15 = m.groups()

all_row = t3[t3["Species_code"] == "ALL"].iloc[0]
producer = all_row["Producer_BDT_kg"]
aratdar = all_row["Aratdar_sell_BDT_kg"]
bepari = all_row["Bepari_sell_BDT_kg"]
retail = all_row["Retailer_sell_BDT_kg"]
consumer = all_row["Consumer_paid_BDT_kg"]
ps = all_row["Producer_share_pct"]

sp_cons = {r["Species_code"]: r["Consumer_paid_BDT_kg"] for _, r in t3.iterrows()}
sp_ret = {r["Species_code"]: r["Retailer_sell_BDT_kg"] for _, r in t3.iterrows()}

def t16v(actor, col):
    return float(t16[t16["Actor"] == actor][col].iloc[0])

def mwu(pair):
    return t16[t16["Actor"] == f"Mann-Whitney U: {pair}"]["Mean_margin_BDT_kg"].iloc[0]

t17row = t17[t17["Respondent_ID"].astype(str).str.startswith("Spearman")].iloc[0]
rho, p17 = t17row["MC_BDT_kg"], t17row["Net_profit_BDT_kg"]

# ---------------- counts from the data workbook ----------------
# Mirrors the R loader: Forms require Interview_Date; PO/CPF require Respondent_ID.
wb = openpyxl.load_workbook(args.data, data_only=True)

# chain-complete species — mirrors R chain(): every stage mean non-NA
# (producer = aratdar buy @ M1/M6; aratdar sell @ M1/M6; bepari sell anywhere;
# consumer paid) AND consumer n >= MIN_CONS (3)
MIN_CONS = 3
LANDING = {"M1", "M6"}
_po_rows = []
_ws = wb["Price_Observations"]
for _r in range(5, _ws.max_row + 1):
    if not _ws.cell(row=_r, column=3).value:
        continue
    _po_rows.append((_ws.cell(row=_r, column=5).value,   # actor
                     _ws.cell(row=_r, column=6).value,    # species
                     _ws.cell(row=_r, column=4).value,     # market
                     _ws.cell(row=_r, column=10).value,    # buy BDT/kg
                     _ws.cell(row=_r, column=11).value))   # sell BDT/kg
_cons = []
_wsc = wb["Consumer_Purchases_Focal"]
for _r in range(5, _wsc.max_row + 1):
    if not _wsc.cell(row=_r, column=2).value:
        continue
    if str(_wsc.cell(row=_r, column=5).value).strip().lower().startswith("y"):
        _cons.append((_wsc.cell(row=_r, column=4).value,
                      _wsc.cell(row=_r, column=9).value))

def _num(x):
    return isinstance(x, (int, float))

n_complete = 0
for _sp in [f"S{i:02d}" for i in range(1, 11)]:
    _prod = [b for a, s, m, b, _ in _po_rows if s == _sp and a == "Aratdar" and m in LANDING and _num(b)]
    _arat = [v for a, s, m, _, v in _po_rows if s == _sp and a == "Aratdar" and m in LANDING and _num(v)]
    _bep = [v for a, s, m, _, v in _po_rows if s == _sp and a == "Bepari_Faria" and _num(v)]
    _cn = [p for s, p in _cons if s == _sp and _num(p)]
    if _prod and _arat and _bep and len(_cn) >= MIN_CONS:
        n_complete += 1

def sheet_rows(name, key_col, start=5):
    """Count rows whose key column is non-empty (R read_form + require_col)."""
    ws = wb[name]
    n = 0
    for r in range(start, ws.max_row + 1):
        if ws.cell(row=r, column=key_col).value not in (None, ""):
            n += 1
    return n

# Forms A/B/R/C: Interview_Date is column 4 in all four sheets
n_A = sheet_rows("Form_A_Aratdar", 4)
n_B = sheet_rows("Form_B_Bepari_Faria", 4)
n_R = sheet_rows("Form_R_Khuchra", 4)
n_C = sheet_rows("Form_C_Consumer", 4)

# Price_Observations: Respondent_ID is column 3 (col 2 = prefilled Obs_ID)
po = wb["Price_Observations"]
po_rows = buy_k = sell_k = sell_d = 0
for r in range(5, po.max_row + 1):
    if not po.cell(row=r, column=3).value:
        continue
    po_rows += 1
    if str(po.cell(row=r, column=7).value).strip() == "K":
        buy_k += 1
    sv = str(po.cell(row=r, column=8).value).strip()
    if sv == "K":
        sell_k += 1
    elif sv == "D":
        sell_d += 1

cpf = wb["Consumer_Purchases_Focal"]
focal_rows = focal_yes = 0
for r in range(5, cpf.max_row + 1):
    if not cpf.cell(row=r, column=2).value:
        continue
    focal_rows += 1
    if str(cpf.cell(row=r, column=5).value).strip().lower().startswith("y"):
        focal_yes += 1

t5c = t5[t5["Actor"].astype(str) == "Consumer"]
bkash_pct = None
if len(t5c):
    row = t5c.iloc[0]
    for col in ("bKash_pct", "bKash_share_pct"):
        if col in row and pd.notna(row[col]):
            bkash_pct = float(row[col])

def fmt(x):
    """Match R literal style: trailing-zero-free but keep >=1 decimal."""
    if x is None or (isinstance(x, float) and pd.isna(x)):
        return None
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    if "." not in s:
        s += ".0"
    return s

# ---------------- name-anchored patcher ----------------
def find_call_end(s, start):
    """Index of the ')' closing the chk( call starting at 'start' (idx of 'chk')."""
    depth = 0
    i = start
    in_str = False
    while i < len(s):
        ch = s[i]
        if in_str:
            if ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1

def patch_num(name, newval, tol_keep=True):
    """Replace the expected numeric literal of chk("name", ..., OLD[, tol = t])."""
    global src
    anchor = f'chk("{name}"'
    i = src.find(anchor)
    if i < 0:
        print(f"!! NOT FOUND (anchor): {name}")
        return
    end = find_call_end(src, i)
    if end < 0:
        print(f"!! NOT FOUND (close): {name}")
        return
    call = src[i:end + 1]
    # expected value = numeric literal after the LAST top-level comma
    mm = re.search(r",\s*(-?[\d.]+)\s*(,\s*tol\s*=\s*([\d.]+))?\s*\)\s*$", call)
    if not mm:
        print(f"!! NOT FOUND (value): {name}")
        return
    tol_part = f", tol = {mm.group(3)}" if (tol_keep and mm.group(3)) else ""
    new_call = call[:mm.start()] + f", {newval}{tol_part})"
    src = src[:i] + new_call + src[end + 1:]

def patch_str(name, newval):
    """Replace the expected "..." literal of chk("name", ..., "OLD")."""
    global src
    anchor = f'chk("{name}"'
    i = src.find(anchor)
    if i < 0:
        print(f"!! NOT FOUND (anchor): {name}")
        return
    end = find_call_end(src, i)
    call = src[i:end + 1]
    mm = re.search(r',\s*"([^"]*)"\s*\)\s*$', call)
    if not mm:
        print(f"!! NOT FOUND (string value): {name}")
        return
    new_call = call[:mm.start()] + f', "{newval}")'
    src = src[:i] + new_call + src[end + 1:]

def patch_tail(anchor, newval):
    """Replace the trailing ', OLD)' after a literal anchor (continuation lines)."""
    global src
    i = src.find(anchor)
    if i < 0:
        print(f"!! NOT FOUND (tail anchor): {anchor[:50]}")
        return
    j = src.find(")", i)
    seg = src[i:j + 1]
    mm = re.search(r",\s*(-?[\d.]+)\s*\)\s*$", seg)
    if not mm:
        print(f"!! NOT FOUND (tail value): {anchor[:50]}")
        return
    src = src[:i] + seg[:mm.start()] + f", {newval})" + src[j + 1:]

# ---------------- apply ----------------
patch_num("Form A (Aratdar) respondents", n_A)
patch_num("Form B (Bepari/Faria) respondents", n_B)
patch_num("Form R (Retailer) respondents", n_R)
patch_num("Form C (Consumer) respondents", n_C)
patch_num("Total interviews", n_A + n_B + n_R + n_C)
patch_num("Price_Observations rows", po_rows)
patch_num("Buy price cells K (closed today)", buy_k)
patch_num("Sell price cells K (closed today)", sell_k)
patch_num("Sell price cells D (refused)", sell_d)
patch_num("Consumer focal purchase rows", focal_rows)
patch_num("Focal purchases bought today (Yes)", focal_yes)

patch_num("T1 Aratdar mean age (years)", fmt(t1.iloc[0]["Age_mean_years"]))
patch_num("T1 Bepari mean age (years)", fmt(t1.iloc[1]["Age_mean_years"]))
patch_num("T1 Faria mean age (years)", fmt(t1.iloc[2]["Age_mean_years"]))
patch_num("T1 Retailer mean age (years)", fmt(t1.iloc[3]["Age_mean_years"]))
patch_num("T1 Aratdar mean experience (years)", fmt(t1.iloc[0]["Years_in_business_mean"]))
patch_num("T1 Retailer mean experience (years)", fmt(t1.iloc[3]["Years_in_business_mean"]))

patch_num("T2 Aratdar mean daily capacity (kg)", fmt(t2.iloc[0]["Daily_capacity_kg_mean"]))
patch_num("T2 Bepari/Faria mean daily capacity (kg)", fmt(t2.iloc[1]["Daily_capacity_kg_mean"]))
patch_num("T2 Retailer mean daily capacity (kg)", fmt(t2.iloc[2]["Daily_capacity_kg_mean"]))

patch_num("T5 Aratdar mean cash share (%)", fmt(t5.iloc[0]["Cash_pct_mean"]))
patch_num("T5 Bepari mean cash share (%)", fmt(t5.iloc[1]["Cash_pct_mean"]))
patch_num("T5 Retailer mean cash share (%)", fmt(t5.iloc[2]["Cash_pct_mean"]))
if bkash_pct is not None:
    patch_tail('T5c$pct[T5c$Method == "bKash"]', fmt(bkash_pct))

patch_num("Chain-complete species count (MIN_CONS)", n_complete)
patch_num("T3 ALL producer price (BDT/kg)", fmt(producer))
patch_num("T3 ALL aratdar sell (BDT/kg)", fmt(aratdar))
patch_num("T3 ALL bepari sell (BDT/kg)", fmt(bepari))
patch_num("T3 ALL retailer quote (BDT/kg)", fmt(retail))
patch_num("T3 ALL consumer paid (BDT/kg)", fmt(consumer))
patch_num("T10 aratdar margin (BDT/kg)", fmt(aratdar - producer))
patch_num("T10 bepari margin (BDT/kg)", fmt(bepari - aratdar))
patch_num("T10 retailer margin (BDT/kg)", fmt(consumer - bepari))
patch_num("T10 total marketing spread (BDT/kg)", fmt(consumer - producer))
patch_num("T10 producer share (%)", fmt(ps))

for sp, nm in [("S01", 'T3 S01 Ilish consumer price (BDT/kg)'),
               ("S02", 'T3 S02 Rupchanda consumer price'),
               ("S03", 'T3 S03 Lakkha consumer price'),
               ("S04", 'T3 S04 Koral consumer price'),
               ("S05", 'T3 S05 Surma consumer price'),
               ("S06", 'T3 S06 Churi consumer price'),
               ("S07", 'T3 S07 Poa consumer price'),
               ("S08", 'T3 S08 Kankoita consumer price'),
               ("S09", 'T3 S09 Loitta consumer price'),
               ("S10", 'T3 S10 Harina consumer price')]:
    # names may carry suffixes like " (n=1, descriptive)" in older versions --
    # anchor on the base text via fuzzy find
    anchor = f'chk("{nm}'
    i = src.find(anchor)
    if i < 0:
        print(f"!! NOT FOUND (species): {nm}")
        continue
    end = find_call_end(src, i)
    call = src[i:end + 1]
    mm = re.search(r'chk\("([^"]+)"', call)
    if mm:
        patch_num(mm.group(1), fmt(sp_cons[sp]))
    else:
        print(f"!! NOT FOUND (species name): {nm}")

patch_num("T3 S01 Ilish retailer quote (BDT/kg)", fmt(sp_ret["S01"]))
patch_num("T11 S01 Ilish retail at Fishery Ghat", fmt(t11.iloc[0]["Fishery Ghat"]))

patch_num("T12b usable matched pairs", int(t12b.iloc[0]["Value"]))
patch_num("T12b pairs with non-zero difference", int(t12b.iloc[1]["Value"]))
patch_num("T12b Wilcoxon W (scipy convention)", t12b.iloc[4]["Value"])
patch_num("T12b Wilcoxon p-value", t12b.iloc[5]["Value"])

patch_num("T15 chi-square statistic", chi2)
patch_num("T15 chi-square df", df_)
patch_num("T15 chi-square p-value", p15)

for actor in ("Aratdar", "Bepari_Faria", "Khuchra"):
    patch_tail(f'T16$Median_margin_BDT_kg[T16$Actor == "{actor}"]',
               fmt(t16v(actor, "Median_margin_BDT_kg")))
    patch_tail(f'T16$Mean_margin_BDT_kg[T16$Actor == "{actor}"]',
               fmt(t16v(actor, "Mean_margin_BDT_kg")))

patch_str("T16 MWU result Aratdar vs Bepari/Faria", mwu("Aratdar vs Bepari_Faria"))
patch_str("T16 MWU result Aratdar vs Retailer", mwu("Aratdar vs Khuchra"))
patch_str("T16 MWU result Bepari/Faria vs Retailer", mwu("Bepari_Faria vs Khuchra"))

patch_num("T17 Spearman rho (MC vs net margin)", rho)
patch_num("T17 Spearman p-value", p17)
patch_num("T17 retailer n", 30)

if src != orig:
    open(RFILE, "w", encoding="utf-8").write(src)
    n_changed = sum(1 for a, b in zip(orig.splitlines(), src.splitlines()) if a != b)
    print(f"patched run_analysis.R ({n_changed} lines changed) -> {RFILE}")
else:
    print("no changes needed")
