# ============================================================================
# MS-499 — Marine Fish Marketing System of Chattogram, Bangladesh (March 2026)
# R ANALYTICS SUITE — config.R
# ----------------------------------------------------------------------------
# ONE place to set: (1) INPUT Excel workbook, (2) OUTPUT folder.
# Everything else in the suite derives from these two paths.
#
# HOW TO RUN (on your machine, from R or RStudio):
#   setwd("path/to/TermPaperNew")          # or set the working directory
#   source("scripts/R/run_all.R")          # runs the complete pipeline
#
# REQUIRED PACKAGES (one-time):
#   install.packages(c("readxl", "openxlsx"))
#
# All outputs are written to OUTPUT_DIR (default F:\TermPaperNew\Analysis):
#   tables/            Table 1..18 as CSV (utf-8, Excel-friendly)
#   charts/            Figure C1..C8 as PNG, 300 dpi, Times New Roman
#   R_Analysis_Summary.xlsx   all tables + Index sheet, publication styling
#   run_log.txt        console log of the session
# ============================================================================

## ---------------------------------------------------------------------------
## 1. INPUT WORKBOOK  ---------------------------------------------------------
##    >>> SET THIS when your final (real-data) Excel file is ready. <<<
##    Example:  INPUT_FILE <- "F:/TermPaperNew/Data/My_Final_Data.xlsx"
##    The default below points at the repo's filled workbook (simulated data,
##    currently in 04_data_filled/) so the suite can be tested end-to-end.
##    The repo root is located by walking upward from the working directory.
## ---------------------------------------------------------------------------
find_repo_root <- function() {
  d <- normalizePath(getwd(), winslash = "/")
  repeat {
    if (dir.exists(file.path(d, "04_data_filled"))) return(d)
    nd <- dirname(d)
    if (identical(nd, d)) return(NULL)
    d <- nd
  }
}
repo_root <- find_repo_root()
if (!is.null(repo_root)) {
  found <- list.files(file.path(repo_root, "04_data_filled"),
                      pattern = "\\.xlsx$", full.names = TRUE)
  found <- found[!grepl("^~\\$", basename(found))]
  if (length(found) > 0) {
    INPUT_FILE <- found[1]
  } else {
    INPUT_FILE <- NULL
    warning("[config] No filled workbook (*.xlsx) found in 04_data_filled/ - set INPUT_FILE.")
  }
} else {
  INPUT_FILE <- NULL
  warning("[config] Could not locate the repo root - set INPUT_FILE explicitly.")
}
stopifnot(!is.null(INPUT_FILE), file.exists(INPUT_FILE))

## ---------------------------------------------------------------------------
## 2. OUTPUT FOLDER  ----------------------------------------------------------
##    Windows default = F:\TermPaperNew\Analysis (as requested).
##    On any other OS we fall back to a dev folder inside the repo.
## ---------------------------------------------------------------------------
if (.Platform$OS.type == "windows") {
  OUTPUT_DIR <- "F:/TermPaperNew/Analysis"          # <<< your requested path
} else {
  OUTPUT_DIR <- file.path(getwd(), "analysis_outputs_r")   # dev/test mirror
}
if (interactive()) {   # override interactively at any time, e.g.:
  # OUTPUT_DIR <- choose.dir(default = OUTPUT_DIR, caption = "Output folder")
}

## ---------------------------------------------------------------------------
## 3. DESIGN CONSTANTS (must not be changed casually — mirror the methodology)
## ---------------------------------------------------------------------------
MAUND        <- 37.32      # 1 maund = 37.32 kg (Unit_Converter sheet)
LANDING      <- c("M1", "M6")   # landing-linked markets: first-sale proxy
MIN_CONS     <- 3          # min consumer-paid slips for a species share
ALPHA        <- 0.05       # significance level, two-sided
MKT_ORDER    <- paste0("M", 1:6)

## ---------------------------------------------------------------------------
## 4. TYPOGRAPHY & DESIGN  ----------------------------------------------------
##    Times New Roman throughout, per instruction. On Windows the font is used
##    natively; elsewhere we fall back to a serif face so scripts still run.
## ---------------------------------------------------------------------------
FONT_FAMILY <- "Times New Roman"
if (!.Platform$OS.type == "windows") {
  # no Times New Roman guarantee outside Windows -> use a metric-compatible serif
  FONT_FAMILY <- "serif"
  message("[config] Non-Windows session: figure font family = 'serif' ",
          "(Times New Roman is used automatically when run on Windows).")
}
## Publication palette (kept identical to the repo design system)
COL_PRODUCER <- "#1F4E79"; COL_ARATDAR <- "#D9822B"; COL_BEPARI <- "#2E8B57"
COL_RETAIL   <- "#C0504D"; COL_CONSUMER <- "#7B5EA7"
HDR_FILL     <- "1F4E79";  BAND_FILL    <- "F2F6FA"

## Output sub-folders (created by run_all.R)
DIR_TABLES  <- file.path(OUTPUT_DIR, "tables")
DIR_CHARTS  <- file.path(OUTPUT_DIR, "charts")
XLSX_OUT    <- file.path(OUTPUT_DIR, "R_Analysis_Summary.xlsx")
LOG_FILE    <- file.path(OUTPUT_DIR, "run_log.txt")

## ---------------------------------------------------------------------------
## 5. START THE SESSION LOG  --------------------------------------------------
## ---------------------------------------------------------------------------
log_start <- function() {
  dir.create(OUTPUT_DIR, recursive = TRUE, showWarnings = FALSE)
  dir.create(DIR_TABLES, recursive = TRUE, showWarnings = FALSE)
  dir.create(DIR_CHARTS, recursive = TRUE, showWarnings = FALSE)
  sink(LOG_FILE, split = TRUE)
  cat("MS-499 R analysis session\n", format(Sys.time()), "\n")
  cat("Input :", INPUT_FILE, "\n")
  cat("Output:", OUTPUT_DIR, "\n\n")
}
