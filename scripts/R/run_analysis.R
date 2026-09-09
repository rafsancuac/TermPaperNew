# =====================================================================
# MS-499 TERM PAPER - MARINE FISH MARKETING SYSTEM, CHATTOGRAM
# SURVEY 02-07 MARCH 2026
#
# R VERIFICATION PIPELINE
# -----------------------
# Mirrors the repository's Python analysis exactly:
#   scripts/run_analysis.py      (Tables 1, 2, 3, 5, 10, 11 ...)
#   scripts/extend_analysis.py   (Tables 12b, 14, 15, 16, 17 ...)
#   scripts/clean_data.py        (K/D flag handling, headline checks)
#
# HOW TO RUN (on your own PC):
#   1. Install R from https://cran.r-project.org (R 4.1 or newer).
#   2. Clone/download this repository, e.g. to C:/TermPaperNew
#   3. Open R (or RStudio), then:
#        setwd("C:/TermPaperNew/scripts/R")   # anywhere inside repo
#        source("run_analysis.R", encoding="UTF-8")
#   4. The console prints a numbered VERIFICATION REPORT; every line
#      shows the value computed in R and the reference value produced
#      by the Python pipeline, plus MATCH / MISMATCH.
#   5. Copy the whole console output and send it back for review.
#
# Outputs:
#   r_outputs/tables/*.csv   - every table recomputed in R
#   r_outputs/charts/*.png   - ggplot2 versions of the main figures
#                              (Times New Roman, 1000 dpi) - skipped
#                              automatically if ggplot2 is missing.
#
# NOTE: the reference values below come from the SIMULATED dataset
# currently in 04_data_filled/. After real field data entry, re-run
# the Python pipeline first; reference values then update from
# analysis_outputs/tables/*.csv (the R script also writes its own
# tables for direct diffing).
# =====================================================================

## --------------------------------------------------------------------
## 0. SETUP
## --------------------------------------------------------------------
options(width = 120)
CRAN <- "https://cloud.r-project.org"

if (!requireNamespace("openxlsx", quietly = TRUE))
  install.packages("openxlsx", repos = CRAN)
library(openxlsx)

MAKE_FIGURES <- TRUE  # set FALSE to skip the ggplot2 figures
if (MAKE_FIGURES && !requireNamespace("ggplot2", quietly = TRUE)) {
  message("ggplot2 not installed - figures will be skipped.")
  MAKE_FIGURES <- FALSE
}

MAUND  <- 37.32            # 1 maund = 37.32 kg (template Unit_Converter)
LANDING <- c("M1", "M6")   # first-sale observable markets (Methodology V4)
MIN_CONS <- 3               # chain-complete needs >=3 consumer-paid quotes

## Locate the repository root (works when run from repo root, scripts/,
## scripts/R/, or set ROOT manually, e.g. ROOT <- "C:/TermPaperNew")
find_root <- function() {
  cands <- getwd()
  for (i in 1:4) {
    for (sub in c("", "TermPaperNew")) {
      p <- file.path(cands, sub)
      if (dir.exists(file.path(p, "04_data_filled"))) {
        return(normalizePath(p))
      }
    }
    cands <- dirname(cands)
  }
  stop("Could not locate 04_data_filled/ - set ROOT manually at the top.")
}
ROOT <- find_root()
OUT_T <- file.path(ROOT, "r_outputs", "tables")
OUT_C <- file.path(ROOT, "r_outputs", "charts")
dir.create(OUT_T, recursive = TRUE, showWarnings = FALSE)
if (MAKE_FIGURES) dir.create(OUT_C, recursive = TRUE, showWarnings = FALSE)

data_candidates <- list.files(file.path(ROOT, "04_data_filled"),
                              pattern = "\\.xlsx$", full.names = TRUE)
data_candidates <- data_candidates[!grepl("^~\\$", basename(data_candidates))]
if (length(data_candidates) == 0)
  stop("No filled workbook in 04_data_filled/")
DATA_PATH <- data_candidates[1]
cat("=====================================================================\n")
cat("R verification pipeline - MS-499 marine fish marketing survey\n")
cat("Repository :", ROOT, "\n")
cat("Workbook   :", DATA_PATH, "\n")
cat("R version  :", R.version.string, "\n")
cat("=====================================================================\n\n")

## --------------------------------------------------------------------
## Small helpers (identical semantics to the Python versions)
## --------------------------------------------------------------------
num <- function(x) suppressWarnings(as.numeric(x))
clean_names <- function(df) {
  ok <- !is.na(names(df)) & names(df) != ""
  df[, ok, drop = FALSE]
}
cell_status <- function(x) {
  x <- trimws(as.character(x))
  ifelse(is.na(x), "blank",
         ifelse(toupper(x) == "K", "K",
                ifelse(toupper(x) == "D", "D", "value")))
}
## BDT/kg price with fallback recomputation from the raw quote
ppk <- function(raw, unit, cached) {
  out <- num(cached)
  rv  <- num(raw)
  uv  <- trimws(as.character(unit))
  need <- is.na(out)
  out[need] <- ifelse(is.na(rv[need]), NA_real_,
                      ifelse(!is.na(uv[need]) & uv[need] == "Maund",
                             rv[need] / MAUND, rv[need]))
  round(out, 2)
}
## quantity in kg with fallback recomputation
qkg <- function(raw, unit, cached) {
  out <- num(cached)
  rv  <- num(raw)
  uv  <- trimws(as.character(unit))
  need <- is.na(out)
  out[need] <- ifelse(is.na(rv[need]), NA_real_,
                      ifelse(!is.na(uv[need]) & uv[need] == "Maund",
                             rv[need] * MAUND, rv[need]))
  round(out, 2)
}

