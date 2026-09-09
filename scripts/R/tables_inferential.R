# ============================================================================
# tables_inferential.R — inferential tables T12..T18
# Implements every test pre-registered in Methodology V4 Sec. 3.8 / Table 3.6:
#   * Shapiro-Wilk normality screening           (T18)
#   * Wilcoxon signed-rank on Pair_ID            (T12b)
#   * Kruskal-Wallis + Dunn (Holm) by species    (T14, T14b)
#   * Mann-Whitney U across strata               (T16)
#   * chi-square (+ G-test, + exact Fisher)      (T15)
#   * Spearman cost-profit correlation           (T17)
# All two-sided at alpha = 0.05; cells n>=5 per market pre-specified,
# exploratory tier n>=3 flagged; never pool across species.
# ============================================================================
suppressPackageStartupMessages(library(stats))

## ============================================================================
## TABLE 12 / 12b — matched pairs and Wilcoxon signed-rank
## ============================================================================
build_pairs <- function() {
  po <- DATA$PO
  ord <- c(Aratdar = 0, Bepari_Faria = 1, Khuchra = 2)
  ids <- unique(po$Pair_ID[!is.na(po$Pair_ID) & po$Pair_ID != ""])
  out <- lapply(sort(ids), function(pid) {
    rows <- po[!is.na(po$Pair_ID) & po$Pair_ID == pid, , drop = FALSE]
    best <- NULL
    if (nrow(rows) >= 2) {
      for (a in seq_len(nrow(rows))) for (b in seq_len(nrow(rows))) {
        if (a == b) next
        sa <- rows[a, ]; bb <- rows[b, ]
        if (is.na(sa$sell_kg) || is.na(bb$buy_kg)) next
        oa <- ord[as.character(sa$Actor_type)]; ob <- ord[as.character(bb$Actor_type)]
        if (length(oa) == 0 || length(ob) == 0 || is.na(oa) || is.na(ob)) next
        if (oa > ob) next                                     # channel order
        d <- abs(sa$sell_kg - bb$buy_kg)
        if (is.null(best) || d < best$d) best <- list(d = d, sa = sa, bb = bb)
      }
    }
    if (is.null(best)) {
      data.frame(Pair_ID = pid, Market = rows$Market[1],
                 Species_code = rows$Species_code[1],
                 Seller_ID = NA, Seller_actor = NA, Seller_sell_BDT_kg = NA,
                 Buyer_ID = NA, Buyer_actor = NA, Buyer_buy_BDT_kg = NA,
                 Diff_BDT_kg = NA, Complete = FALSE)
    } else {
      data.frame(Pair_ID = pid, Market = best$sa$Market,
                 Species_code = best$sa$Species_code,
                 Seller_ID = best$sa$Respondent_ID,
                 Seller_actor = best$sa$Actor_type,
                 Seller_sell_BDT_kg = r2(best$sa$sell_kg),
                 Buyer_ID = best$bb$Respondent_ID,
                 Buyer_actor = best$bb$Actor_type,
                 Buyer_buy_BDT_kg = r2(best$bb$buy_kg),
                 Diff_BDT_kg = r2(best$sa$sell_kg - best$bb$buy_kg),
                 Complete = TRUE)
    }
  })
  do.call(rbind, out)
}
t12 <- function() {
  df <- build_pairs()
  list(name = "T12_Pair_Detail",
       title = "Table 12. Matched buyer-seller pairs (Pair_ID)",
       note = paste("Matched-pair transaction prices (Methodology 3.3.4). Seller_sell = the seller's",
                    "quoted sale price of the lot; Buyer_buy = the buyer's quoted purchase price of the",
                    "same lot. Diff = seller sell - buyer buy (~0 if self-reports are consistent).",
                    "Complete = both sides quoted numerically."),
       df = df)
}
t12b <- function() {
  df <- build_pairs()
  dd <- df$Diff_BDT_kg[df$Complete & !is.na(df$Diff_BDT_kg)]
  n <- length(dd)
  nz <- sum(dd != 0)
  item <- function(k, v) data.frame(Item = k, Value = v)
  if (n == 0) {
    rows <- item("Wilcoxon signed-rank (two-sided)", "No usable pairs")
  } else {
    w <- suppressWarnings(wilcox.test(dd, alternative = "two.sided", exact = FALSE))
    ## scipy.stats.wilcoxon reports W = the smaller of the signed-rank sums
    ## (ranks of |diff| over non-zero differences; zero_method='wilcox' drops
    ## zeros before ranking, exactly as R's wilcox.test does).
    d0 <- dd[dd != 0]
    rk <- rank(abs(d0))
    wpos <- sum(rk[d0 > 0])
    wstat <- min(wpos, sum(rk) - wpos)
    rows <- rbind(
      item("Usable matched pairs (n)", n),
      item("Pairs with non-zero difference", nz),
      item("Median difference (BDT/kg)", r2(median(dd))),
      item("Mean difference (BDT/kg)", r2(np_mean(dd))),
      item("Wilcoxon W statistic", wstat),
      item("p-value (two-sided)", rp(as.numeric(w$p.value), 4)),
      item("Interpretation",
           if (w$p.value >= 0.05)
             "p >= 0.05: seller-sell and buyer-buy quotes of matched lots do not differ systematically - self-reported chain prices are internally consistent"
           else "p < 0.05: matched buy/sell reports differ systematically - flag for review"))
  }
  list(name = "T12b_Wilcoxon_Result",
       title = "Table 12b. Wilcoxon signed-rank test on matched pairs",
       note = paste("Wilcoxon signed-rank on paired differences (seller's sell - buyer's buy) of the",
                    "same matched lot (Methodology 3.3.4). Diagnostic consistency check, not a powered",
                    "hypothesis test; report n alongside the result. R uses the normal approximation",
                    "with tie handling when exact calculation is unavailable."),
       df = rows)
}

