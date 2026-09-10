#!/usr/bin/env python3
"""Re-embed the v2 dataset reference values into scripts/R/run_analysis.R
chk() calls (Python pipeline outputs are the source of truth)."""
import re
import pandas as pd

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RFILE = os.path.join(ROOT, "scripts", "R", "run_analysis.R")
T = lambda name: pd.read_csv(os.path.join(ROOT, "analysis_outputs", "tables", name + ".csv"))

src = open(RFILE, encoding="utf-8").read()
orig = src

t1 = T("T1_Respondent_Profile")
t2 = T("T2_Business_Scale")
t5 = T("T5_Payment_Methods")
t3 = T("T3_Price_Chain")
t11 = T("T11_Retail_Price_by_Market")
t12b = T("T12b_Wilcoxon_Result")
t16 = T("T16_Stratum_Margin_MannWhitney")
t17 = T("T17_Retailer_MC_Profit_Spearman")

t15 = T("T15_Payment_Actor_ChiSquare")
chi_row = t15[t15["Actor"].str.startswith("chi-square")]["MFS_share_pct"].iloc[0]
m = re.match(r"chi2=([\d.]+), df=(\d+), p=([\d.]+)", str(chi_row))
chi2, df_, p15 = m.groups()

all_row = t3[t3["Species_code"] == "ALL"].iloc[0]
producer, aratdar, bepari = all_row["Producer_BDT_kg"], all_row["Aratdar_sell_BDT_kg"], all_row["Bepari_sell_BDT_kg"]
retail, consumer, ps = all_row["Retailer_sell_BDT_kg"], all_row["Consumer_paid_BDT_kg"], all_row["Producer_share_pct"]

sp_cons = {r["Species_code"]: r["Consumer_paid_BDT_kg"] for _, r in t3.iterrows()}
sp_ret = {r["Species_code"]: r["Retailer_sell_BDT_kg"] for _, r in t3.iterrows()}

def t16v(actor, col):
    return float(t16[t16["Actor"] == actor][col].iloc[0])

def mwu(pair):
    return t16[t16["Actor"] == f"Mann-Whitney U: {pair}"]["Mean_margin_BDT_kg"].iloc[0]

t17row = t17[t17["Respondent_ID"].str.startswith("Spearman")].iloc[0]
rho, p17 = t17row["MC_BDT_kg"], t17row["Net_profit_BDT_kg"]