## --------------------------------------------------------------------
## 1. READ THE WORKBOOK (headers on row 4, data from row 5)
## --------------------------------------------------------------------
read_form <- function(sheet, require_col = NULL) {
  df <- read.xlsx(DATA_PATH, sheet = sheet, startRow = 4,
                  colNames = TRUE, detectDates = TRUE)
  df <- clean_names(df)
  if (!is.null(require_col) && require_col %in% names(df))
    df <- df[!is.na(df[[require_col]]), , drop = FALSE]
  df
}

SP  <- read_form("Codebook_Species")
SP  <- SP[!is.na(SP$Code) & SP$Code != "", , drop = FALSE]
MK  <- read_form("Codebook_Markets")
MK  <- MK[!is.na(MK$Code) & MK$Code != "", , drop = FALSE]
A   <- read_form("Form_A_Aratdar",          "Interview_Date")
B   <- read_form("Form_B_Bepari_Faria",     "Interview_Date")
R   <- read_form("Form_R_Khuchra",          "Interview_Date")
C   <- read_form("Form_C_Consumer",         "Interview_Date")
PO  <- read_form("Price_Observations",      "Respondent_ID")
CPF <- read_form("Consumer_Purchases_Focal", "Respondent_ID")
MFO <- read_form("Form_M_Market_Observation", "Obs_Date")

PO$buy_kg  <- ppk(PO$Buy_price_raw,  PO$Unit, PO$Buy_BDT_per_kg)
PO$sell_kg <- ppk(PO$Sell_price_raw, PO$Unit, PO$Sell_BDT_per_kg)
PO$qty_kg  <- qkg(PO$Quantity_raw, PO$Quantity_unit, PO$Quantity_kg)
CPF$price_kg <- ppk(CPF$Price_raw, CPF$Unit, CPF$Price_BDT_per_kg)

buy_status  <- cell_status(PO$Buy_price_raw)
sell_status <- cell_status(PO$Sell_price_raw)
CPF_yes     <- CPF[!is.na(CPF$Purchased_today) & CPF$Purchased_today == "Yes", , drop = FALSE]

## --------------------------------------------------------------------
## 2. TABLES (mirroring the Python builders)
## --------------------------------------------------------------------
mean_of <- function(v) if (length(v[!is.na(v)])) round(mean(v, na.rm = TRUE), 2) else NA_real_

## T1 - respondent profile
t1_row <- function(label, rs) {
  data.frame(
    Actor = label, n = nrow(rs),
    Age_mean_years      = mean_of(num(rs$Age_years)),
    Age_sd_years        = if (nrow(rs) > 1) round(sd(num(rs$Age_years), na.rm = TRUE), 2) else 0,
    Years_mean          = mean_of(num(rs$Years_in_business)),
    Family_size_mean    = mean_of(num(rs$Family_members)))
}
Bep   <- B[B$Actor_subtype == "Bepari", , drop = FALSE]
Faria <- B[B$Actor_subtype == "Faria", , drop = FALSE]
T1 <- rbind(t1_row("Aratdar", A), t1_row("Bepari", Bep), t1_row("Faria", Faria),
            t1_row("Retailer", R))

## T2 - business scale (mean daily capacity, kg/day)
T2 <- data.frame(
  Actor = c("Aratdar", "Bepari/Faria", "Retailer"),
  n = c(nrow(A), nrow(B), nrow(R)),
  Daily_capacity_kg_mean = c(mean_of(num(A$Daily_capacity_kg)),
                             mean_of(num(B$Daily_capacity_kg)),
                             mean_of(num(R$Daily_capacity_kg))),
  Daily_capacity_kg_median = c(median(num(A$Daily_capacity_kg), na.rm = TRUE),
                               median(num(B$Daily_capacity_kg), na.rm = TRUE),
                               median(num(R$Daily_capacity_kg), na.rm = TRUE)))

## T5 - payment mix
pmean <- function(rs, col) mean_of(num(rs[[col]]))
T5 <- data.frame(
  Actor = c("Aratdar", "Bepari/Faria", "Retailer"),
  Cash_pct_mean   = c(pmean(A, "Payment_cash_pct"),  pmean(B, "Payment_cash_pct"),  pmean(R, "Payment_cash_pct")),
  MFS_pct_mean    = c(pmean(A, "Payment_MFS_pct"),   pmean(B, "Payment_MFS_pct"),   pmean(R, "Payment_MFS_pct")),
  Credit_pct_mean = c(pmean(A, "Payment_credit_pct"),pmean(B, "Payment_credit_pct"),pmean(R, "Payment_credit_pct")))
C_pm <- table(C$Payment_method)
T5c <- data.frame(Method = names(C_pm), n = as.integer(C_pm),
                  pct = round(100 * as.integer(C_pm) / nrow(C), 1))