## ============================================================================
## TABLE 13 — species x market price spread (descriptive)
## ============================================================================
t13 <- function() {
  po <- DATA$PO
  cpf_yes <- DATA$CPF[!is.na(DATA$CPF$Purchased_today) & DATA$CPF$Purchased_today == "Yes", , drop = FALSE]
  codes <- sort(unique(DATA$SP$Code))
  rows <- lapply(codes, function(code) {
    lapply(MKT_ORDER, function(m) {
      ws <- po$sell_kg[po$Actor_type == "Bepari_Faria" & po$Market == m &
                         po$Species_code == code & !is.na(po$sell_kg)]
      rs <- po$sell_kg[po$Actor_type == "Khuchra" & po$Market == m &
                         po$Species_code == code & !is.na(po$sell_kg)]
      cs <- cpf_yes$price_kg[!is.na(cpf_yes$price_kg) & cpf_yes$Market == m &
                               cpf_yes$Species_code == code]
      wm <- if (length(ws)) r2(np_mean(ws)) else NA_real_
      rm <- if (length(rs)) r2(np_mean(rs)) else NA_real_
      cm <- if (length(cs)) r2(np_mean(cs)) else NA_real_
      data.frame(Species = code, Market = m,
                 Wholesale_sell_mean = wm, n_wholesale = length(ws),
                 Retailer_sell_quote_mean = rm, n_retailer = length(rs),
                 Consumer_paid_mean = cm, n_consumer = length(cs),
                 Retail_margin_quote_BDT_kg = if (!anyNA(c(wm, rm))) r2(rm - wm) else NA_real_,
                 Retail_margin_paid_BDT_kg = if (!anyNA(c(wm, cm))) r2(cm - wm) else NA_real_)
    })
  })
  df <- do.call(rbind, do.call(c, rows))
  list(name = "T13_Species_Market_Spread",
       title = "Table 13. Species x market price spread (BDT/kg)",
       note = paste("Species x market price decomposition. Wholesale = Bepari/Faria sell quotes;",
                    "Retailer quote = khuchra sell quotes; Consumer = Form C slips. The difference between",
                    "quote- and paid-based margins reflects bargaining at retail. Cells with n=0 are not",
                    "observed. Per Methodology 3.8 cells with n<5 support descriptive statements only."),
       df = df)
}