def fmt(x):
    """Match R literal style: trailing-zero-free but keep >=2 decimals."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    if "." not in s:
        s += ".0"
    return s

REPL = [
    # counts
    ('chk("Price_Observations rows",                nrow(PO), 463)',
     'chk("Price_Observations rows",                nrow(PO), 492)'),
    ('chk("Buy price cells K (closed today)",       sum(buy_status == "K"), 48)',
     'chk("Buy price cells K (closed today)",       sum(buy_status == "K"), 53)'),
    ('chk("Sell price cells K (closed today)",      sum(sell_status == "K"), 45)',
     'chk("Sell price cells K (closed today)",      sum(sell_status == "K"), 62)'),
    ('chk("Sell price cells D (refused)",           sum(sell_status == "D"), 19)',
     'chk("Sell price cells D (refused)",           sum(sell_status == "D"), 16)'),
    ('chk("Consumer focal purchase rows",           nrow(CPF), 69)',
     'chk("Consumer focal purchase rows",           nrow(CPF), 75)'),
    ('chk("Focal purchases bought today (Yes)",     nrow(CPF_yes), 52)',
     'chk("Focal purchases bought today (Yes)",     nrow(CPF_yes), 64)'),
    # T1
    ('chk("T1 Aratdar mean age (years)",            T1$Age_mean_years[1], 44.13)',
     f'chk("T1 Aratdar mean age (years)",            T1$Age_mean_years[1], {fmt(t1.iloc[0]["Age_mean_years"])})'),
    ('chk("T1 Bepari mean age (years)",             T1$Age_mean_years[2], 40.1)',
     f'chk("T1 Bepari mean age (years)",             T1$Age_mean_years[2], {fmt(t1.iloc[1]["Age_mean_years"])})'),
    ('chk("T1 Faria mean age (years)",              T1$Age_mean_years[3], 40.4)',
     f'chk("T1 Faria mean age (years)",              T1$Age_mean_years[3], {fmt(t1.iloc[2]["Age_mean_years"])})'),
    ('chk("T1 Retailer mean age (years)",           T1$Age_mean_years[4], 38.77)',
     f'chk("T1 Retailer mean age (years)",           T1$Age_mean_years[4], {fmt(t1.iloc[3]["Age_mean_years"])})'),
    ('chk("T1 Aratdar mean experience (years)",     T1$Years_mean[1], 18.73)',
     f'chk("T1 Aratdar mean experience (years)",     T1$Years_mean[1], {fmt(t1.iloc[0]["Years_in_business_mean"])})'),
    ('chk("T1 Retailer mean experience (years)",    T1$Years_mean[4], 12.77)',
     f'chk("T1 Retailer mean experience (years)",    T1$Years_mean[4], {fmt(t1.iloc[3]["Years_in_business_mean"])})'),
    # T2
    ('chk("T2 Aratdar mean daily capacity (kg)",    T2$Daily_capacity_kg_mean[1], 797.4)',
     f'chk("T2 Aratdar mean daily capacity (kg)",    T2$Daily_capacity_kg_mean[1], {fmt(t2.iloc[0]["Daily_capacity_kg_mean"])})'),
    ('chk("T2 Bepari/Faria mean daily capacity (kg)", T2$Daily_capacity_kg_mean[2], 204.51)',
     f'chk("T2 Bepari/Faria mean daily capacity (kg)", T2$Daily_capacity_kg_mean[2], {fmt(t2.iloc[1]["Daily_capacity_kg_mean"])})'),
    ('chk("T2 Retailer mean daily capacity (kg)",   T2$Daily_capacity_kg_mean[3], 99.95)',
     f'chk("T2 Retailer mean daily capacity (kg)",   T2$Daily_capacity_kg_mean[3], {fmt(t2.iloc[2]["Daily_capacity_kg_mean"])})'),
    # T5
    ('chk("T5 Aratdar mean cash share (%)",         T5$Cash_pct_mean[1], 67.6)',
     f'chk("T5 Aratdar mean cash share (%)",         T5$Cash_pct_mean[1], {fmt(t5.iloc[0]["Cash_pct_mean"])})'),
    ('chk("T5 Bepari mean cash share (%)",          T5$Cash_pct_mean[2], 63.87)',
     f'chk("T5 Bepari mean cash share (%)",          T5$Cash_pct_mean[2], {fmt(t5.iloc[1]["Cash_pct_mean"])})'),
    ('chk("T5 Retailer mean cash share (%)",        T5$Cash_pct_mean[3], 55.23)',
     f'chk("T5 Retailer mean cash share (%)",        T5$Cash_pct_mean[3], {fmt(t5.iloc[2]["Cash_pct_mean"])})'),
    ('    T5c$pct[T5c$Method == "bKash"], 36.7)',
     '    T5c$pct[T5c$Method == "bKash"], 20.0)'),
    # chain completeness + T3/T10 pool
    ('chk("Chain-complete species count (MIN_CONS)", length(complete_codes), 8)',
     'chk("Chain-complete species count (MIN_CONS)", length(complete_codes), 10)'),
    ('chk("T3 ALL producer price (BDT/kg)",         P$producer, 601.41)',
     f'chk("T3 ALL producer price (BDT/kg)",         P$producer, {fmt(producer)})'),
    ('chk("T3 ALL aratdar sell (BDT/kg)",           P$aratdar, 629.25)',
     f'chk("T3 ALL aratdar sell (BDT/kg)",           P$aratdar, {fmt(aratdar)})'),
    ('chk("T3 ALL bepari sell (BDT/kg)",            P$bepari, 728.83)',
     f'chk("T3 ALL bepari sell (BDT/kg)",            P$bepari, {fmt(bepari)})'),
    ('chk("T3 ALL retailer quote (BDT/kg)",         P$retail, 869.5)',
     f'chk("T3 ALL retailer quote (BDT/kg)",         P$retail, {fmt(retail)})'),
    ('chk("T3 ALL consumer paid (BDT/kg)",          P$consumer, 847.8)',
     f'chk("T3 ALL consumer paid (BDT/kg)",          P$consumer, {fmt(consumer)})'),
    ('chk("T10 aratdar margin (BDT/kg)",            P$aratdar - P$producer, 27.84)',
     f'chk("T10 aratdar margin (BDT/kg)",            P$aratdar - P$producer, {fmt(aratdar - producer)})'),
    ('chk("T10 bepari margin (BDT/kg)",             P$bepari - P$aratdar, 99.58)',
     f'chk("T10 bepari margin (BDT/kg)",             P$bepari - P$aratdar, {fmt(bepari - aratdar)})'),
    ('chk("T10 retailer margin (BDT/kg)",           P$consumer - P$bepari, 118.97)',
     f'chk("T10 retailer margin (BDT/kg)",           P$consumer - P$bepari, {fmt(consumer - bepari)})'),
    ('chk("T10 total marketing spread (BDT/kg)",    P$consumer - P$producer, 246.39)',
     f'chk("T10 total marketing spread (BDT/kg)",    P$consumer - P$producer, {fmt(consumer - producer)})'),
    ('chk("T10 producer share (%)",                 100 * P$producer / P$consumer, 70.9)',
     f'chk("T10 producer share (%)",                 100 * P$producer / P$consumer, {fmt(ps)})'),
    # per-species consumer prices (labels cleaned: no longer descriptive-only)
    ('chk("T3 S01 Ilish consumer price (BDT/kg)",   chains$S01$consumer, 1420)',
     f'chk("T3 S01 Ilish consumer price (BDT/kg)",   chains$S01$consumer, {fmt(sp_cons["S01"])})'),
    ('chk("T3 S02 Rupchanda consumer price",        chains$S02$consumer, 1615)',
     f'chk("T3 S02 Rupchanda consumer price",        chains$S02$consumer, {fmt(sp_cons["S02"])})'),
    ('chk("T3 S03 Lakkha consumer price",           chains$S03$consumer, 1033.33)',
     f'chk("T3 S03 Lakkha consumer price",           chains$S03$consumer, {fmt(sp_cons["S03"])})'),
    ('chk("T3 S04 Koral consumer price",            chains$S04$consumer, 885)',
     f'chk("T3 S04 Koral consumer price",            chains$S04$consumer, {fmt(sp_cons["S04"])})'),
    ('chk("T3 S05 Surma consumer price",            chains$S05$consumer, 585)',
     f'chk("T3 S05 Surma consumer price",            chains$S05$consumer, {fmt(sp_cons["S05"])})'),
    ('chk("T3 S06 Churi consumer price",            chains$S06$consumer, 446.54)',
     f'chk("T3 S06 Churi consumer price",            chains$S06$consumer, {fmt(sp_cons["S06"])})'),
    ('chk("T3 S07 Poa consumer price",              chains$S07$consumer, 530)',
     f'chk("T3 S07 Poa consumer price",              chains$S07$consumer, {fmt(sp_cons["S07"])})'),
    ('chk("T3 S08 Kankoita consumer price (n=1, descriptive)", chains$S08$consumer, 330)',
     f'chk("T3 S08 Kankoita consumer price",          chains$S08$consumer, {fmt(sp_cons["S08"])})'),
    ('chk("T3 S09 Loitta consumer price",           chains$S09$consumer, 267.5)',
     f'chk("T3 S09 Loitta consumer price",           chains$S09$consumer, {fmt(sp_cons["S09"])})'),
    ('chk("T3 S10 Harina consumer price (n=1, descriptive)", chains$S10$consumer, 215)',
     f'chk("T3 S10 Harina consumer price",           chains$S10$consumer, {fmt(sp_cons["S10"])})'),
    ('chk("T3 S01 Ilish retailer quote (BDT/kg)",   chains$S01$retail, 1486.96)',
     f'chk("T3 S01 Ilish retailer quote (BDT/kg)",   chains$S01$retail, {fmt(sp_ret["S01"])})'),
    ('chk("T11 S01 Ilish retail at Fishery Ghat",   T11["S01", "M1"], 1416.0)',
     f'chk("T11 S01 Ilish retail at Fishery Ghat",   T11["S01", "M1"], {fmt(t11.iloc[0]["Fishery Ghat"])})'),
    # T12b
    ('chk("T12b usable matched pairs",            T12b$Value[1], 14)',
     f'chk("T12b usable matched pairs",            T12b$Value[1], {int(t12b.iloc[0]["Value"])})'),
    ('chk("T12b pairs with non-zero difference",  T12b$Value[2], 13)',
     f'chk("T12b pairs with non-zero difference",  T12b$Value[2], {int(t12b.iloc[1]["Value"])})'),
    ('chk("T12b Wilcoxon W (scipy convention)",   T12b$Value[5], 23.0, tol = 0.51)',
     f'chk("T12b Wilcoxon W (scipy convention)",   T12b$Value[5], {t12b.iloc[4]["Value"]}, tol = 0.51)'),
    ('chk("T12b Wilcoxon p-value",                T12b$Value[7], 0.1157, tol = 0.002)',
     f'chk("T12b Wilcoxon p-value",                T12b$Value[7], {t12b.iloc[5]["Value"]}, tol = 0.002)'),
    # T15
    ('chk("T15 chi-square statistic",               T15b$chi2, 1.22)',
     f'chk("T15 chi-square statistic",               T15b$chi2, {chi2})'),
    ('chk("T15 chi-square df",                      T15b$df, 4)',
     f'chk("T15 chi-square df",                      T15b$df, {df_})'),
    ('chk("T15 chi-square p-value",                 T15b$p, 0.8749, tol = 0.002)',
     f'chk("T15 chi-square p-value",                 T15b$p, {p15}, tol = 0.002)'),
    # T16
    ('    T16$Median_margin_BDT_kg[T16$Actor == "Aratdar"], 30.14)',
     f'    T16$Median_margin_BDT_kg[T16$Actor == "Aratdar"], {fmt(t16v("Aratdar", "Median_margin_BDT_kg"))})'),
    ('    T16$Median_margin_BDT_kg[T16$Actor == "Bepari_Faria"], 83.74)',
     f'    T16$Median_margin_BDT_kg[T16$Actor == "Bepari_Faria"], {fmt(t16v("Bepari_Faria", "Median_margin_BDT_kg"))})'),
    ('    T16$Median_margin_BDT_kg[T16$Actor == "Khuchra"], 182.0)',
     f'    T16$Median_margin_BDT_kg[T16$Actor == "Khuchra"], {fmt(t16v("Khuchra", "Median_margin_BDT_kg"))})'),
    ('    T16$Mean_margin_BDT_kg[T16$Actor == "Aratdar"], 30.62)',
     f'    T16$Mean_margin_BDT_kg[T16$Actor == "Aratdar"], {fmt(t16v("Aratdar", "Mean_margin_BDT_kg"))})'),
    ('    T16$Mean_margin_BDT_kg[T16$Actor == "Bepari_Faria"], 84.07)',
     f'    T16$Mean_margin_BDT_kg[T16$Actor == "Bepari_Faria"], {fmt(t16v("Bepari_Faria", "Mean_margin_BDT_kg"))})'),
    ('    T16$Mean_margin_BDT_kg[T16$Actor == "Khuchra"], 176.02)',
     f'    T16$Mean_margin_BDT_kg[T16$Actor == "Khuchra"], {fmt(t16v("Khuchra", "Mean_margin_BDT_kg"))})'),
    ('      "Mann-Whitney U: Aratdar vs Bepari_Faria"], "U=0, p<0.0001")',
     f'      "Mann-Whitney U: Aratdar vs Bepari_Faria"], "{mwu("Aratdar vs Bepari_Faria")}")'),
    ('      "Mann-Whitney U: Aratdar vs Khuchra"], "U=0, p<0.0001")',
     f'      "Mann-Whitney U: Aratdar vs Khuchra"], "{mwu("Aratdar vs Khuchra")}")'),
    ('      "Mann-Whitney U: Bepari_Faria vs Khuchra"], "U=10, p<0.0001")',
     f'      "Mann-Whitney U: Bepari_Faria vs Khuchra"], "{mwu("Bepari_Faria vs Khuchra")}")'),
    # T17
    ('chk("T17 Spearman rho (MC vs net margin)",  T17b$rho, 0.43, tol = 0.006)',
     f'chk("T17 Spearman rho (MC vs net margin)",  T17b$rho, {rho}, tol = 0.006)'),
    ('chk("T17 Spearman p-value",                 T17b$p, 0.0177, tol = 0.002)',
     f'chk("T17 Spearman p-value",                 T17b$p, {p17}, tol = 0.002)'),
    ('chk("T17 retailer n",                       T17b$n, 30)',
     'chk("T17 retailer n",                       T17b$n, 30)'),
]

n_ok = 0
for old, new in REPL:
    if old in src:
        src = src.replace(old, new, 1)
        n_ok += 1
    else:
        print("!! NOT FOUND:", old[:80])

if src != orig:
    open(RFILE, "w", encoding="utf-8").write(src)
print(f"patched {n_ok}/{len(REPL)} lines -> {RFILE}")
