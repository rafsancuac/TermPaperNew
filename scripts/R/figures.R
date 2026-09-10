# ============================================================================
# figures.R — publication figures C1..C8
#   300 dpi PNG, Times New Roman (Windows) / serif (elsewhere), English labels
# Data sources: table objects built by tables_descriptive/inferential
# ============================================================================

## colour ramp for heatmap
heat_pal <- colorRampPalette(c("#F7FBFF", "#C6DBEF", "#6BAED6", "#2171B5", "#08306B"))

## ---------------------------------------------------------------------------
## C1 — price chain by species (grouped bars)
## ---------------------------------------------------------------------------
fig_c1 <- function(T3) {
  df <- T3[T3$Species_code != "ALL", , drop = FALSE]
  df <- df[order(-df$Consumer_paid_BDT_kg), , drop = FALSE]
  x <- seq_len(nrow(df)); k <- length(x)
  levs <- c("Producer_BDT_kg","Aratdar_sell_BDT_kg","Bepari_sell_BDT_kg",
            "Retailer_sell_BDT_kg","Consumer_paid_BDT_kg")
  cols <- c(COL_PRODUCER, COL_ARATDAR, COL_BEPARI, COL_RETAIL, COL_CONSUMER)
  labs <- c("Producer (net auction)","Aratdar sell","Bepari sell",
            "Retailer sell","Consumer paid")
  open_png(file.path(DIR_CHARTS, "C1_price_chain_by_species.png"), w = 12.5, h = 7.5)
  on.exit(close_png())
  ## extra left/bottom/top room: (a) stops the leading letter of the leftmost
  ## rotated species label ("S02...") from being clipped by the plot edge,
  ## (b) leaves headroom above the tallest bars for a top legend strip
  graphics::par(mar = c(7.0, 4.6, 3.6, 1.4))
  ymax <- max(sapply(levs, function(l) max(df[[l]], na.rm = TRUE)))
  plot.new(); plot.window(xlim = c(0.0, k + 0.7), ylim = c(0, ymax * 1.24))
  wd <- 0.16
  for (j in seq_along(levs)) {
    rect(x + (j - 3) * wd - wd/2, 0, x + (j - 3) * wd + wd/2, df[[levs[j]]],
         col = cols[j], border = "white", lwd = 0.4)
  }
  axis(1, at = x, labels = paste(df$Species_code, df$Local_name), las = 2, cex.axis = 0.7)
  axis(2); box()
  title(ylab = "BDT per kg",
        main = "Marine fish price chain by species - Chattogram markets, March 2026")
  ## legend as a horizontal strip ABOVE the bars (not "bottomright" inside the
  ## plot, which used to sit on top of the short S09/S10 bars) - reserved
  ## headroom above is ymax*1.08..ymax*1.24
  legend(x = mean(range(x)), y = ymax * 1.24, xjust = 0.5, yjust = 1,
         legend = labs, fill = cols, border = NA, cex = 0.8, bty = "n",
         horiz = TRUE, xpd = TRUE)
}

## ---------------------------------------------------------------------------
## C2 — producer's share by species
## ---------------------------------------------------------------------------
fig_c2 <- function(T3) {
  df <- T3[!is.na(T3$Producer_share_pct) & T3$Species_code != "ALL", , drop = FALSE]
  df <- df[order(df$Producer_share_pct), , drop = FALSE]
  overall <- T3$Producer_share_pct[T3$Species_code == "ALL"]
  open_png(file.path(DIR_CHARTS, "C2_producers_share.png"), w = 9, h = 7.5)
  on.exit(close_png())
  ## widen the left margin so the longest species labels ("S04 Koral/Kurl",
  ## "S02 Rupchanda") aren't clipped at the canvas edge
  graphics::par(mar = c(4.2, 7.8, 3.2, 1.2))
  ## names.arg = NA + explicit axis(2, ...) below, instead of letting
  ## barplot's own names.arg place the labels: with 8 close-set horizontal
  ## bars, barplot()/axis() was silently skipping every other category
  ## label to avoid overlap (S02, S03, S04, S06 were disappearing).
  ## Drawing the axis ourselves with tick = FALSE forces all 8 to render.
  xr <- barplot(df$Producer_share_pct, horiz = TRUE, col = COL_PRODUCER,
                border = NA, xlim = c(0, 110), names.arg = NA,
                xlab = "Producer share of consumer price (%)")
  axis(2, at = xr, labels = paste(df$Species_code, df$Local_name),
       las = 1, cex.axis = 0.8, tick = FALSE, line = -0.4)
  abline(v = overall, col = COL_CONSUMER, lty = 2, lwd = 1.8)
  mtext(sprintf("Pooled mean %.1f%%", overall), side = 1, at = overall + 2.5,
        col = COL_CONSUMER, cex = 0.85, adj = 0)
  text(df$Producer_share_pct - 1.5, xr, sprintf("%.0f", df$Producer_share_pct),
       adj = 1, col = "white", cex = 0.8)
  title(main = "Producer's share of the consumer's taka, by species")
}