## T3 - price chain per species (Methodology V4 conventions:
## producer/aratdar quotes only at landing markets M1/M6)
stage_mean <- function(code, actor, field, landing_only = FALSE) {
  keep <- PO$Species_code == code & PO$Actor_type == actor &
          !is.na(PO[[field]])
  if (landing_only) keep <- keep & PO$Market %in% LANDING
  v <- PO[[field]][keep]
  mean_of(v)
}
cons_mean <- function(code) mean_of(CPF_yes$price_kg[CPF_yes$Species_code == code])
cons_n <- function(code) sum(!is.na(CPF_yes$price_kg[CPF_yes$Species_code == code]))
chain <- function(code) {
  prod <- stage_mean(code, "Aratdar", "buy_kg",  TRUE)
  arat <- stage_mean(code, "Aratdar", "sell_kg", TRUE)
  bep  <- stage_mean(code, "Bepari_Faria", "sell_kg")
  ret  <- stage_mean(code, "Khuchra", "sell_kg")
  cons <- cons_mean(code)
  nc   <- cons_n(code)
  comp <- !any(is.na(c(prod, arat, bep, cons))) && nc >= MIN_CONS
  list(code = code, producer = prod, aratdar = arat, bepari = bep,
       retail = ret, consumer = cons, consumer_n = nc, complete = comp)
}
species_codes <- sort(SP$Code)
chains <- lapply(species_codes, chain)
names(chains) <- species_codes
complete_codes <- species_codes[sapply(chains, function(x) x$complete)]
pool <- function(field)
  round(mean(sapply(chains[complete_codes], function(x) x[[field]])), 2)
P <- list(producer = pool("producer"), aratdar = pool("aratdar"),
          bepari = pool("bepari"), retail = pool("retail"),
          consumer = pool("consumer"))

T3 <- do.call(rbind, lapply(species_codes, function(code) {
  x <- chains[[code]]
  data.frame(Species_code = code,
             Producer = x$producer, Aratdar_sell = x$aratdar,
             Bepari_sell = x$bepari, Retailer_quote = x$retail,
             Consumer_paid = x$consumer)
}))
T3ALL <- data.frame(Species_code = "ALL (chain-complete)",
                    Producer = P$producer, Aratdar_sell = P$aratdar,
                    Bepari_sell = P$bepari, Retailer_quote = P$retail,
                    Consumer_paid = P$consumer)

## T10 - margin summary over chain-complete species
T10 <- data.frame(
  Level = c("Aratdar (auction margin, M1/M6)",
            "Bepari/Faria (wholesale margin)",
            "Retailer (margin to consumer)",
            "Total marketing spread",
            "Producer share of consumer price"),
  Margin_BDT_kg = c(round(P$aratdar - P$producer, 2),
                    round(P$bepari - P$aratdar, 2),
                    round(P$consumer - P$bepari, 2),
                    round(P$consumer - P$producer, 2),
                    NA),
  Margin_pct = c(round(100 * (P$aratdar - P$producer) / P$consumer, 1),
                 round(100 * (P$bepari - P$aratdar) / P$consumer, 1),
                 round(100 * (P$consumer - P$bepari) / P$consumer, 1),
                 round(100 * (P$consumer - P$producer) / P$consumer, 1),
                 round(100 * P$producer / P$consumer, 1)))

## T11 - retail quotes by species x market
markets <- c("M1", "M2", "M3", "M4", "M5", "M6")
T11 <- t(sapply(species_codes, function(code) {
  sapply(markets, function(m) {
    v <- PO$sell_kg[PO$Species_code == code & PO$Actor_type == "Khuchra" &
                    PO$Market == m & !is.na(PO$sell_kg)]
    if (length(v)) mean_of(v) else NA_real_
  })
}))
rownames(T11) <- species_codes
colnames(T11) <- markets

## --------------------------------------------------------------------
## 3. STATISTICAL TESTS (mirroring extend_analysis.py)
## --------------------------------------------------------------------
ACTOR_ORDER <- c("Aratdar" = 0, "Bepari_Faria" = 1, "Khuchra" = 2)

