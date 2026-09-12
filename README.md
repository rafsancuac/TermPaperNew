# MS-499 — Marine Fish Marketing System of Chattogram, Bangladesh

Term paper analysing the marketing channels, costs, margins and price spread of ten
commercially important marine fish species in the Chattogram metropolitan region.

This repository contains **three files**: the data, the analysis script and the paper.

---

## ⚠️ Data provenance — read before citing anything

**The dataset is synthetic.** `MS499_Chattogram_Marine_Fish_Data.xlsx` was generated
from a fixed random seed (20260315) to reproduce the survey design, the instrument
structure and the cost–price relationships of the Chattogram study. It exists so that
the questionnaire, the quality-control gate, the statistical battery and the reporting
conventions could be validated end to end before fieldwork.

**It is not observed field data.** No figure in the paper may be cited as an empirical
finding about Chattogram's markets. Presenting it as a real survey would be research
misconduct. Section 3.13, Section 5.5 and Appendix B of the paper state exactly what
must be redone when real data replace the workbook.

---

## Contents

| File | What it is |
|---|---|
| `MS499_Chattogram_Marine_Fish_Data.xlsx` | The analysis dataset. 16 sheets: Forms A/B/R/M/C, codebooks, derived columns and a 24-check QC dashboard (currently 24/24). 120 respondents across 6 markets, 10 focal species, 491 price observations, 15 matched buyer–seller pairs. |
| `MS499_full_analysis.R` | One self-contained script that reproduces every number in the paper: 23 tables (T1–T19), 14 charts and a summary workbook. |
| `MS499_Term_Paper.docx` | The finished paper — five chapters, APA 7th edition, 15 tables and 6 figures, a single reference list placed before three appendices. |

---

## Running the analysis in R

Put the script and the workbook in the **same folder**, then in the R console:

```r
install.packages(c("readxl", "openxlsx"))   # one time only
setwd("path/to/that/folder")
source("MS499_full_analysis.R")
```

Or from a terminal: `Rscript MS499_full_analysis.R`

**Requires base R plus `readxl` and `openxlsx` only** — no dplyr, tidyr or ggplot2, so it
runs on a stock R 4.x installation. Tested against R 4.5.0.

Outputs are written to a new folder `analysis_outputs_r/` containing `tables/` (23 CSVs),
`charts/` (14 PNGs) and `R_Analysis_Summary.xlsx`. Every figure printed in the paper is
among them (F1–F4, A1–A2), so the illustrations regenerate alongside the numbers. The
remaining charts (C1–C5, C7, F5, F8) are additional views not carried into the paper.

The script ends by printing a **verification report** — every table with its row and
column count, the headline figures, and three reproducibility gates:

```
  [PASS] segment margins telescope to the spread (251.34 vs 251.34)
  [PASS] producer share + spread = 100 (100.0)
  [PASS] Table 3 pooled PS = Table 10 PS (72.4 vs 72.4)

RESULT: ALL CHECKS PASSED  -- 23/23 tables written, 3/3 gates passed
```

### Using real field data

1. Fill the workbook's **yellow cells only** — grey ID columns and blue derived columns
   must not be edited.
2. Give a unit (Maund/Kg) for every price. Use `K` if nothing was bought that day, `D`
   if the respondent declined.
3. Keep Cash + MFS + Credit = 100. Link buyer–seller pairs with `Pair_ID`.
4. Save it beside the script and set `INPUT_FILE` at the top of
   `MS499_full_analysis.R` to its file name (or set it to `""` to auto-detect the only
   `.xlsx` in the folder).

Nothing else changes — every table, chart and figure regenerates.

---

## Headline figures from the current dataset

Synthetic, and valid only as a demonstration of the pipeline:

- Producer's share of the consumer price: **72.4 %** (71.9 % volume-weighted)
- Total price spread: **251.35 BDT/kg (27.6 %)**
- Segment margins: aratdar 29.94 (3.3 %), bepari/faria 104.87 (11.5 %), retailer 116.54 (12.8 %) BDT/kg
- Marketing cost per kg: aratdar 7.12, bepari/faria 78.12, retailer 50.95
- Gross marketing margin 27.6 %; net marketing margin 12.7 %
- Shepherd efficiency index 2.35 (consumer-referenced), 1.70 (producer-referenced)
- Chain-complete species (6 of 10): Ilish, Rupchanda, Koral, Surma, Churi, Poa

---

## Design in one table

| Item | Detail |
|---|---|
| Markets | M1 Fishery Ghat, M6 Patenga (landing-linked); M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat (retail) |
| Respondents | 120 — 30 aratdar, 30 bepari/faria, 30 khuchra retailers, 30 exit-intercepted consumers |
| Species | S01–S10, Ilish to Harina, spanning high/medium/low price tiers |
| Chain | Fisher → aratdar (auction) → bepari/faria → retailer → consumer |
| Units | BDT per kilogram; 1 maund = 37.32 kg |
| Survey window | 2 March 2026 (pilot), 3–7 March 2026 (collection) |
| Tests | Kruskal–Wallis + Dunn (Holm), Mann–Whitney U, Wilcoxon signed-rank, chi-square with exact fallback, Spearman, Shapiro–Wilk screening |

---

## Notes on the paper

- **Numbering is chapter-qualified**: Tables 3.1–3.4 in Chapter 3, 4.1–4.10 in
  Chapter 4, A.1 in the appendices. Figures are 4.1–4.5 and A.1.
- **All 19 references sit in one list at the very end of the document, immediately
  before the appendices**, and every entry is complete with volume, issue and page or
  DOI details.
- The paper is set in the house style of `Methodology_v4_FIXED`: A4, Times New Roman,
  12 pt body at 1.32 line height with 1-inch margins, 12 pt bold headings at every
  level, 10 pt tables with horizontal rules only, and 12 pt italic equations numbered
  right.
- Three objectives only, and every chapter is framed as pursuing those three.
- No em dashes anywhere in the text.
- The hilsa conservation ban (reported 1 March – 30 April 2026) is treated as a caveat on
  interpreting the Ilish results, not as a measured variable. Chattogram is not among the
  six designated sanctuary districts.

Earlier drafts, the source methodology text, questionnaires, the Python pipeline and all
intermediate outputs remain available in this repository's Git history.
