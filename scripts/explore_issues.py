#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Deep-dive exploration used for the supervisor-style review (Sep 2026).
Checks: chain additivity, producer-price market scope, pair structure,
species x market quote coverage, docs-vs-tables mismatches.
Read-only; writes nothing except printing.
"""
import os
import sys
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_analysis import (load_data, num, price_per_kg, qty_to_kg, MAUND,
                          find_default_data)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = load_data(find_default_data())

po = d["PO"]
SP = d["SP"]
MK = d["MK"]
cpf = [r for r in d["CPF"] if r.get("Purchased_today") == "Yes"]

def mean(vals):
    vals = [v for v in vals if v is not None]
    return float(np.mean(vals)) if vals else None

def pcol(dfrows, actor, field, mkt=None, sp=None):
    return mean([r[field] for r in dfrows
                 if r.get("Actor_type") == actor and r[field] is not None
                 and (mkt is None or r.get("Market") == mkt)
                 and (sp is None or r.get("Species_code") == sp)])

print("=" * 72)
print("A) PRODUCER PRICE SCOPE: aratdar buy by market (BDT/kg pooled over species)")
print("=" * 72)
for m in ["M1", "M2", "M3", "M4", "M5", "M6"]:
    n = sum(1 for r in po if r.get("Actor_type") == "Aratdar"
            and r.get("Market") == m and r["buy_kg"] is not None)
    print(f"  {m} {MK[m]:22s}  aratdar-buy mean = {mean([r['buy_kg'] for r in po if r.get('Actor_type')=='Aratdar' and r.get('Market')==m and r['buy_kg'] is not None]):8.2f}   n={n}")

print("  Landing-linked (M1,M6)  :", round(pcol(po, "Aratdar", "buy_kg", mkt=None) or 0, 2))
for mset, lab in [(("M1", "M6"), "M1+M6 (landing)"),
                  (("M2", "M3", "M4", "M5"), "M2-M5 (retail arats)")]:
    v = mean([r["buy_kg"] for r in po if r.get("Actor_type") == "Aratdar"
              and r.get("Market") in mset and r["buy_kg"] is not None])
    print(f"  {lab:22s}: {v:8.2f}")

print()
print("=" * 72)
print("B) PER-SPECIES: where do 'producer' (Aratdar buy) quotes come from?")
print("=" * 72)
for code in sorted(SP):
    mkts = sorted({r.get("Market") for r in po
                   if r.get("Actor_type") == "Aratdar"
                   and r.get("Species_code") == code and r["buy_kg"] is not None})
    print(f"  {code} {SP[code]['Local_name']:10s} Aratdar-buy quotes in markets: {mkts}")

print()
print("=" * 72)
print("C) CHAIN ADDITIVITY (current tables vs consumer-anchored margins)")
print("=" * 72)
codes = sorted(SP)
def sp_level(field):
    vals = []
    for c in codes:
        v = None
        if field == "prod_all":   v = pcol(po, "Aratdar", "buy_kg", sp=c)
        if field == "prod_land":  v = mean([r["buy_kg"] for r in po
                                            if r.get("Actor_type") == "Aratdar"
                                            and r.get("Market") in ("M1", "M6")
                                            and r.get("Species_code") == c
                                            and r["buy_kg"] is not None])
        if field == "arat_sell":  v = pcol(po, "Aratdar", "sell_kg", sp=c)
        if field == "bep_sell":   v = pcol(po, "Bepari_Faria", "sell_kg", sp=c)
        if field == "ret_sell":   v = pcol(po, "Khuchra", "sell_kg", sp=c)
        if field == "cons":       v = mean([r["price_kg"] for r in cpf
                                            if r.get("Species_code") == c])
        if v is not None:
            vals.append(v)
    return float(np.mean(vals)) if vals else None, len(vals)

prod_all, _ = sp_level("prod_all")
prod_land, _ = sp_level("prod_land")
arat, _ = sp_level("arat_sell")
bep, _ = sp_level("bep_sell")
retq, _ = sp_level("ret_sell")
cons, _ = sp_level("cons")

print(f"  Producer (Aratdar buy, all markets)     = {prod_all:.2f}")
print(f"  Producer (Aratdar buy, M1+M6 only)      = {prod_land:.2f}   <- proxy per methodology")
print(f"  Aratdar sell = {arat:.2f} | Bepari sell = {bep:.2f} | Retailer sell quote = {retq:.2f} | Consumer paid = {cons:.2f}")
print()
print("  CURRENT table logic (retail margin from retailer SELL QUOTE):")
m_arat = arat - prod_all; m_bep = bep - arat; m_ret_q = retq - bep; spread_q = cons - prod_all
print(f"    margins: A {m_arat:.2f} + B {m_bep:.2f} + R {m_ret_q:.2f} = {m_arat+m_bep+m_ret_q:.2f}")
print(f"    total spread (cons - prod) = {spread_q:.2f}  -> gap = {m_arat+m_bep+m_ret_q-spread_q:.2f} ({100*(m_arat+m_bep+m_ret_q-spread_q)/cons:.1f}% of consumer taka)")
print(f"    producer share {100*prod_all/cons:.1f}% + margins {100*(m_arat+m_bep+m_ret_q)/cons:.1f}% = {100*(prod_all+m_arat+m_bep+m_ret_q)/cons:.1f}% (should be 100)")
print()
print("  ANCHORED logic (retail link = consumer-paid price):")
m_ret_c = cons - bep; spread = cons - prod_all
print(f"    margins: A {m_arat:.2f} + B {m_bep:.2f} + R {m_ret_c:.2f} = {m_arat+m_bep+m_ret_c:.2f}")
print(f"    total spread = {spread:.2f}  -> gap = {m_arat+m_bep+m_ret_c-spread:.2f}")
print(f"    producer share {100*prod_all/cons:.1f}% + margins {100*(m_arat+m_bep+m_ret_c)/cons:.1f}% = {100*(prod_all+m_arat+m_bep+m_ret_c)/cons:.1f}%")
print()
print("  If BOTH fixed (producer = landing-linked only; retail anchor = consumer):")
m_arat2 = arat - prod_land
print(f"    margins: A {m_arat2:.2f} + B {m_bep:.2f} + R {m_ret_c:.2f} = {m_arat2+m_bep+m_ret_c:.2f}")
print(f"    spread (cons - prod_land) = {cons-prod_land:.2f}  gap = {m_arat2+m_bep+m_ret_c-(cons-prod_land):.2f}")
print(f"    producer share = {100*prod_land/cons:.1f}% ; margins% = {100*(m_arat2+m_bep+m_ret_c)/cons:.1f}% ; sum = {100*(prod_land+m_arat2+m_bep+m_ret_c)/cons:.1f}%")

print()
print("=" * 72)
print("D) PAIR DATA (for Wilcoxon signed-rank)")
print("=" * 72)
pair_rows = {}
for r in po:
    pid = r.get("Pair_ID")
    if pid:
        pair_rows.setdefault(pid, []).append(r)
n_pair_prices = sum(len(v) for v in pair_rows.values())
print(f"  distinct Pair_IDs in Price_Obs = {len(pair_rows)}; price rows carrying Pair_ID = {n_pair_prices}")
print(f"  expected 16 pairs x 2 sides = 32 rows")
for pid in sorted(pair_rows)[:8]:
    for r in pair_rows[pid]:
        print(f"   {pid}: {r['Respondent_ID']} {r.get('Actor_type'):12s} {r.get('Species_code')} "
              f"buy={r['buy_kg']} sell={r['sell_kg']} mkt={r.get('Market')}")
    print("   ---")

# build paired arrays (buyer's buy vs seller's sell)
pairs = {}
for r in po:
    pid = r.get("Pair_ID")
    if not pid:
        continue
    pairs.setdefault(pid, {"seller_sell": None, "buyer_buy": None})
    at = r.get("Actor_type")
    if at in ("Aratdar", "Bepari_Faria", "Khuchra"):
        if r["sell_kg"] is not None:
            pairs[pid]["seller_sell"] = r["sell_kg"]
        if r["buy_kg"] is not None:
            pairs[pid]["buyer_buy"] = r["buy_kg"]
# A pair should have the seller's sell row + buyer's buy row
valid = {k: v for k, v in pairs.items() if v["seller_sell"] is not None and v["buyer_buy"] is not None}
diffs = [v["seller_sell"] - v["buyer_buy"] for v in valid.values()]
print(f"  complete seller-sell/buyer-buy pairs: {len(valid)} / {len(pairs)}")
if diffs:
    print(f"  diff (seller sell - buyer buy) mean {np.mean(diffs):.2f} BDT/kg; "
          f"all-zero diffs? {all(abs(x) < 1e-9 for x in diffs)}")
    print(f"  diffs: {[round(x,2) for x in diffs]}")

print()
print("=" * 72)
print("E) SPECIES x MARKET quote counts (retailer sell + consumer paid)")
print("=" * 72)
mkt_list = ["M1", "M2", "M3", "M4", "M5", "M6"]
hdr = "  Species   " + "".join(f"{MK[m][:12]:>14s}" for m in mkt_list)
print(hdr)
for code in sorted(SP):
    cells = []
    for m in mkt_list:
        n_ret = sum(1 for r in po if r.get("Actor_type") == "Khuchra"
                    and r.get("Market") == m and r.get("Species_code") == code
                    and r["sell_kg"] is not None)
        n_con = sum(1 for r in cpf if r.get("Market") == m
                    and r.get("Species_code") == code and r["price_kg"] is not None)
        cells.append(f"{n_ret}+{n_con}")
    print(f"  {code} {SP[code]['Local_name']:10s} " + "".join(f"{c:>14s}" for c in cells))

print()
print("=" * 72)
print("F) DOC vs TABLE number spot-checks")
print("=" * 72)
t2 = pd.read_csv(os.path.join(ROOT, "analysis_outputs", "tables", "T2_Business_Scale.csv"))
a_cap = t2.loc[t2["Actor"] == "Aratdar", "Daily_capacity_kg_mean"].iloc[0]
r_cap = t2.loc[t2["Actor"] == "Retailer", "Daily_capacity_kg_mean"].iloc[0]
print(f"  Aratdar mean daily capacity (table) = {a_cap:.0f} kg | WRITING_GUIDE/README claim ~1,100 kg")
print(f"  Retailer mean daily capacity (table) = {r_cap:.0f} kg | WRITING_GUIDE claims ~120 kg")
t10 = pd.read_csv(os.path.join(ROOT, "analysis_outputs", "tables", "T10_Margin_Summary.csv"))
ps = t10.loc[t10["Level"] == "Producer share of consumer price", "Margin_pct_consumer"].iloc[0]
rm = t10.loc[t10["Level"] == "Retailer (khuchra margin)", "Margin_pct_consumer"].iloc[0]
print(f"  Producer share {ps}% | retailer margin {rm}% | A+B+R+PS = {3.4+8.5+16.7+73.9:.1f} (quoted docs) vs actual {rm}...")