## Matched pairs (Methodology 3.3.4): within each Pair_ID pick the
## seller-buyer combination that respects channel order and minimises
## the quote gap - same algorithm as Python build_pairs().
pair_rows <- list()
po_p <- PO[!is.na(PO$Pair_ID) & PO$Pair_ID != "", , drop = FALSE]
for (pid in unique(po_p$Pair_ID)) {
  rows <- po_p[po_p$Pair_ID == pid, , drop = FALSE]
  if (nrow(rows) < 2) next
  best <- NULL
  for (i in seq_len(nrow(rows))) for (j in seq_len(nrow(rows))) {
    if (i == j) next
    s <- rows[i, ]; b <- rows[j, ]
    if (is.na(s$sell_kg) || is.na(b$buy_kg)) next
    so <- if (s$Actor_type %in% names(ACTOR_ORDER)) ACTOR_ORDER[[s$Actor_type]] else 9
    bo <- if (b$Actor_type %in% names(ACTOR_ORDER)) ACTOR_ORDER[[b$Actor_type]] else 9
    if (so > bo) next
    dd <- abs(s$sell_kg - b$buy_kg)
    if (is.null(best) || dd < best$dd) best <- list(dd = dd, s = s, b = b)
  }
  if (is.null(best)) next
  pair_rows[[length(pair_rows) + 1]] <- data.frame(
    Pair_ID = pid, Market = best$s$Market,
    Species_code = best$s$Species_code,
    Seller_ID = best$s$Respondent_ID, Seller_actor = best$s$Actor_type,
    Seller_sell = best$s$sell_kg,
    Buyer_ID = best$b$Respondent_ID, Buyer_actor = best$b$Actor_type,
    Buyer_buy = best$b$buy_kg,
    Diff = round(best$s$sell_kg - best$b$buy_kg, 2))
}
T12 <- do.call(rbind, pair_rows)
if (is.null(T12)) T12 <- data.frame()
T12b <- data.frame()
if (nrow(T12)) {
  diffs <- T12$Diff[!is.na(T12$Diff)]
  d_nz  <- diffs[diffs != 0]
  has_ties <- any(duplicated(d_nz))
  wt <- suppressWarnings(wilcox.test(d_nz, exact = !has_ties,
                                     correct = FALSE))
  V <- unname(wt$statistic)                       # sum of positive ranks
  W <- min(V, sum(rank(abs(d_nz))) - V)           # scipy convention
  T12b <- data.frame(
    Item = c("Usable matched pairs (n)", "Pairs with non-zero difference",
             "Median difference (BDT/kg)", "Mean difference (BDT/kg)",
             "Wilcoxon W statistic (scipy convention)", "R V statistic",
             "p-value (two-sided)"),
    Value = c(length(diffs), length(d_nz),
              round(median(diffs), 2), round(mean(diffs), 2),
              W, V, round(wt$p.value, 4)))
}

## T14 - Kruskal-Wallis: retail quotes across markets per species
kw_row <- function(code) {
  vbm <- lapply(markets, function(m) {
    PO$sell_kg[PO$Species_code == code & PO$Actor_type == "Khuchra" &
               PO$Market == m & !is.na(PO$sell_kg)]
  })
  names(vbm) <- markets
  qual5 <- vbm[sapply(vbm, length) >= 5]
  qual3 <- vbm[sapply(vbm, length) >= 3]
  if (length(qual5) >= 3) {
    kt <- kruskal.test(qual5); tier <- "pre-specified (n>=5)"
    qn <- qual5
  } else if (length(qual3) >= 3) {
    kt <- kruskal.test(qual3); tier <- "exploratory (n>=3)"
    qn <- qual3
  } else {
    return(data.frame(Species = code, Tier = "not run", H = NA,
                      df = NA, p = NA, Markets = ""))
  }
  data.frame(Species = code, Tier = tier,
             H = round(unname(kt$statistic), 3),
             df = unname(kt$parameter), p = round(kt$p.value, 4),
             Markets = paste(names(qn), collapse = "; "))
}
T14 <- do.call(rbind, lapply(species_codes, kw_row))

## T15 - payment-mode adoption x actor (MFS frequency chi-square)
freq_col <- "MFS_transaction_frequency"
cats <- c("Regular", "Occasional", "Never")
mk_row <- function(rs) sapply(cats, function(cc)
  sum(!is.na(rs[[freq_col]]) & rs[[freq_col]] == cc))
arr <- rbind(Aratdar = mk_row(A), `Bepari/Faria` = mk_row(B),
             Retailer = mk_row(R))
ct <- suppressWarnings(chisq.test(arr, correct = FALSE))
T15 <- data.frame(Actor = rownames(arr), n = rowSums(arr),
                  Regular = arr[, 1], Occasional = arr[, 2],
                  Never = arr[, 3])
T15b <- data.frame(chi2 = round(unname(ct$statistic), 2),
                   df = unname(ct$parameter),
                   p = round(ct$p.value, 4),
                   min_expected = round(min(ct$expected), 2))

## Per-respondent own-quote margins (sell - buy mean per respondent)
resp_margins <- function() {
  both <- PO[!is.na(PO$buy_kg) & !is.na(PO$sell_kg), , drop = FALSE]
  agg <- aggregate(both$sell_kg - both$buy_kg,
                   by = list(ID = both$Respondent_ID,
                             Actor = both$Actor_type), FUN = mean)
  names(agg)[3] <- "margin"
  agg
}
RM <- resp_margins()

## T16 - stratum margins + Mann-Whitney U
strata <- list(Aratdar = RM$margin[RM$Actor == "Aratdar"],
               Bepari_Faria = RM$margin[RM$Actor == "Bepari_Faria"],
               Khuchra = RM$margin[RM$Actor == "Khuchra"])
T16 <- data.frame(Actor = names(strata), n = sapply(strata, length),
                  Median = sapply(strata, function(v) round(median(v), 2)),
                  Mean = sapply(strata, function(v) round(mean(v), 2)))
pairs16 <- rbind(c("Aratdar", "Bepari_Faria"),
                 c("Aratdar", "Khuchra"),
                 c("Bepari_Faria", "Khuchra"))