## ============================================================================
## TABLE 14 / 14b — Kruskal-Wallis by species across markets (+ Dunn-Holm)
## ============================================================================
kw_one <- function(code, min_cell) {
  po <- DATA$PO
  cells <- lapply(MKT_ORDER, function(m)
    po$sell_kg[po$Actor_type == "Khuchra" & po$Market == m &
                 po$Species_code == code & !is.na(po$sell_kg)])
  names(cells) <- MKT_ORDER
  qual <- names(cells)[lengths(cells) >= min_cell]
  if (length(qual) < 3) return(NULL)
  test <- kruskal.test(cells[qual])
  info <- data.frame(
    Test_tier = if (min_cell == 5) "pre-specified (n>=5)" else "exploratory (n>=3)",
    Markets_qualifying = paste(qual, collapse = "; "),
    n_per_market = paste(sprintf("%s=%d", qual, lengths(cells[qual])), collapse = "; "),
    H = rp(as.numeric(test$statistic), 3), df = as.numeric(test$parameter),
    p_value = as.numeric(test$p.value))
  list(info = info, cells = cells[qual])
}
t14 <- function() {
  codes <- sort(unique(DATA$SP$Code))
  rows <- lapply(codes, function(code) {
    sp <- DATA$SP[DATA$SP$Code == code, , drop = FALSE]
    r5 <- kw_one(code, 5); r3 <- kw_one(code, 3)
    res <- if (!is.null(r5)) r5 else r3
    if (is.null(res)) {
      data.frame(Species = code, Local_name = sp$Local_name, Test_tier = "not run",
                 Markets_qualifying = "", n_per_market = "", H = NA, df = NA,
                 p_value = NA, Decision = "cells < n threshold in <3 markets -> descriptive only")
    } else {
      decision <- if (res$info$p_value < ALPHA)
        "reject H0 (p<0.05): prices differ across markets"
      else "fail to reject H0 (p>=0.05)"
      data.frame(Species = code, Local_name = sp$Local_name,
                 Test_tier = res$info$Test_tier,
                 Markets_qualifying = res$info$Markets_qualifying,
                 n_per_market = res$info$n_per_market, H = res$info$H,
                 df = res$info$df,
                 p_value = rp(res$info$p_value, 4), Decision = decision)
    }
  })
  df <- do.call(rbind, rows)
  list(name = "T14_Species_Market_KruskalWallis",
       title = "Table 14. Kruskal-Wallis: species price across markets",
       note = paste("Kruskal-Wallis H (Methodology 3.8): do retailer selling prices of the same species",
                    "differ across markets? Cells with n>=5 in >=3 markets use the pre-specified test;",
                    "otherwise an exploratory tier (n>=3) is flagged and species with thinner coverage are",
                    "reported descriptively only (no pooled-across-species tests)."),
       df = df)
}
t14b <- function() {
  codes <- sort(unique(DATA$SP$Code))
  res <- lapply(codes, function(code) {
    r5 <- kw_one(code, 5); r3 <- kw_one(code, 3)
    rr <- if (!is.null(r5)) r5 else r3
    if (is.null(rr) || rr$info$p_value >= ALPHA) return(NULL)
    d <- dunn_holm(rr$cells, strsplit(rr$info$Markets_qualifying, "; ")[[1]])
    d$Species <- code
    d
  })
  df <- do.call(rbind, res[!vapply(res, is.null, logical(1))])
  if (is.null(df)) {
    df <- data.frame(Market_i = character(), Market_j = character(), z = numeric(),
                     raw_p = numeric(), p_holm = numeric(),
                     significant_0.05 = logical(), Species = character())
  }
  list(name = "T14b_Dunn_Holm_Posthoc",
       title = "Table 14b. Dunn-Holm pairwise market comparisons",
       note = "Dunn's post-hoc with Holm step-down (p_holm) following significant Kruskal-Wallis.",
       df = df)
}

## ============================================================================
## TABLE 15 — payment mode x actor (chi-square + sparse fallbacks)
## ============================================================================
## Exact Freeman-Halton p for a 3x3 table — byte-for-byte the algorithm of
## extend_analysis.py `fisher_exact_3x3`: enumerate every table with the
## observed margins, weight by its exact conditional (hypergeometric)
## log-probability via lgamma, and return the tail mass P(chi2 >= observed).
fisher_exact_3x3 <- function(tab) {
  t <- matrix(as.integer(tab), nrow = 3, byrow = TRUE)
  r <- rowSums(t); c <- colSums(t); N <- sum(t)
  if (any(r < 0) || N == 0) return(NA_real_)
  expm <- outer(r, c) / N
  obs_chi2 <- sum((t - expm)^2 / expm)
  g <- expand.grid(A = 0:min(r[1], c[1]), B = 0:min(r[1], c[2]),
                   D = 0:min(r[2], c[1]), E = 0:min(r[2], c[2]))
  keep <- with(g, (A + B <= r[1]) & (D + E <= r[2]) &
                  (A + D <= c[1]) & (B + E <= c[2]))
  g <- g[keep, , drop = FALSE]
  A <- g$A; B <- g$B; D <- g$D; E <- g$E
  Cv <- r[1] - A - B; Fv <- r[2] - D - E
  Gv <- c[1] - A - D; Hv <- c[2] - B - E
  I1 <- r[3] - Gv - Hv; I2 <- c[3] - Cv - Fv
  ok <- (I1 == I2) & (I1 >= 0) & (Cv >= 0) & (Fv >= 0) & (Gv >= 0) & (Hv >= 0)
  cells <- cbind(A, B, Cv, D, E, Fv, Gv, Hv, I1)[ok, , drop = FALSE]
  Erow <- matrix(as.vector(t(expm)), nrow = nrow(cells), ncol = 9, byrow = TRUE)
  chi2v <- rowSums((cells - Erow)^2 / Erow)
  logP <- sum(lgamma(r + 1)) + sum(lgamma(c + 1)) - lgamma(N + 1) -
    rowSums(lgamma(cells + 1))
  P <- exp(logP - max(logP))
  sum(P[chi2v >= obs_chi2]) / sum(P)
}

