# Data Cleaning Report
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
counted as structural blanks. 32 variable-by-form combinations are
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
17 of the numeric price cells (1.8%)
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