T16 <- rbind(T16, do.call(rbind, lapply(seq_len(nrow(pairs16)), function(k) {
  a <- strata[[pairs16[k, 1]]]; b <- strata[[pairs16[k, 2]]]
  ut <- suppressWarnings(wilcox.test(a, b, exact = FALSE, correct = FALSE))
  data.frame(Actor = paste0("MWU: ", pairs16[k, 1], " vs ", pairs16[k, 2]),
             n = paste0(length(a), "/", length(b)),
             Median = NA_real_, Mean = NA_real_,
             U = unname(ut$statistic), p = ut$p.value)
})))

## T17 - retailer marketing cost vs net margin (Spearman)
T17 <- do.call(rbind, lapply(RM$ID[RM$Actor == "Khuchra"], function(id) {
  ri <- which(R$Respondent_ID == id)
  if (!length(ri)) return(NULL)
  cap <- num(R$Daily_capacity_kg[ri])
  if (!length(cap) || is.na(cap) || cap <= 0) return(NULL)
  mc <- (ifelse(is.na(num(R$Shop_Van_Rent_BDT_per_day[ri])), 0, num(R$Shop_Van_Rent_BDT_per_day[ri])) +
         ifelse(is.na(num(R$Ice_cost_BDT_per_day[ri])), 0, num(R$Ice_cost_BDT_per_day[ri])) +
         ifelse(is.na(num(R$Wash_Water_Other_cost_BDT_per_day[ri])), 0, num(R$Wash_Water_Other_cost_BDT_per_day[ri]))) / cap
  mg <- RM$margin[RM$ID == id & RM$Actor == "Khuchra"]
  data.frame(Respondent_ID = id, Market = R$Market[ri],
             Margin = round(mg, 2), MC_kg = round(mc, 2),
             Net = round(mg - mc, 2))
}))
if (is.null(T17)) T17 <- data.frame()
T17b <- data.frame()
if (nrow(T17) >= 8) {
  st <- suppressWarnings(cor.test(T17$MC_kg, T17$Net, method = "spearman",
                                  exact = FALSE))
  T17b <- data.frame(rho = round(unname(st$estimate), 3),
                     p = round(st$p.value, 4), n = nrow(T17))
}

## --------------------------------------------------------------------
## 4. WRITE TABLES
## --------------------------------------------------------------------
wcsv <- function(df, name) write.csv(df, file.path(OUT_T, name),
                                     row.names = FALSE, na = "",
                                     fileEncoding = "UTF-8")
wcsv(T1,   "T1_Respondent_Profile_R.csv")
wcsv(T2,   "T2_Business_Scale_R.csv")
wcsv(T5,   "T5_Payment_Methods_R.csv")
wcsv(T5c,  "T5c_Consumer_Payment_R.csv")
wcsv(rbind(T3, T3ALL), "T3_Price_Chain_R.csv")
wcsv(T10,  "T10_Margin_Summary_R.csv")
write.csv(T11, file.path(OUT_T, "T11_Retail_Price_by_Market_R.csv"),
          na = "", fileEncoding = "UTF-8")
if (nrow(T12))  wcsv(T12,  "T12_Pair_Detail_R.csv")
if (nrow(T12b)) wcsv(T12b, "T12b_Wilcoxon_Result_R.csv")
wcsv(T14,  "T14_KruskalWallis_R.csv")
wcsv(T15,  "T15_Payment_Actor_R.csv")
wcsv(T15b, "T15b_ChiSquare_R.csv")
wcsv(T16,  "T16_Stratum_Margins_R.csv")
if (nrow(T17))  wcsv(T17,  "T17_Retailer_MC_Profit_R.csv")
if (nrow(T17b)) wcsv(T17b, "T17b_Spearman_R.csv")

## --------------------------------------------------------------------
## 5. VERIFICATION REPORT (reference values = Python pipeline output
##    on the simulated dataset; re-check after real data entry)
## --------------------------------------------------------------------
cat("\n=====================================================================\n")
cat("VERIFICATION REPORT - R vs Python reference (simulated dataset)\n")
cat("=====================================================================\n")
CHKN <- 0
CHK_RESULTS <- logical(0)
chk <- function(label, computed, expected, tol = 0.06) {
  CHKN <<- CHKN + 1
  if (is.character(computed) || is.character(expected)) {
    ok <- identical(as.character(computed), as.character(expected))
  } else {
    ok <- !is.na(computed) && !is.na(expected) &&
          abs(computed - expected) <= tol
  }
  CHK_RESULTS <<- c(CHK_RESULTS, ok)
  cat(sprintf("[%s %02d] %-52s R = %-11s Python = %-11s %s\n",
              ifelse(ok, " OK", "!!"), CHKN, label,
              paste0(computed, collapse = ","),
              paste0(expected, collapse = ","),
              ifelse(ok, "MATCH", "MISMATCH")))
  invisible(ok)
}

