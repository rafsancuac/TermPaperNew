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
## If the user already set INPUT_FILE manually (in console, env var, or by editing this file
## below), respect it and do not overwrite.
## 1) R variable INPUT_FILE in global env
if (exists("INPUT_FILE", inherits = TRUE)) {
  try({
    pf <- get("INPUT_FILE", inherits = TRUE)
    if (is.character(pf) && length(pf) == 1 && file.exists(pf)) {
      INPUT_FILE <- normalizePath(pf, winslash = "/", mustWork = FALSE)
    }
  }, silent = TRUE)
}
## 2) Environment variable INPUT_FILE (e.g. INPUT_FILE=... Rscript ...)
if (!exists("INPUT_FILE", inherits = FALSE) || !file.exists(INPUT_FILE)) {
  ev <- Sys.getenv("INPUT_FILE", unset = "")
  if (nzchar(ev) && file.exists(ev)) {
    INPUT_FILE <- normalizePath(ev, winslash = "/", mustWork = FALSE)
    message(sprintf("[config] Using INPUT_FILE from env var: %s", INPUT_FILE))
  }
}

find_repo_root <- function() {
  d <- normalizePath(getwd(), winslash = "/", mustWork = FALSE)
  repeat {
    if (dir.exists(file.path(d, "04_data_filled"))) return(d)
    if (file.exists(file.path(d, "scripts", "R", "run_all.R"))) return(d)
    nd <- dirname(d)
    if (identical(nd, d)) return(NULL)
    d <- nd
  }
}
repo_root <- find_repo_root()

## Only auto-detect if INPUT_FILE is not already a valid file
need_auto <- TRUE
if (exists("INPUT_FILE", inherits = FALSE)) {
  if (is.character(INPUT_FILE) && length(INPUT_FILE) == 1 && file.exists(INPUT_FILE)) {
    need_auto <- FALSE
  }
}
if (need_auto) {
  if (!is.null(repo_root) && dir.exists(file.path(repo_root, "04_data_filled"))) {
    all_xlsx <- list.files(file.path(repo_root, "04_data_filled"),
                           pattern = "\\.xlsx$", full.names = TRUE, recursive = FALSE)
    all_xlsx <- all_xlsx[!grepl("^~\\$", basename(all_xlsx))]
    ## Exclude archive folder
    all_xlsx <- all_xlsx[!grepl("/archive/", all_xlsx, fixed = TRUE)]

    ## Priority 1: REAL FILLED file (actual field data for Chattogram)
    real_filled <- all_xlsx[grepl("REAL.*FILLED|FILLED.*REAL", basename(all_xlsx), ignore.case = TRUE)]
    ## Priority 2: any REAL file that is not EMPTY
    real_any <- all_xlsx[grepl("REAL", basename(all_xlsx), ignore.case = TRUE) &
                           !grepl("EMPTY", basename(all_xlsx), ignore.case = TRUE)]
    ## Priority 3: any filled file (legacy, simulated)
    legacy_filled <- all_xlsx[grepl("Filled", basename(all_xlsx), ignore.case = TRUE)]

    if (length(real_filled) > 0) {
      INPUT_FILE <- real_filled[1]
      message(sprintf("[config] Using REAL field data: %s", basename(INPUT_FILE)))
    } else if (length(real_any) > 0) {
      INPUT_FILE <- real_any[1]
      message(sprintf("[config] Using REAL file: %s", basename(INPUT_FILE)))
    } else if (length(legacy_filled) > 0) {
      INPUT_FILE <- legacy_filled[1]
      warning(sprintf("[config] Using legacy/simulated file %s (04_data_filled/archive/ contains simulated v2). For real Chattogram field data, fill %s and rename to *_REAL_FILLED.xlsx",
                      basename(INPUT_FILE), "Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx"))
    } else if (length(all_xlsx) > 0) {
      ## Only EMPTY template exists
      INPUT_FILE <- all_xlsx[1]
      warning(sprintf("[config] Only template found: %s — this is EMPTY (yellow cells not filled). Fill it with real field data from Chattogram (6 markets: M1 Fishery Ghat, M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli, M5 Bahaddarhat, M6 Patenga) and save as *_REAL_FILLED.xlsx", basename(INPUT_FILE)))
    } else {
      INPUT_FILE <- NULL
      warning("[config] No workbook found in 04_data_filled/ — expected REAL field data file, e.g.:\n  04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx\nCreate it from REAL_EMPTY.xlsx by filling yellow cells with Chattogram field data.")
    }
  } else if (!is.null(repo_root)) {
    INPUT_FILE <- NULL
    warning(sprintf("[config] Repo root found at %s but no 04_data_filled/ folder. Set INPUT_FILE manually, e.g.:\n  INPUT_FILE <- \"F:/TermPaperNew/04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx\"", repo_root))
  } else {
    INPUT_FILE <- NULL
    warning("[config] Could not locate the repo root (looked for 04_data_filled/ or scripts/R/run_all.R). Set INPUT_FILE explicitly, e.g.:\n  INPUT_FILE <- \"F:/TermPaperNew/04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx\"")
  }
}

## Final validation — with a helpful message for the empty-template case
if (is.null(INPUT_FILE) || !is.character(INPUT_FILE) || !file.exists(INPUT_FILE)) {
  stop(sprintf("[config] INPUT_FILE not found. Current value: %s\nSet it before running, e.g.:\n  INPUT_FILE <- \"F:/TermPaperNew/Marine_Fish_Marketing_Data_Entry (1).xlsx\"\n  source(\"scripts/R/run_all.R\")", deparse(if (exists("INPUT_FILE")) INPUT_FILE else NULL)))
}
INPUT_FILE <- normalizePath(INPUT_FILE, winslash = "/", mustWork = TRUE)

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