t15 <- function() {
  cats <- c("Regular", "Occasional", "Never")
  freq <- function(rs) vapply(cats, function(k)
    sum(rs$MFS_transaction_frequency == k, na.rm = TRUE), integer(1))
  labs <- c("Aratdar", "Bepari/Faria", "Retailer")
  tab <- rbind(freq(DATA$A), freq(DATA$B), freq(DATA$R))
  dimnames(tab) <- list(labs, cats)
  chi <- chisq.test(tab, correct = FALSE)
  exp_min <- min(chi$expected)
  gtest_p <- NA_real_; exact_p <- NA_real_
  if (exp_min < 5) {
    G2 <- 2 * sum(tab * log(tab / chi$expected), na.rm = TRUE)
    gtest_p <- pchisq(G2, df = (nrow(tab) - 1) * (ncol(tab) - 1), lower.tail = FALSE)
    exact_p <- fisher_exact_3x3(tab)
  }
  cramer <- sqrt(as.numeric(chi$statistic) / (sum(tab) * (min(dim(tab)) - 1)))
  rows <- lapply(seq_len(nrow(tab)), function(i) {
    data.frame(Actor = labs[i], n = sum(tab[i, ]),
               MFS_Regular = tab[i, "Regular"], MFS_Occasional = tab[i, "Occasional"],
               MFS_Never = tab[i, "Never"],
               MFS_share_pct = rp(100 * tab[i, "Regular"] / sum(tab[i, ]), 1))
  })
  fallback_txt <- if (exp_min < 5)
    sprintf(", G-test p=%.4f, Fisher-exact p=%.4f", gtest_p, exact_p) else ""
  rows[[4]] <- data.frame(
    Actor = "chi-square (actor x MFS frequency)", n = sum(tab),
    MFS_Regular = NA, MFS_Occasional = NA, MFS_Never = NA,
    MFS_share_pct = sprintf("chi2=%.2f, df=%d, p=%.4f%s", chi$statistic,
                            chi$parameter, chi$p.value, fallback_txt))
  rows[[5]] <- data.frame(
    Actor = "Cramer's V / smallest expected count", n = NA,
    MFS_Regular = NA, MFS_Occasional = NA, MFS_Never = NA,
    MFS_share_pct = sprintf("V=%.3f / min exp=%.2f", cramer, exp_min))
  df <- do.call(rbind, rows)
  list(name = "T15_Payment_Actor_ChiSquare",
       title = "Table 15. Payment mode x actor chi-square",
       note = paste("Payment-mode adoption by trader class (Methodology 3.8 Q4). Chi-square on MFS-use",
                    "frequency (Regular/Occasional/Never); because the smallest expected cell may fall below 5,",
                    "the likelihood-ratio (G) test and the exact Freeman-Halton/Fisher test are reported",
                    "alongside Pearson chi-square as sparse-cell fallbacks. Consumer payment method is a",
                    "separate question and appears in Tables 5/8."),
       df = df)
}