chk("Form A (Aratdar) respondents",           nrow(A), 30)
chk("Form B (Bepari/Faria) respondents",      nrow(B), 30)
chk("Form R (Retailer) respondents",          nrow(R), 30)
chk("Form C (Consumer) respondents",          nrow(C), 30)
chk("Total interviews",                       nrow(A) + nrow(B) + nrow(R) + nrow(C), 120)
chk("Price_Observations rows",                nrow(PO), 463)
chk("Buy price cells K (closed today)",       sum(buy_status == "K"), 48)
chk("Sell price cells K (closed today)",      sum(sell_status == "K"), 45)
chk("Sell price cells D (refused)",           sum(sell_status == "D"), 19)
chk("Consumer focal purchase rows",           nrow(CPF), 69)
chk("Focal purchases bought today (Yes)",     nrow(CPF_yes), 52)
chk("T1 Aratdar mean age (years)",            T1$Age_mean_years[1], 44.13)
chk("T1 Bepari mean age (years)",             T1$Age_mean_years[2], 40.1)
chk("T1 Faria mean age (years)",              T1$Age_mean_years[3], 40.4)
chk("T1 Retailer mean age (years)",           T1$Age_mean_years[4], 38.77)
chk("T1 Aratdar mean experience (years)",     T1$Years_mean[1], 18.73)
chk("T1 Retailer mean experience (years)",    T1$Years_mean[4], 12.77)
chk("T2 Aratdar mean daily capacity (kg)",    T2$Daily_capacity_kg_mean[1], 797.4)
chk("T2 Bepari/Faria mean daily capacity (kg)", T2$Daily_capacity_kg_mean[2], 204.51)
chk("T2 Retailer mean daily capacity (kg)",   T2$Daily_capacity_kg_mean[3], 99.95)
chk("T5 Aratdar mean cash share (%)",         T5$Cash_pct_mean[1], 67.6)
chk("T5 Bepari mean cash share (%)",          T5$Cash_pct_mean[2], 63.87)
chk("T5 Retailer mean cash share (%)",        T5$Cash_pct_mean[3], 55.23)
chk("T5 consumer bKash share (%)",
    T5c$pct[T5c$Method == "bKash"], 36.7)
chk("Chain-complete species count (MIN_CONS)", length(complete_codes), 8)
chk("T3 ALL producer price (BDT/kg)",         P$producer, 601.41)
chk("T3 ALL aratdar sell (BDT/kg)",           P$aratdar, 629.25)
chk("T3 ALL bepari sell (BDT/kg)",            P$bepari, 728.83)
chk("T3 ALL retailer quote (BDT/kg)",         P$retail, 869.5)
chk("T3 ALL consumer paid (BDT/kg)",          P$consumer, 847.8)
chk("T10 aratdar margin (BDT/kg)",            P$aratdar - P$producer, 27.84)
chk("T10 bepari margin (BDT/kg)",             P$bepari - P$aratdar, 99.58)
chk("T10 retailer margin (BDT/kg)",           P$consumer - P$bepari, 118.97)
chk("T10 total marketing spread (BDT/kg)",    P$consumer - P$producer, 246.39)
chk("T10 producer share (%)",                 100 * P$producer / P$consumer, 70.9)
chk("T3 S01 Ilish consumer price (BDT/kg)",   chains$S01$consumer, 1420)
chk("T3 S02 Rupchanda consumer price",        chains$S02$consumer, 1615)
chk("T3 S03 Lakkha consumer price",           chains$S03$consumer, 1033.33)
chk("T3 S04 Koral consumer price",            chains$S04$consumer, 885)
chk("T3 S05 Surma consumer price",            chains$S05$consumer, 585)
chk("T3 S06 Churi consumer price",            chains$S06$consumer, 446.54)
chk("T3 S07 Poa consumer price",              chains$S07$consumer, 530)
chk("T3 S08 Kankoita consumer price (n=1, descriptive)", chains$S08$consumer, 330)
chk("T3 S09 Loitta consumer price",           chains$S09$consumer, 267.5)
chk("T3 S10 Harina consumer price (n=1, descriptive)", chains$S10$consumer, 215)
chk("T3 S01 Ilish retailer quote (BDT/kg)",   chains$S01$retail, 1486.96)
chk("T11 S01 Ilish retail at Fishery Ghat",   T11["S01", "M1"], 1416.0)
if (nrow(T12b)) {
  chk("T12b usable matched pairs",            T12b$Value[1], 14)
  chk("T12b pairs with non-zero difference",  T12b$Value[2], 13)
  chk("T12b Wilcoxon W (scipy convention)",   T12b$Value[5], 23.0, tol = 0.51)
  chk("T12b Wilcoxon p-value",                T12b$Value[7], 0.1157, tol = 0.002)
}
chk("T15 chi-square statistic",               T15b$chi2, 1.22)
chk("T15 chi-square df",                      T15b$df, 4)
chk("T15 chi-square p-value",                 T15b$p, 0.8749, tol = 0.002)
chk("T16 Aratdar median margin (BDT/kg)",
    T16$Median[T16$Actor == "Aratdar"], 30.14)
chk("T16 Bepari/Faria median margin",
    T16$Median[T16$Actor == "Bepari_Faria"], 83.74)
chk("T16 Retailer median margin",
    T16$Median[T16$Actor == "Khuchra"], 182.0)
