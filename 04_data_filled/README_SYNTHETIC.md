# 04_data_filled — the dataset the analysis runs on

## ⚠️ Provenance — read before citing anything

The active workbook is **SYNTHETIC**. It was produced by
`scripts/generate_synthetic_data.py` from `random.Random(20260315)`; every price,
cost, age, problem mention and date in it is drawn from the distributions hard-coded
in that script.

- **Active:** `SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx` (seed 20260315)
- **Blank template for real collection:** `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx`

This dataset exists so the questionnaire structure, the QC gate, the audit script, the
statistical battery and the reporting templates can be exercised end to end before —
or instead of — fieldwork. It is **not observed field data**, and no figure derived
from it may be presented as an empirical finding about Chattogram's markets.

## Files

| File | Role |
|---|---|
| `SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx` | Active synthetic dataset — all 16 sheets populated |
| `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx` | Blank template (IDs pre-filled, yellow cells empty) for real collection |

## Design encoded in the workbook

- **6 markets:** M1 Fishery Ghat (landing), M2 Chawkbazar, M3 Kazir Dewri,
  M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga (landing-linked)
- **120 respondents:** 30 aratdar + 30 bepari/faria + 30 retailer + 30 consumer
- **10 focal species** S01–S10; **1 maund = 37.32 kg**; K/D flags for
  "did not buy today" / "declined to answer"
- **Survey window:** 2–7 March 2026 (2 March pilot, 3–7 March collection)
- **Chain:** fisher → aratdar (auction) → bepari/faria → retailer → consumer

## Regenerating

```bash
python scripts/generate_synthetic_data.py
python scripts/qc_recalc.py 04_data_filled/SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx
```

`qc_recalc.py` reimplements the derived (blue) columns and the 24 QC checks in Python
and writes the results as literal values, so the workbook reads identically in Excel,
in pandas and in R **without needing a spreadsheet engine to recalculate it**. Do not
skip it: without it the QC cells are empty and `verify_filled.py` would be checking
nothing.

## Switching to real field data

1. Open `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx`
2. Fill **only the yellow cells**; leave grey ID columns and blue formula columns alone
3. Record a unit (Maund/Kg) for every price; use `K` if nothing was bought that day,
   `D` if the respondent declined
4. Keep Cash + MFS + Credit = 100; link buyer–seller pairs with `Pair_ID`
5. Save as `*_REAL_FILLED.xlsx` in this folder

`run_analysis.find_default_data()` prefers `SYNTHETIC_*_Filled.xlsx` first and
`*REAL*FILLED*.xlsx` second, so to switch engines entirely, move the synthetic file to
`archive/` (or delete it) and the real workbook is picked up automatically — nothing
else in the pipeline changes.

## Running the analysis

```bash
python scripts/verify_filled.py          # 24-check QC gate
python scripts/run_analysis.py           # T1–T11, T4b, T19 + charts
python scripts/extend_analysis.py        # T12–T18 inferential battery
python scripts/clean_data.py             # cleaning log, outlier flags
python scripts/make_charts_v2.py         # publication figures
python scripts/review_audit.py           # independent 65-check audit
```

Or, in R / RStudio, one script does all of the above:

```r
source("scripts/R/MS499_full_analysis.R")
```