## ---------------------------------------------------------------------------
## C3 — payment mix (stacked)
## ---------------------------------------------------------------------------
fig_c3 <- function(T5) {
  df <- T5[T5$Actor %in% c("Aratdar","Bepari/Faria","Retailer"), , drop = FALSE]
  mat <- as.matrix(df[, c("Cash_pct_mean","MFS_pct_mean","Credit_pct_mean")])
  cols <- c("#8C8C8C", "#2E8B57", "#C0504D")
  labs <- c("Cash","MFS (bKash/Nagad)","Credit")
  open_png(file.path(DIR_CHARTS, "C3_payment_mix.png"), w = 8.5, h = 5.5)
  on.exit(close_png())
  x <- barplot(t(mat), beside = FALSE, col = cols, border = NA, ylim = c(0, 100),
               names.arg = df$Actor, ylab = "Mean share of receipts (%)")
  for (j in seq_len(ncol(mat))) {
    cum0 <- if (j == 1) 0 else rowSums(mat[, seq_len(j - 1), drop = FALSE])
    yy <- cum0 + mat[, j] / 2
    text(x, yy, sprintf("%.0f%%", mat[, j]), col = "white", cex = 0.85)
  }
  legend("top", legend = labs, fill = cols, border = NA, bty = "n", ncol = 3, cex = 0.9)
  title(main = "How channel actors get paid (mean share of receipts)")
}

## ---------------------------------------------------------------------------
## C4 — education by actor
## ---------------------------------------------------------------------------
fig_c4 <- function(T1) {
  df <- T1[T1$Actor != "All traders", , drop = FALSE]
  edu <- c("Edu_Illiterate_pct","Edu_Primary_pct","Edu_Secondary_pct",
           "Edu_Higher Secondary_pct")
  elab <- c("Illiterate","Primary","Secondary","Higher Secondary")
  cols <- c(COL_PRODUCER, COL_ARATDAR, COL_BEPARI, COL_RETAIL)
  open_png(file.path(DIR_CHARTS, "C4_education.png"), w = 9.5, h = 5.5)
  on.exit(close_png())
  mat <- as.matrix(df[, edu, drop = FALSE])      # rows = actors (series)
  barplot(mat, beside = TRUE, col = cols, border = NA, names.arg = elab,
          ylab = "% of respondents", legend.text = df$Actor,
          args.legend = list(bty = "n", x = "top", ncol = 4, cex = 0.85),
          main = "Education level of trading actors")
}

## ---------------------------------------------------------------------------
## C5 — marketing problems (top 12)
## ---------------------------------------------------------------------------
fig_c5 <- function(T6) {
  df <- head(T6, 12)
  df <- df[order(df$Total_pct), , drop = FALSE]
  open_png(file.path(DIR_CHARTS, "C5_problems.png"), w = 10, h = 6.5)
  on.exit(close_png())
  xr <- barplot(df$Total_pct, horiz = TRUE, col = COL_ARATDAR, border = NA,
                xlim = c(0, max(df$Total_pct) * 1.25),
                names.arg = df$Problem, cex.names = 0.8,
                xlab = "% of traders mentioning (multi-response, n=90)")
  text(df$Total_pct + 1, xr, sprintf("%.0f%% (n=%d)", df$Total_pct, df$Total_n),
       adj = 0, cex = 0.8)
  title(main = "Leading marketing problems reported by traders")
}

## ---------------------------------------------------------------------------
## C6 — retail price heatmap (species x market)
## ---------------------------------------------------------------------------
fig_c6 <- function(T11) {
  mat <- as.matrix(T11[, -1, drop = FALSE])
  rownames(mat) <- T11$Species
  pal <- heat_pal(100)
  open_png(file.path(DIR_CHARTS, "C6_retail_price_heatmap.png"), w = 9.5, h = 6.5)
  on.exit(close_png())
  par(mar = c(6.5, 6, 3, 4.5))
  image(seq_len(ncol(mat)), seq_len(nrow(mat)), t(mat), col = pal, axes = FALSE,
        xlab = "", ylab = "")
  box()
  axis(1, at = seq_len(ncol(mat)), labels = colnames(mat), las = 2, cex.axis = 0.7)
  axis(2, at = seq_len(nrow(mat)), labels = rownames(mat), las = 1, cex.axis = 0.7)
  vmax <- max(mat, na.rm = TRUE)
  for (i in seq_len(nrow(mat))) for (j in seq_len(ncol(mat))) {
    v <- mat[i, j]
    if (!is.na(v)) text(j, i, sprintf("%.0f", v), cex = 0.75,
                        col = if (v > 0.55 * vmax) "white" else "#263238")
  }
  title(main = "Retailer selling prices by species and market (BDT/kg)", line = 1)
}

