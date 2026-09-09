# ============================================================================
# excel_out.R — styled Excel workbook of every table (openxlsx)
# ============================================================================
write_excel <- function(TABLES) {
  wb <- openxlsx::createWorkbook()
  ## Index sheet
  openxlsx::addWorksheet(wb, "Index")
  openxlsx::writeData(wb, "Index", x = data.frame(
    Sheet = names(TABLES), `Table title` = vapply(TABLES, `[[`, "", "title"),
    Rows = vapply(TABLES, function(t) nrow(t$df), integer(1)),
    Cols = vapply(TABLES, function(t) ncol(t$df), integer(1))),
    startCol = 2, startRow = 5)
  openxlsx::writeData(wb, "Index",
                      "MS-499 R analysis summary - Marine Fish Marketing, Chattogram 2026",
                      startCol = 2)
  openxlsx::addStyle(wb, "Index", openxlsx::createStyle(textDecoration = "bold",
                     fontSize = 14, fontColour = paste0("#", HDR_FILL)),
                     rows = 2, cols = 2)
  openxlsx::addStyle(wb, "Index", openxlsx::createStyle(textDecoration = "bold",
                     fgFill = paste0("#", HDR_FILL), fontColour = "white"),
                     rows = 5, cols = 2:5)
  hdr_style <- openxlsx::createStyle(textDecoration = "bold", fgFill = paste0("#", HDR_FILL),
                                     fontColour = "white", halign = "center", wrapText = TRUE)
  band_style <- openxlsx::createStyle(fgFill = paste0("#", BAND_FILL))
  title_style <- openxlsx::createStyle(textDecoration = "bold", fontSize = 13,
                                       fontColour = paste0("#", HDR_FILL))
  note_style <- openxlsx::createStyle(fontSize = 9, fontColour = "#808080",
                                      textDecoration = "italic", wrapText = TRUE)

  for (nm in names(TABLES)) {
    t <- TABLES[[nm]]
    sn <- substr(nm, 1, 31)
    openxlsx::addWorksheet(wb, sn)
    openxlsx::writeData(wb, sn, t$df, startCol = 2, startRow = 5)
    openxlsx::writeData(wb, sn, t$title, startCol = 2)
    openxlsx::writeData(wb, sn, t$note, startCol = 2, startRow = 3)
    openxlsx::addStyle(wb, sn, title_style, rows = 2, cols = 2)
    openxlsx::addStyle(wb, sn, note_style, rows = 3, cols = 2)
    openxlsx::addStyle(wb, sn, hdr_style,
                       rows = 4, cols = 2:(ncol(t$df) + 1),
                       gridExpand = TRUE)
    if (nrow(t$df) > 1)
      openxlsx::addStyle(wb, sn, band_style,
                         rows = seq(6, 4 + nrow(t$df), by = 2),
                         cols = 2:(ncol(t$df) + 1), gridExpand = TRUE)
    openxlsx::freezePane(wb, sn, firstActiveRow = 5, firstActiveCol = 3)
  }
  openxlsx::saveWorkbook(wb, XLSX_OUT, overwrite = TRUE)
  cat("Workbook written:", XLSX_OUT, "\n")
}

## ---------------------------------------------------------------------------
## QUALITY GATES — re-checked inside R before finishing
## ---------------------------------------------------------------------------
quality_gates <- function(TABLES) {
  T3 <- TABLES[["T3_Price_Chain"]]$df; T10 <- TABLES[["T10_Margin_Summary"]]$df
  allr <- T3[T3$Species_code == "ALL", , drop = FALSE]
  A <- allr$Aratdar_margin_BDT_kg; B <- allr$Bepari_margin_BDT_kg
  R <- allr$Retailer_margin_BDT_kg; spread <- allr$Total_spread_BDT_kg
  ps <- allr$Producer_share_pct
  ok1 <- abs((A + B + R) - spread) < 0.05
  ok2 <- abs(ps - 100 * (1 - spread / allr$Consumer_paid_BDT_kg)) < 0.15
  t10ps <- T10$Margin_pct_consumer[T10$Level == "Producer share of consumer price"]
  ok3 <- abs(ps - t10ps) < 0.15
  cat("\n---------------- QUALITY GATES ----------------\n")
  cat(sprintf("Margins telescope: A+B+R = %.2f vs spread = %.2f  [%s]\n",
              A + B + R, spread, if (ok1) "PASS" else "FAIL"))
  cat(sprintf("PS + spread%% = 100: PS %.1f%%  [%s]\n", ps, if (ok2) "PASS" else "FAIL"))
  cat(sprintf("T3 ALL matches T10: %.1f%% vs %.1f%%  [%s]\n", ps, t10ps,
              if (ok3) "PASS" else "FAIL"))
  cat("-----------------------------------------------\n")
  invisible(ok1 && ok2 && ok3)
}
