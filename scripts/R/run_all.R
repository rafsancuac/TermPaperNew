# ============================================================================
# run_all.R — MS-499 R ANALYTICS SUITE (master runner)
# ----------------------------------------------------------------------------
#   source("scripts/R/run_all.R")            # from the repo root
#
# Pipeline:
#   1. read the input workbook (config.R: INPUT_FILE - set your final file)
#   2. descriptive tables  T1..T11 (+T2b)  -> OUTPUT_DIR/tables/*.csv
#   3. inferential tables  T12..T18        -> OUTPUT_DIR/tables/*.csv
#   4. figures C1..C8 (300 dpi, Times New Roman) -> OUTPUT_DIR/charts/
#   5. R_Analysis_Summary.xlsx (styled workbook + Index)
#   6. quality gates: margins telescope & PS + spread% = 100
# All output goes to OUTPUT_DIR (F:/TermPaperNew/Analysis on Windows).
# ============================================================================

rm(list = setdiff(ls(), c("INPUT_FILE", "OUTPUT_DIR")))   # clean session, keep manual overrides
options(warn = 1)                                  # warnings become visible
if (!requireNamespace("readxl", quietly = TRUE) ||
    !requireNamespace("openxlsx", quietly = TRUE)) {
  stop("Install required packages first:  install.packages(c('readxl','openxlsx'))")
}

## ---- 0. configuration & helpers -------------------------------------------
source("scripts/R/config.R")
source("scripts/R/helpers.R")
log_start()

## ---- 1. data loading & descriptive tables ---------------------------------
source("scripts/R/tables_descriptive.R")
DESC <- build_descriptive()

## ---- 2. inferential tables --------------------------------------------------
source("scripts/R/tables_inferential.R")
INF  <- build_inferential()

## assemble named table registry ----------------------------------------------
TABLES <- setNames(c(DESC, INF), vapply(c(DESC, INF), `[[`, "", "name"))

## ---- 3. write CSVs ------------------------------------------------------------
invisible(lapply(TABLES, function(t) {
  f <- file.path(DIR_TABLES, paste0(t$name, ".csv"))
  write_tbl(t$df, f)
  cat(sprintf("  table  %-42s (%d rows)\n", basename(f), nrow(t$df)))
}))

## ---- 4. figures ----------------------------------------------------------------
source("scripts/R/figures.R")
suppressWarnings(build_figures(TABLES))

## ---- 5. Excel summary ---------------------------------------------------------
source("scripts/R/excel_out.R")
write_excel(TABLES)

## ---- 6. quality gates ----------------------------------------------------------
gates_ok <- quality_gates(TABLES)

cat("\nDONE - R analysis outputs in:", OUTPUT_DIR, "\n")
if (!gates_ok) warning("QUALITY GATES FAILED - inspect the tables before use.")
sink()