## ============================================================================
## TABLE 16 — stratum margins and Mann-Whitney U
## ============================================================================
t16 <- function() {
  po <- DATA$PO
  rows_num <- po[!is.na(po$buy_kg) & !is.na(po$sell_kg), , drop = FALSE]
  m <- by(rows_num, rows_num$Respondent_ID, function(z) {
    data.frame(id = z$Respondent_ID[1], actor = z$Actor_type[1],
               m = np_mean(z$sell_kg - z$buy_kg))
  })
  m <- do.call(rbind, as.list(m))
  lv <- lapply(c("Aratdar","Bepari_Faria","Khuchra"), function(ac) m$m[m$actor == ac])
  names(lv) <- c("Aratdar","Bepari_Faria","Khuchra")
  row_for <- function(ac) {
    v <- lv[[ac]]
    data.frame(Actor = ac, n = length(v),
               Median_margin_BDT_kg = rp(median(v), 2),
               IQR_BDT_kg = rp(IQR(v), 2),
               Mean_margin_BDT_kg = rp(np_mean(v), 2))
  }
  rows <- lapply(c("Aratdar","Bepari_Faria","Khuchra"), row_for)
  pair_txt <- function(a, b) {
    u <- suppressWarnings(wilcox.test(lv[[a]], lv[[b]], exact = FALSE))
    paste0("U=", formatC(as.numeric(u$statistic), digits = 0, format = "f"),
           if (u$p.value < 1e-4) ", p<0.0001" else sprintf(", p=%.4f", u$p.value))
  }
  rows[[4]] <- data.frame(Actor = "Mann-Whitney U: Aratdar vs Bepari_Faria",
    n = sprintf("%d/%d", length(lv$Aratdar), length(lv$Bepari_Faria)),
    Median_margin_BDT_kg = NA, IQR_BDT_kg = NA, Mean_margin_BDT_kg = pair_txt("Aratdar","Bepari_Faria"))
  rows[[5]] <- data.frame(Actor = "Mann-Whitney U: Aratdar vs Khuchra",
    n = sprintf("%d/%d", length(lv$Aratdar), length(lv$Khuchra)),
    Median_margin_BDT_kg = NA, IQR_BDT_kg = NA, Mean_margin_BDT_kg = pair_txt("Aratdar","Khuchra"))
  rows[[6]] <- data.frame(Actor = "Mann-Whitney U: Bepari_Faria vs Khuchra",
    n = sprintf("%d/%d", length(lv$Bepari_Faria), length(lv$Khuchra)),
    Median_margin_BDT_kg = NA, IQR_BDT_kg = NA, Mean_margin_BDT_kg = pair_txt("Bepari_Faria","Khuchra"))
  df <- do.call(rbind, rows)
  list(name = "T16_Stratum_Margin_MannWhitney",
       title = "Table 16. Trader stratum margins and Mann-Whitney tests",
       note = paste("Per-respondent mean own-quote margin = mean of (sell - buy) over species quoted with",
                    "both prices on the interview day (Methodology 3.7.2: M = P_s - P_b). Mann-Whitney U per",
                    "stratum pair (Q2); Holm adjustment is recommended when quoting all three comparisons."),
       df = df)
}