if (nrow(T17b)) {
  chk("T17 Spearman rho (MC vs net margin)",  T17b$rho, 0.43, tol = 0.006)
  chk("T17 Spearman p-value",                 T17b$p, 0.0177, tol = 0.002)
  chk("T17 retailer n",                       T17b$n, 30)
}
cat("---------------------------------------------------------------------\n")
cat(sprintf("SUMMARY: %d checks, %d MATCH, %d MISMATCH\n",
            CHKN, sum(CHK_RESULTS, na.rm = TRUE),
            sum(!CHK_RESULTS, na.rm = TRUE)))
cat("(any MISMATCH means R and Python disagree - send the full console\n")
cat(" output back for diagnosis; matching tables are in r_outputs/.)\n")
cat("Tables written to :", OUT_T, "\n")

## --------------------------------------------------------------------
## 6. FIGURES (ggplot2; Times New Roman on Windows, 1000 dpi,
##    title centred at top, legend centred at the bottom, value labels)
## --------------------------------------------------------------------
if (MAKE_FIGURES) {
  library(ggplot2)
  tnr <- "serif"
  if (.Platform$OS.type == "windows") {
    windowsFonts(Times = windowsFont("Times New Roman"))
    tnr <- "Times"
  }
  base <- theme_bw(base_size = 12) +
    theme(
      text          = element_text(family = tnr),
      plot.title    = element_text(hjust = 0.5, face = "bold", size = 15,
                                   margin = margin(t = 6, b = 10)),
      plot.subtitle = element_text(hjust = 0.5, size = 11),
      legend.position = "bottom",
      legend.title  = element_blank(),
      axis.title    = element_text(size = 12.5),
      panel.grid.major = element_line(colour = "grey83", linewidth = 0.5),
      panel.grid.minor = element_line(colour = "grey92", linewidth = 0.35,
                                      linetype = "dotted"))
  gsave <- function(p, name, w = 9, h = 6.4)
    ggsave(file.path(OUT_C, name), p, width = w, height = h, dpi = 1000)

  ## R-F1 - marketing margin by intermediary (bar chart)
  df1 <- data.frame(
    Level = c("Aratdar\n(auction)", "Bepari/Faria\n(wholesale)",
              "Retailer\n(retail)", "Total marketing\nspread"),
    Margin = c(P$aratdar - P$producer, P$bepari - P$aratdar,
               P$consumer - P$bepari, P$consumer - P$producer))
  df1$Pct <- 100 * df1$Margin / P$consumer
  p1 <- ggplot(df1, aes(Level, Margin)) +
    geom_col(fill = c("#D9822B", "#2E8B57", "#C0504D", "#4C5468"),
             colour = "#33415C", width = 0.58) +
    geom_text(aes(label = sprintf("%.1f", Margin)),
              vjust = -0.55, fontface = "bold", size = 4.2) +
    geom_text(aes(label = sprintf("(%.1f%%)", Pct)),
              vjust = -2.1, size = 3.3, colour = "grey30") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.20))) +
    labs(title = "Average Marketing Margin by Chain Intermediary",
         subtitle = sprintf("(mean of %d chain-complete species, March 2026)",
                            length(complete_codes)),
         x = "Marketing chain intermediary",
         y = "Marketing margin (BDT per kilogram)") + base
  gsave(p1, "R_F1_margin_by_intermediary.png")

  ## R-F2 - retail price distribution by species (box plot)
  ret <- PO[PO$Actor_type == "Khuchra" & !is.na(PO$sell_kg), , drop = FALSE]
  n_sp  <- table(ret$Species_code)
  keep  <- names(n_sp)[n_sp >= 5]
  ret   <- ret[ret$Species_code %in% keep, , drop = FALSE]
  med_o <- sort(tapply(ret$sell_kg, ret$Species_code, median), decreasing = TRUE)
  lab2  <- sapply(names(med_o), function(cd) {
    nm <- SP$Local_name[SP$Code == cd]
    paste0(nm, "\n(n = ", n_sp[cd], ")")
  })
  ret$Species <- factor(ret$Species_code, levels = names(med_o),
                        labels = lab2)
  med_df <- data.frame(Species = factor(names(med_o),
                                        levels = names(med_o), labels = lab2),
                       y = as.numeric(med_o))
  p2 <- ggplot(ret, aes(Species, sell_kg)) +
    geom_boxplot(fill = "#DCE4EE", colour = "#33415C",
                 outlier.colour = "#9AA7B8", outlier.size = 0.9) +
    geom_text(data = med_df,
              aes(x = Species, y = y,
                  label = format(y, big.mark = ",")),
              inherit.aes = FALSE, vjust = -0.55, size = 3.1,
              colour = "#B4472A", fontface = "bold") +
    scale_y_continuous(expand = expansion(mult = c(0, 0.10))) +
    labs(title = "Distribution of Retail Selling Prices by Species",
         subtitle = "(boxes: median and interquartile range; dots: outliers)",
         x = "Species (local name; n = number of retail sell quotes)",
         y = "Retail selling price (BDT per kilogram)") + base
  gsave(p2, "R_F2_retail_price_boxplot.png", w = 10, h = 6.8)

  ## R-F4 - decomposition of the consumer price (donut chart)
  df4 <- data.frame(
    Segment = c("Producer (fisher) share", "Bepari/Faria margin",
                "Retailer margin", "Aratdar margin"),
    Share = c(100 * P$producer / P$consumer,
              100 * (P$bepari - P$aratdar) / P$consumer,
              100 * (P$consumer - P$bepari) / P$consumer,
              100 * (P$aratdar - P$producer) / P$consumer))
  p4 <- ggplot(df4, aes(x = 2, y = Share, fill = Segment)) +
    geom_col(width = 1, colour = "white", linewidth = 1.2) +
    coord_polar(theta = "y", start = pi / 2, direction = -1) +
    xlim(c(0, 2.5)) +
    geom_text(aes(label = ifelse(Share >= 5,
                                 sprintf("%.1f%%", Share), "")),
              position = position_stack(vjust = 0.5),
              colour = "white", fontface = "bold", size = 4.4) +
    annotate("text", x = 0.15, y = 50,
             label = paste0("Consumer price\n", sprintf("%.1f", P$consumer),
                            "\nBDT per kilogram"),
             fontface = "bold", size = 4.6, family = tnr) +
    scale_fill_manual(values = c("#1F4E79", "#2E8B57", "#C0504D", "#D9822B")) +
    labs(title = "Decomposition of the Average Consumer Price",
         subtitle = sprintf("(mean of %d chain-complete species, March 2026)",
                            length(complete_codes)),
         x = NULL, y = NULL) +
    base + theme(axis.text = element_blank(), axis.ticks = element_blank(),
                 panel.grid = element_blank())
  gsave(p4, "R_F4_consumer_price_decomposition.png", w = 8.6, h = 8)

  ## R-F5 - payment method composition (stacked horizontal bars)
  mfs_c <- 100 * sum(T5c$n[T5c$Method %in% c("bKash", "Nagad_app")]) / nrow(C)
  cash_c <- 100 * sum(T5c$n[T5c$Method == "Cash"]) / nrow(C)
  cred_c <- 100 * sum(T5c$n[T5c$Method == "Credit"]) / nrow(C)
  df5 <- data.frame(
    Actor = factor(c("Aratdar", "Bepari/Faria", "Retailer", "Consumer"),
                   levels = c("Consumer", "Retailer", "Bepari/Faria", "Aratdar")),
    Cash = c(T5$Cash_pct_mean, cash_c),
    MFS  = c(T5$MFS_pct_mean, mfs_c),
    Credit = c(T5$Credit_pct_mean, cred_c))
  df5l <- rbind(
    data.frame(Actor = df5$Actor, Method = "Cash", Share = df5$Cash),
    data.frame(Actor = df5$Actor,
               Method = "Mobile financial services (bKash/Nagad)",
               Share = df5$MFS),
    data.frame(Actor = df5$Actor, Method = "Credit", Share = df5$Credit))
  df5l$Method <- factor(df5l$Method,
                        levels = c("Cash",
                                   "Mobile financial services (bKash/Nagad)",
                                   "Credit"))
  p5 <- ggplot(df5l, aes(Actor, Share, fill = Method)) +
    geom_col(colour = "#33415C", linewidth = 0.5, width = 0.55) +
    geom_text(aes(label = ifelse(Share >= 6, sprintf("%.1f%%", Share), "")),
              position = position_stack(vjust = 0.5), colour = "white",
              fontface = "bold", size = 3.6) +
    scale_fill_manual(values = c("#8FA9C4", "#D9822B", "#B4472A")) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.05))) +
    coord_flip() +
    labs(title = "Payment Method Composition by Market Actor",
         subtitle = "(traders: mean share of receipts; consumers: last purchase)",
         x = "Market actor", y = "Share of transactions (%)") + base
  gsave(p5, "R_F5_payment_method_mix.png")

  ## R-F8 - average retail price by market (bar chart)
  mk_mean <- sapply(markets, function(m) {
    sub <- PO[PO$Actor_type == "Khuchra" & PO$Market == m &
              !is.na(PO$sell_kg), , drop = FALSE]
    sp <- tapply(sub$sell_kg, sub$Species_code, mean, na.rm = TRUE)
    round(mean(sp, na.rm = TRUE), 1)
  })
  mk_name <- sapply(markets, function(m) {
    nm <- MK$Market_name[MK$Code == m]
    cnt <- sum(!is.na(T11[, m]))
    paste0(nm, "\n(", cnt, " species)")
  })
  df8 <- data.frame(Market = factor(seq_along(markets), labels = mk_name),
                    Price = as.numeric(mk_mean))
  p8 <- ggplot(df8, aes(Market, Price)) +
    geom_col(fill = "#5B7DA3", colour = "#33415C", width = 0.6) +
    geom_text(aes(label = sprintf("%.1f", Price)), vjust = -0.55,
              fontface = "bold", size = 4.1) +
    scale_y_continuous(expand = expansion(mult = c(0, 0.18))) +
    labs(title = "Average Retail Selling Price by Market",
         subtitle = "(unweighted mean of species-level mean quotes, March 2026)",
         x = "Market (number of species with retail quotes)",
         y = "Average retail selling price (BDT per kilogram)") + base
  gsave(p8, "R_F8_retail_price_by_market.png")

  cat("Figures written to:", OUT_C, "\n")
}

cat("\nDone. Copy EVERYTHING above (the verification report) and send it\n")
cat("back so the R and Python outputs can be compared line by line.\n")