## ---------------------------------------------------------------------------
## C7 — daily capacity by actor (log)
## ---------------------------------------------------------------------------
fig_c7 <- function(DATA) {
  vals <- list(num(DATA$A$Daily_capacity_kg), num(DATA$B$Daily_capacity_kg),
               num(DATA$R$Daily_capacity_kg))
  vals <- lapply(vals, function(v) v[!is.na(v) & v > 0])
  labs <- sprintf("%s\n(n=%d)", c("Aratdar","Bepari/Faria","Retailer"),
                  lengths(vals))
  open_png(file.path(DIR_CHARTS, "C7_daily_capacity.png"), w = 8.5, h = 5.5)
  on.exit(close_png())
  boxplot(vals, names = labs, log = "y", col = c(COL_PRODUCER, COL_ARATDAR, COL_RETAIL),
          ylab = "Daily volume handled (kg, log scale)", border = "#333333")
  title(main = "Scale gap between channel actors (daily volume)")
}

## ---------------------------------------------------------------------------
## C8 — wholesale vs retail price per species (panels by market)
## ---------------------------------------------------------------------------
fig_c8 <- function(DATA) {
  po <- DATA$PO
  codes <- sort(unique(DATA$SP$Code))
  have <- sapply(codes, function(code) {
    sum(sapply(MKT_ORDER, function(m)
      length(po$sell_kg[po$Actor_type == "Bepari_Faria" & po$Market == m &
                          po$Species_code == code & !is.na(po$sell_kg)]) >= 1 &&
        length(po$sell_kg[po$Actor_type == "Khuchra" & po$Market == m &
                            po$Species_code == code & !is.na(po$sell_kg)]) >= 1))
  })
  panels <- names(which(have >= 4))[seq_len(min(8, sum(have >= 4)))]
  if (!length(panels)) return(invisible(NULL))
  ncol <- 2; nrow <- ceiling(length(panels) / ncol)
  open_png(file.path(DIR_CHARTS, "C8_retail_vs_wholesale_by_market.png"),
           w = 12.5, h = 3.8 * nrow)
  par(mfrow = c(nrow, ncol), mar = c(5, 4, 2.5, 1), oma = c(0.5, 0, 2.5, 0))
  on.exit(close_png())
  for (code in panels) {
    ws <- sapply(MKT_ORDER, function(m) {
      v <- po$sell_kg[po$Actor_type == "Bepari_Faria" & po$Market == m &
                        po$Species_code == code & !is.na(po$sell_kg)]
      if (length(v)) mean(v) else NA_real_
    })
    rs <- sapply(MKT_ORDER, function(m) {
      v <- po$sell_kg[po$Actor_type == "Khuchra" & po$Market == m &
                        po$Species_code == code & !is.na(po$sell_kg)]
      if (length(v)) mean(v) else NA_real_
    })
    nw <- sapply(MKT_ORDER, function(m)
      sum(po$Actor_type == "Bepari_Faria" & po$Market == m &
            po$Species_code == code & !is.na(po$sell_kg)))
    nr <- sapply(MKT_ORDER, function(m)
      sum(po$Actor_type == "Khuchra" & po$Market == m &
            po$Species_code == code & !is.na(po$sell_kg)))
    ymax <- max(c(ws, rs), na.rm = TRUE) * 1.2
    bp <- barplot(rbind(ws, rs), beside = TRUE, col = c(COL_BEPARI, COL_RETAIL),
                  border = NA, ylim = c(0, ymax), names.arg = rep("", 6),
                  ylab = "BDT/kg", main = sprintf("%s %s", code,
                    DATA$SP$Local_name[DATA$SP$Code == code]))
    for (j in seq_along(MKT_ORDER)) {
      if (!is.na(ws[j])) text(bp[1, j], ws[j] + ymax * 0.04, nw[j], cex = 0.65)
      if (!is.na(rs[j])) text(bp[2, j], rs[j] + ymax * 0.04, nr[j], cex = 0.65)
    }
    labs <- DATA$MK$Market_name[match(MKT_ORDER, DATA$MK$Code)]
    labs <- ifelse(nchar(labs) > 10, paste0(substr(labs, 1, 9), "."), labs)
    axis(1, at = colMeans(bp), labels = labs, las = 2, cex.axis = 0.65, tick = FALSE)
  }
  mtext("Wholesale vs retail price by market, Chattogram, March 2026 (labels = n quotes)",
        outer = TRUE, side = 3, cex = 1.0)
  legend("topright", legend = c("Wholesale (bepari sell)", "Retail (khuchra sell)"),
         fill = c(COL_BEPARI, COL_RETAIL), border = NA, bty = "n", cex = 0.8,
         xpd = NA)
}

## ---------------------------------------------------------------------------
## DRAW ALL FIGURES
## ---------------------------------------------------------------------------
build_figures <- function(TABLES) {
  fig_c1(TABLES[["T3_Price_Chain"]]$df)
  fig_c2(TABLES[["T3_Price_Chain"]]$df)
  fig_c3(TABLES[["T5_Payment_Methods"]]$df)
  fig_c4(TABLES[["T1_Respondent_Profile"]]$df)
  fig_c5(TABLES[["T6_Problems"]]$df)
  fig_c6(TABLES[["T11_Retail_Price_by_Market"]]$df)
  fig_c7(DATA)
  fig_c8(DATA)
  stamp("Figures C1-C8 written")
}