## ============================================================================
## TABLE 17 — retailer marketing cost vs net margin (Spearman)
## ============================================================================
t17 <- function() {
  po <- DATA$PO
  rows_num <- po[!is.na(po$buy_kg) & !is.na(po$sell_kg), , drop = FALSE]
  m <- by(rows_num, rows_num$Respondent_ID, function(z) {
    data.frame(id = z$Respondent_ID[1], m = np_mean(z$sell_kg - z$buy_kg))
  })
  m <- do.call(rbind, as.list(m))
  cost_or_0 <- function(v) {
    x <- num(v)
    ifelse(is.na(x), 0, x)
  }
  out <- lapply(seq_len(nrow(DATA$R)), function(i) {
    r <- DATA$R[i, ]
    mm <- m$m[m$id == r$Respondent_ID]
    if (!length(mm)) return(NULL)
    ## capacity: cached kg column preferred, else raw value (python `num(kg) or
    ## num(raw)`; a literal 0 also falls back to the raw column, then skip)
    cap <- num(r$Daily_capacity_kg)
    if (is.na(cap) || cap == 0) cap <- num(r$Daily_capacity_raw)
    if (is.na(cap) || cap <= 0) return(NULL)
    mc <- (cost_or_0(r$Shop_Van_Rent_BDT_per_day) +
             cost_or_0(r$Ice_cost_BDT_per_day) +
             cost_or_0(r$Wash_Water_Other_cost_BDT_per_day)) / cap
    data.frame(Respondent_ID = r$Respondent_ID, Market = r$Market,
               Mean_margin_BDT_kg = r2(mm), MC_BDT_kg = r2(mc),
               Net_profit_BDT_kg = r2(mm - mc))
  })
  df <- do.call(rbind, out[!vapply(out, is.null, logical(1))])
  if (nrow(df) >= 8) {
    ## scipy.stats.spearmanr reports the asymptotic t p-value (rho on averaged
    ## ranks, t = rho*sqrt((n-2)/(1-rho^2)), 2-sided t with n-2 df) even when
    ## R's cor.test would switch to an exact permutation p — mirror scipy.
    rho <- cor(rank(df$MC_BDT_kg), rank(df$Net_profit_BDT_kg))
    nn <- nrow(df)
    tstat <- rho * sqrt((nn - 2) / (1 - rho^2))
    pval <- 2 * pt(-abs(tstat), df = nn - 2)
    df <- rbind(df, data.frame(Respondent_ID = "Spearman rho(MC, net margin)",
                               Market = sprintf("n=%d", nn),
                               Mean_margin_BDT_kg = NA,
                               MC_BDT_kg = rp(rho, 3),
                               Net_profit_BDT_kg = rp(pval, 4)))
  }
  list(name = "T17_Retailer_MC_Profit_Spearman",
       title = "Table 17. Retailer marketing cost vs net margin (Spearman)",
       note = paste("Retailers only (daily cost structure is unambiguous): MC/kg = (stall rent + ice +",
                    "wash/water/other, all BDT/day) / daily capacity kg; net margin = own-quote margin -",
                    "MC/kg. Spearman rho between MC and net margin (Methodology 3.8 Q5). Other strata mix",
                    "monthly/yearly/per-trip frequencies, so per-kg MC is not computed for them until the",
                    "cost module defines the period consistently (flagged in review)."),
       df = df)
}

## ============================================================================
## TABLE 18 — Shapiro-Wilk normality screening (pre-test, Method 3.8)
## ============================================================================
t18 <- function() {
  po <- DATA$PO
  cpf_yes <- DATA$CPF[!is.na(DATA$CPF$Purchased_today) & DATA$CPF$Purchased_today == "Yes", , drop = FALSE]
  series <- list(
    list(label = "Producer price - landing markets M1/M6 (Form A buy)",
         v = po$buy_kg[po$Actor_type == "Aratdar" & po$Market %in% LANDING & !is.na(po$buy_kg)]),
    list(label = "Aratdar auction sell - M1/M6",
         v = po$sell_kg[po$Actor_type == "Aratdar" & po$Market %in% LANDING & !is.na(po$sell_kg)]),
    list(label = "Bepari/Faria sell - all markets",
         v = po$sell_kg[po$Actor_type == "Bepari_Faria" & !is.na(po$sell_kg)]),
    list(label = "Khuchra retailer sell quotes - all markets",
         v = po$sell_kg[po$Actor_type == "Khuchra" & !is.na(po$sell_kg)]),
    list(label = "Consumer-paid prices (Form C slips)",
         v = cpf_yes$price_kg[!is.na(cpf_yes$price_kg)]))
  rows <- lapply(series, function(s) {
    v <- num(s$v); v <- v[!is.na(v)]
    if (length(v) < 3)
      return(data.frame(Series = s$label, n = length(v), W = NA, p_value = NA,
                        Decision = "n<3 - not tested"))
    sw <- shapiro.test(v)
    data.frame(Series = s$label, n = length(v), W = rp(as.numeric(sw$statistic), 4),
               p_value = rp(as.numeric(sw$p.value), 4),
               Decision = if (sw$p.value > 0.05)
                 "p>0.05 - normality not rejected"
               else "p<=0.05 - non-normal; nonparametric tests used")
  })
  df <- do.call(rbind, rows)
  list(name = "T18_ShapiroWilk_Screening",
       title = "Table 18. Shapiro-Wilk normality screening",
       note = paste("Shapiro-Wilk screening on pooled price series run BEFORE any inferential test, as",
                    "pre-registered in Methodology 3.8. Screening motivates the distribution-free battery",
                    "(Kruskal-Wallis / Mann-Whitney / Wilcoxon) used in Tables 12b/14/16."),
       df = df)
}

## ---------------------------------------------------------------------------
## BUILD ALL INFERENTIAL TABLES
## ---------------------------------------------------------------------------
build_inferential <- function() {
  list(t12(), t12b(), t13(), t14(), t14b(), t15(), t16(), t17(), t18())
}
