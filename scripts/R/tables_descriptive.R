# ============================================================================
# tables_descriptive.R — descriptive tables T1..T11 (+T2b)
# Conventions identical to the methodology & pipeline (run_analysis.py):
#   * producer / auction price = landing-linked markets M1 & M6 only
#   * retail margin anchored to consumer-paid price (Form C slips)
#   * chain-complete species = all four stages AND >= MIN_CONS consumer quotes
#   * ALL row / Table 10 pool only chain-complete species (mean of species
#     means); K/D flagged prices excluded everywhere
# ============================================================================

## ---------------------------------------------------------------------------
## DATA LOADING (once, global `DATA`)
## ---------------------------------------------------------------------------
load_data <- function() {
  SP  <- drop_id(read_tab("Codebook_Species",
                  c("Code","Local_name","English_common_name","Scientific_name","Price_tier")))
  MK  <- drop_id(read_tab("Codebook_Markets",
                  c("Code","Market_name","Channel_position","Primary_analytical_contribution")))
  fA  <- c("Respondent_ID","Market","Interview_Date","Age_years","Education",
           "Years_in_business","Daily_capacity_raw","Daily_capacity_unit",
           "Daily_capacity_kg","Family_members","Rent_pay_or_receive",
           "Rent_amount_BDT","Rent_frequency","Commission_basis","Commission_rate",
           "Electricity_bill_BDT","Electricity_frequency","Workers_count",
           "Worker_daily_wage_BDT","Equipment_Cooler_Maintenance_BDT",
           "Equipment_Cooler_Maintenance_frequency","Other_cost_description",
           "Other_cost_BDT","Payment_cash_pct","Payment_MFS_pct",
           "Payment_credit_pct","MFS_transaction_frequency","Problem_1","Problem_2",
           "Problem_3","Pair_ID","Notes")
  fB  <- c("Respondent_ID","Market","Interview_Date","Actor_subtype","Business_pattern",
           "Age_years","Education","Years_in_business","Daily_capacity_raw",
           "Daily_capacity_unit","Daily_capacity_kg","Family_members","Source_location",
           "Supplier_category","Transport_fare_per_trip_BDT","Trip_frequency_days",
           "Trips_per_period","Loading_Unloading_cost_per_trip_BDT",
           "Ice_usage_kg_per_day","Ice_cost_BDT_per_day","Commission_to_aratdar_value",
           "Commission_unit","Transit_damage_pct","Payment_cash_pct","Payment_MFS_pct",
           "Payment_credit_pct","MFS_transaction_frequency","Credit_sales_share",
           "Problem_1","Problem_2","Problem_3","Pair_ID","Notes")
  fR  <- c("Respondent_ID","Market","Interview_Date","Age_years","Education",
           "Years_in_business","Daily_capacity_raw","Daily_capacity_unit",
           "Daily_capacity_kg","Family_members","Shop_Van_Rent_BDT_per_day",
           "Ice_cost_BDT_per_day","Wash_Water_Other_cost_BDT_per_day","Spoilage_pct",
           "Buys_from","Sells_to","Payment_cash_pct","Payment_MFS_pct",
           "Payment_credit_pct","MFS_transaction_frequency","Sells_on_credit",
           "Problem_1","Problem_2","Problem_3","Pair_ID","Notes")
  fC  <- c("Respondent_ID","Market","Interview_Date","Interview_time","Consent_given",
           "Visit_frequency","Visit_interval_days","Payment_method",
           "Main_reason_choosing_arat","Pair_ID","Notes")
  fPO <- c("Obs_ID","Respondent_ID","Market","Actor_type","Species_code",
           "Buy_price_raw","Sell_price_raw","Unit","Buy_BDT_per_kg","Sell_BDT_per_kg",
           "Quantity_raw","Quantity_unit","Quantity_kg","Pair_ID","Notes")
  fCPF<- c("Respondent_ID","Market","Species_code","Purchased_today","Bought_from",
           "Price_raw","Unit","Price_BDT_per_kg","Quantity_raw","Quantity_unit",
           "Quantity_kg","Notes")
  fCOF<- c("Respondent_ID","Market","Fish_name_local","Price_raw","Unit",
           "Price_BDT_per_kg","Quantity_raw","Quantity_unit","Quantity_kg",
           "Purchase_location","Notes")
  fM  <- c("Market","Market_name","Obs_Date","Market_type","Trading_hours",
           "Retail_stall_count","Transport_access","Platform_condition","Roofing",
           "Drainage","Electricity","Ice_availability","Ice_distance_note","Sanitation",
           "Water_supply","Fee_arrangement","Fee_rate_note","GPS_coordinates",
           "Photo_references","Evidence_source_note")

  A  <- has_date(drop_id(read_tab("Form_A_Aratdar", fA)))
  B  <- has_date(drop_id(read_tab("Form_B_Bepari_Faria", fB)))
  R  <- has_date(drop_id(read_tab("Form_R_Khuchra", fR)))
  C  <- has_date(drop_id(read_tab("Form_C_Consumer", fC)))
  PO <- drop_id(read_tab("Price_Observations", fPO))
  CPF<- drop_id(read_tab("Consumer_Purchases_Focal", fCPF))
  COF<- drop_id(read_tab("Consumer_Other_Fish", fCOF))
  COF<- COF[!is.na(COF$Fish_name_local) & COF$Fish_name_local != "", , drop = FALSE]
  M  <- has_date(drop_id(read_tab("Form_M_Market_Observation", fM)), "Obs_Date")

  PO$buy_kg  <- mapply(price_kg, PO$Buy_price_raw, PO$Unit, PO$Buy_BDT_per_kg)
  PO$sell_kg <- mapply(price_kg, PO$Sell_price_raw, PO$Unit, PO$Sell_BDT_per_kg)
  PO$qty_kg  <- mapply(qty_kg,  PO$Quantity_raw, PO$Quantity_unit, PO$Quantity_kg)
  CPF$price_kg <- mapply(price_kg, CPF$Price_raw, CPF$Unit, CPF$Price_BDT_per_kg)
  CPF$qty_kg   <- mapply(qty_kg,   CPF$Quantity_raw, CPF$Quantity_unit, CPF$Quantity_kg)
  COF$price_kg <- mapply(price_kg, COF$Price_raw, COF$Unit, COF$Price_BDT_per_kg)

  window <- range(na.omit(as.Date(c(A$Interview_Date, B$Interview_Date,
                                     R$Interview_Date, C$Interview_Date))))
  list(SP = SP, MK = MK, A = A, B = B, R = R, C = C, PO = PO, CPF = CPF,
       COF = COF, M = M, window = format(window, "%d/%m/%Y"))
}
if (!exists("DATA")) DATA <- load_data()

## ============================================================================
## TABLE 1 — socio-economic profile
## ============================================================================
t1 <- function() {
  edu_levels <- c("Illiterate", "Primary", "Secondary", "Higher_Secondary")
  pct1 <- function(v, n) if (n) rp(100 * v / n, 1) else 0
  prof_row <- function(label, rs) {
    n <- nrow(rs)
    data.frame(Actor = label, n = n,
               Age_mean_years = mn(rs$Age_years), Age_sd_years = sdv(rs$Age_years),
               Years_in_business_mean = mn(rs$Years_in_business),
               Years_in_business_sd = sdv(rs$Years_in_business),
               Family_size_mean = mn(rs$Family_members),
               Edu_Illiterate_pct = pct1(sum(rs$Education == "Illiterate", na.rm = TRUE), n),
               Edu_Primary_pct = pct1(sum(rs$Education == "Primary", na.rm = TRUE), n),
               Edu_Secondary_pct = pct1(sum(rs$Education == "Secondary", na.rm = TRUE), n),
               "Edu_Higher Secondary_pct" =
                 pct1(sum(rs$Education == "Higher_Secondary", na.rm = TRUE), n),
               check.names = FALSE)
  }
  bep <- DATA$B[DATA$B$Actor_subtype == "Bepari", , drop = FALSE]
  far <- DATA$B[DATA$B$Actor_subtype == "Faria",  , drop = FALSE]
  pc <- c("Age_years", "Years_in_business", "Family_members", "Education")
  all_t <- rbind(DATA$A[, pc, drop = FALSE], bep[, pc, drop = FALSE],
                 far[, pc, drop = FALSE], DATA$R[, pc, drop = FALSE])
  rows <- rbind(prof_row("Aratdar", DATA$A),
                prof_row("Bepari", bep),
                prof_row("Faria", far),
                prof_row("Retailer", DATA$R),
                prof_row("All traders", all_t))
  list(name = "T1_Respondent_Profile",
       title = "Table 1. Socio-economic profile of respondents",
       note = sprintf("Traders n=%d; consumers n=%d (profile items not collected for consumers). Survey window %s-%s.",
                      sum(rows$n[1:4]), nrow(DATA$C), DATA$window[1], DATA$window[2]),
       df = rows)
}

## ============================================================================
## TABLE 2 — business scale
## ============================================================================
t2 <- function() {
  cap_stats <- function(rs) {
    v <- num(rs$Daily_capacity_kg)
    data.frame(n = sum(!is.na(v)),
               Daily_capacity_kg_mean = mn(v), Daily_capacity_kg_sd = sdv(v),
               Daily_capacity_kg_median = rp(median(v, na.rm = TRUE), 1),
               Daily_capacity_kg_min = rp(min(v, na.rm = TRUE), 1),
               Daily_capacity_kg_max = rp(max(v, na.rm = TRUE), 1))
  }
  a <- cap_stats(DATA$A); b <- cap_stats(DATA$B); rr <- cap_stats(DATA$R)
  row1 <- cbind(data.frame(Actor = "Aratdar", n = a$n), a[, -1, drop = FALSE],
                data.frame(Workers_mean = mn(DATA$A$Workers_count),
                           Worker_wage_BDT_day_mean = mn(DATA$A$Worker_daily_wage_BDT),
                           Trips_per_period_mean = NA, Ice_use_kg_day_mean = NA,
                           Spoilage_pct_mean = NA))
  row2 <- cbind(data.frame(Actor = "Bepari/Faria", n = b$n), b[, -1, drop = FALSE],
                data.frame(Workers_mean = NA, Worker_wage_BDT_day_mean = NA,
                           Trips_per_period_mean = mn(DATA$B$Trips_per_period),
                           Ice_use_kg_day_mean = mn(DATA$B$Ice_usage_kg_per_day),
                           Spoilage_pct_mean = NA))
  row3 <- cbind(data.frame(Actor = "Retailer", n = rr$n), rr[, -1, drop = FALSE],
                data.frame(Workers_mean = NA, Worker_wage_BDT_day_mean = NA,
                           Trips_per_period_mean = NA, Ice_use_kg_day_mean = NA,
                           Spoilage_pct_mean = mn(DATA$R$Spoilage_pct)))
  rows <- rbind(row1, row2, row3)
  list(name = "T2_Business_Scale", title = "Table 2. Business scale of trading actors",
       note = "Daily traded/handled volume per actor group (kg/day).",
       df = rows)
}

## ============================================================================
## TABLE 2b — channel structure
## ============================================================================
t2b <- function() {
  ## Mirrors the Python t2b_channel: with a fixed category list every listed
  ## key is emitted (even at count 0, e.g. the literal "None" category row);
  ## without it, keys follow Counter.most_common() order (count desc, ties by
  ## first appearance in the sheet). Missing/blank values are never emitted.
  block <- function(form, rs, field, values = NULL) {
    x <- as.character(rs[[field]])
    keys <- if (is.null(values)) mc_names(x) else values[!(is.na(values) | values == "")]
    rows <- lapply(keys, function(k) {
      ck <- sum(x == k, na.rm = TRUE)
      data.frame(Form = form, Field = gsub("_", " ", field, fixed = TRUE),
                 Value = k, n = ck,
                 pct = rp(100 * ck / nrow(rs), 1))
    })
    do.call(rbind, rows)
  }
  bep <- DATA$B
  rows <- rbind(
    block("Form B (Bepari/Faria)", bep, "Actor_subtype"),
    block("Form B (Bepari/Faria)", bep, "Business_pattern"),
    block("Form B (Bepari/Faria)", bep, "Supplier_category"),
    block("Form B (Bepari/Faria)", bep, "Source_location"),
    block("Form B (Bepari/Faria)", bep, "Credit_sales_share",
          c("Almost_all","Some","None")),
    block("Form R (Retailer)", DATA$R, "Buys_from"),
    block("Form R (Retailer)", DATA$R, "Sells_to"),
    block("Form R (Retailer)", DATA$R, "Sells_on_credit",
          c("Almost_all","Some","None")))
  list(name = "T2b_Channel_Patterns",
       title = "Table 2b. Channel structure and trading patterns",
       note = "Channel structure: who supplies whom and on what terms (counts, % of form respondents).",
       df = rows)
}

## ============================================================================
## TABLE 3 — price chain by species (heart of the paper)
## ============================================================================
chain_species <- function() {                 # returns per-species chain rows
  po <- DATA$PO; cpf <- DATA$CPF
  cpf_yes <- cpf[!is.na(cpf$Purchased_today) & cpf$Purchased_today == "Yes", , drop = FALSE]
  codes <- sort(unique(DATA$SP$Code))
  lvl <- function(actor, field, code, mkts = NULL) {
    sel <- po[!is.na(po[[field]]) & po$Actor_type == actor &
                po$Species_code == code, , drop = FALSE]
    if (!is.null(mkts)) sel <- sel[sel$Market %in% mkts, , drop = FALSE]
    if (nrow(sel) == 0) NA_real_ else r2(np_mean(sel[[field]]))
  }
  cons_mean <- function(code) {
    v <- cpf_yes$price_kg[!is.na(cpf_yes$price_kg) & cpf_yes$Species_code == code]
    if (length(v) == 0) NA_real_ else r2(np_mean(v))
  }
  cons_n <- function(code) {
    sum(!is.na(cpf_yes$price_kg) & cpf_yes$Species_code == code)
  }
  rows <- lapply(codes, function(code) {
    sp <- DATA$SP[DATA$SP$Code == code, , drop = FALSE]
    n_obs <- sum(!is.na(po$buy_kg) & po$Species_code == code |
                   !is.na(po$sell_kg) & po$Species_code == code)
    ret_markets <- unique(po$Market[po$Actor_type == "Khuchra" &
                                      po$Species_code == code & !is.na(po$sell_kg)])
    cn <- cons_n(code)
    prod <- lvl("Aratdar", "buy_kg", code, LANDING)
    arat <- lvl("Aratdar", "sell_kg", code, LANDING)
    bep  <- lvl("Bepari_Faria", "sell_kg", code, NULL)
    retq <- lvl("Khuchra", "sell_kg", code, NULL)
    cons <- cons_mean(code)
    complete <- !anyNA(c(prod, arat, bep, cons)) && cn >= MIN_CONS

    reasons <- c()
    if (length(ret_markets) < 3)
      reasons <- c(reasons, sprintf("retail quotes in %d market(s)", length(ret_markets)))
    if (cn == 0) reasons <- c(reasons, "no consumer quotes")
    else if (cn < MIN_CONS)
      reasons <- c(reasons, sprintf("consumer quotes n=%d (<%d; share not reported)", cn, MIN_CONS))
    status <- if (length(reasons)) paste0("Descriptive-only (Method 3.8): ",
                                          paste(reasons, collapse = "; ")) else ""

    diff_ <- function(a, b) if (!anyNA(c(a, b))) r2(a - b) else NA_real_
    data.frame(Species_code = code, Local_name = sp$Local_name,
               English_name = sp$English_common_name, n_price_obs = n_obs,
               Retail_markets_n = length(ret_markets), Consumer_paid_n = cn,
               Reporting_status = status,
               Producer_BDT_kg = prod, Aratdar_sell_BDT_kg = arat,
               Bepari_sell_BDT_kg = bep, Retailer_sell_BDT_kg = retq,
               Consumer_paid_BDT_kg = cons,
               Aratdar_margin_BDT_kg = if (complete) diff_(arat, prod) else NA_real_,
               Bepari_margin_BDT_kg = if (complete) diff_(bep, arat) else NA_real_,
               Retailer_margin_BDT_kg = if (complete) diff_(cons, bep) else NA_real_,
               Total_spread_BDT_kg = if (complete) diff_(cons, prod) else NA_real_,
               Producer_share_pct = if (complete && !is.na(prod) && !is.na(cons))
                 rp(100 * prod / cons, 1) else NA_real_)
  })
  do.call(rbind, rows)
}
t3 <- function() {
  rows <- chain_species()
  comp <- rows[!is.na(rows$Total_spread_BDT_kg), , drop = FALSE]
  codes_all <- comp$Species_code
  n_all <- sum(!is.na(DATA$PO$buy_kg) & DATA$PO$Species_code %in% codes_all |
                 !is.na(DATA$PO$sell_kg) & DATA$PO$Species_code %in% codes_all)
  pl <- function(field) {
    v <- comp[[field]]
    if (!length(v)) NA_real_ else r2(np_mean(v))
  }
  prod_p <- pl("Producer_BDT_kg"); arat_p <- pl("Aratdar_sell_BDT_kg")
  bep_p  <- pl("Bepari_sell_BDT_kg"); ret_p <- pl("Retailer_sell_BDT_kg")
  cons_p <- pl("Consumer_paid_BDT_kg")
  allrow <- data.frame(
    Species_code = "ALL",
    Local_name = sprintf("Mean of species means (chain-complete: %s)",
                         paste(codes_all, collapse = ", ")),
    English_name = "-", n_price_obs = n_all, Retail_markets_n = NA,
    Consumer_paid_n = NA,
    Reporting_status = sprintf("Pooled over %d chain-complete species (consumer n >= %d)",
                               length(codes_all), MIN_CONS),
    Producer_BDT_kg = prod_p, Aratdar_sell_BDT_kg = arat_p,
    Bepari_sell_BDT_kg = bep_p, Retailer_sell_BDT_kg = ret_p,
    Consumer_paid_BDT_kg = cons_p,
    Aratdar_margin_BDT_kg = r2(arat_p - prod_p),
    Bepari_margin_BDT_kg = r2(bep_p - arat_p),
    Retailer_margin_BDT_kg = r2(cons_p - bep_p),
    Total_spread_BDT_kg = r2(cons_p - prod_p),
    Producer_share_pct = rp(100 * prod_p / cons_p, 1))
  df <- rbind(rows, allrow)
  list(name = "T3_Price_Chain",
       title = "Table 3. Price chain by species (BDT per kg)",
       note = paste("Producer price = net auction price paid to fishers (Form A buy) at the",
                    "landing-linked markets M1/M6 only; Aratdar sell = auction hammer price at M1/M6;",
                    "Bepari sell = Form B sell over all markets; Retailer sell = Form R vendor quote",
                    "(descriptive; margins use the consumer-paid anchor); Consumer = focal-species",
                    "purchases actually paid (Form C). Margins are differences of consecutive level means",
                    "and telescope to the total spread. K/D-flagged prices excluded. Species without a complete",
                    "chain - or with fewer than MIN_CONS consumer-paid observations - show prices but blank",
                    "margins/share and are excluded from ALL (see Local_name note); Consumer_paid_n reports",
                    "the actual number of consumer slips behind each share. Reporting_status lists Method 3.8",
                    "descriptive-only reasons."),
       df = df)
}

## ============================================================================
## TABLE 4 — marketing costs
## ============================================================================
t4 <- function() {
  add <- function(actor, item, unit, rs, field, note_txt = "") {
    ms <- mean_sd(num(rs[[field]]))
    data.frame(Actor = actor, Cost_item = item, Unit = unit, n = ms["n"],
               Mean = ms["mean"], SD = ms["sd"], Note = note_txt)
  }
  A <- DATA$A; B <- DATA$B; Rp <- DATA$R
  rows <- rbind(
    add("Aratdar","Commission rate","% of lot value",
        A[A$Commission_basis == "Percent", , drop = FALSE], "Commission_rate",
        "Percent-basis aratdars only"),
    add("Aratdar","Arat/office rent (yearly payers)","BDT per year",
        A[A$Rent_frequency == "Yearly", , drop = FALSE], "Rent_amount_BDT"),
    add("Aratdar","Arat/office rent (monthly payers)","BDT per month",
        A[A$Rent_frequency == "Monthly", , drop = FALSE], "Rent_amount_BDT"),
    add("Aratdar","Electricity bill (monthly payers)","BDT per month",
        A[A$Electricity_frequency == "Monthly", , drop = FALSE], "Electricity_bill_BDT"),
    add("Aratdar","Electricity bill (yearly payers)","BDT per year",
        A[A$Electricity_frequency == "Yearly", , drop = FALSE], "Electricity_bill_BDT"),
    add("Aratdar","Workers employed","persons", A, "Workers_count","Own/family + hired"),
    add("Aratdar","Worker daily wage","BDT per day", A, "Worker_daily_wage_BDT"),
    add("Aratdar","Equipment & cooler maintenance (yearly)","BDT per year",
        A[A$Equipment_Cooler_Maintenance_frequency == "Yearly", , drop = FALSE],
        "Equipment_Cooler_Maintenance_BDT"),
    add("Aratdar","Other operating cost","BDT per period", A, "Other_cost_BDT",
        "See Other_cost_description in Form A"),
    add("Bepari/Faria","Transport fare per trip","BDT per trip", B, "Transport_fare_per_trip_BDT"),
    add("Bepari/Faria","Trips per period","trips", B, "Trips_per_period"),
    add("Bepari/Faria","Loading/unloading cost","BDT per trip", B, "Loading_Unloading_cost_per_trip_BDT"),
    add("Bepari/Faria","Ice usage","kg per day", B, "Ice_usage_kg_per_day"),
    add("Bepari/Faria","Ice cost","BDT per day", B, "Ice_cost_BDT_per_day"),
    add("Bepari/Faria","Commission paid to aratdar (percent basis)","% of lot",
        B[B$Commission_unit == "Percent_of_lot", , drop = FALSE], "Commission_to_aratdar_value"),
    add("Bepari/Faria","Commission paid to aratdar (flat basis)","BDT per lot",
        B[B$Commission_unit == "BDT_per_lot", , drop = FALSE], "Commission_to_aratdar_value"),
    add("Bepari/Faria","Transit damage/loss","% of lot", B, "Transit_damage_pct"),
    add("Retailer","Shop/van rent","BDT per day", Rp, "Shop_Van_Rent_BDT_per_day"),
    add("Retailer","Ice cost","BDT per day", Rp, "Ice_cost_BDT_per_day"),
    add("Retailer","Washing, water & other","BDT per day", Rp, "Wash_Water_Other_cost_BDT_per_day"),
    add("Retailer","Spoilage/unsold loss","% of purchase", Rp, "Spoilage_pct"))
  list(name = "T4_Marketing_Costs", title = "Table 4. Marketing costs by channel actor",
       note = "Mean marketing costs by actor (mixed frequencies kept separate - do not sum rows).",
       df = rows)
}

## ============================================================================
## TABLE 5 — payment methods
## ============================================================================
t5 <- function() {
  ## Column layout mirrors the Python reference (base keys first, Actor/n last:
  ## every row is a dict built from the same ordered base keys).
  act <- function(label, rs) {
    data.frame(Cash_pct_mean = mn(rs$Payment_cash_pct),
               MFS_pct_mean = mn(rs$Payment_MFS_pct),
               Credit_pct_mean = mn(rs$Payment_credit_pct),
               MFS_Regular_n = sum(rs$MFS_transaction_frequency == "Regular", na.rm = TRUE),
               MFS_Occasional_n = sum(rs$MFS_transaction_frequency == "Occasional", na.rm = TRUE),
               MFS_Never_n = sum(rs$MFS_transaction_frequency == "Never", na.rm = TRUE),
               Payment_method = NA_character_, Payment_method_pct = NA_real_,
               Actor = label, n = nrow(rs))
  }
  keys <- mc_names(DATA$C$Payment_method)
  ck <- vapply(keys, function(k) sum(DATA$C$Payment_method == k, na.rm = TRUE), integer(1))
  cons_rows <- data.frame(
    Cash_pct_mean = NA, MFS_pct_mean = NA, Credit_pct_mean = NA,
    MFS_Regular_n = NA, MFS_Occasional_n = NA, MFS_Never_n = NA,
    Payment_method = keys,
    Payment_method_pct = rp(100 * ck / nrow(DATA$C), 1),
    Actor = "Consumer (Form C)", n = nrow(DATA$C))
  df <- rbind(act("Aratdar", DATA$A), act("Bepari/Faria", DATA$B),
              act("Retailer", DATA$R), cons_rows)
  list(name = "T5_Payment_Methods", title = "Table 5. Payment methods across the channel",
       note = paste("Trader rows: mean share of sales receipts settled by cash / mobile financial",
                    "services (bKash, Nagad) / credit. Consumer row: % choosing each payment method."),
       df = df)
}

## ============================================================================
## TABLE 6 — marketing problems (deterministic ordering)
## ============================================================================
t6 <- function() {
  slot_mentions <- function(rs, p) {
    sum(rs$Problem_1 == p | rs$Problem_2 == p | rs$Problem_3 == p, na.rm = TRUE)
  }
  probs <- unique(c(na.omit(c(DATA$A$Problem_1, DATA$A$Problem_2, DATA$A$Problem_3)),
                    na.omit(c(DATA$B$Problem_1, DATA$B$Problem_2, DATA$B$Problem_3)),
                    na.omit(c(DATA$R$Problem_1, DATA$R$Problem_2, DATA$R$Problem_3))))
  nA <- nrow(DATA$A); nB <- nrow(DATA$B); nR <- nrow(DATA$R)
  rows <- lapply(probs, function(p) {
    a <- slot_mentions(DATA$A, p); b <- slot_mentions(DATA$B, p); rr <- slot_mentions(DATA$R, p)
    data.frame(Problem = p, Aratdar_n = a, Aratdar_pct = rp(100 * a / nA, 1),
               Bepari_n = b, Bepari_pct = rp(100 * b / nB, 1),
               Retailer_n = rr, Retailer_pct = rp(100 * rr / nR, 1),
               Total_n = a + b + rr,
               Total_pct = rp(100 * (a + b + rr) / (nA + nB + nR), 1))
  })
  df <- do.call(rbind, rows)
  df <- df[order(-df$Total_n, df$Problem), , drop = FALSE]
  list(name = "T6_Problems", title = "Table 6. Marketing problems reported by traders",
       note = "% = share of that actor's respondents mentioning the problem in any of the 3 slots (multi-response).",
       df = df)
}

## ============================================================================
## TABLE 7 — market infrastructure (Form M)
## ============================================================================
t7 <- function() {
  df <- DATA$M
  out <- data.frame(
    Market = df$Market, Market_name = df$Market_name,
    Obs_date = format(as.Date(df$Obs_Date), "%d/%m/%Y"),
    Type = df$Market_type, Trading_hours = df$Trading_hours,
    Retail_stalls = df$Retail_stall_count,
    Transport_access = df$Transport_access,
    Platform = df$Platform_condition, Roofing = df$Roofing,
    Drainage = df$Drainage, Electricity = df$Electricity,
    Ice = df$Ice_availability, Sanitation = df$Sanitation,
    Water_supply = df$Water_supply, Fee_arrangement = df$Fee_arrangement,
    Fee_rate_note = df$Fee_rate_note, GPS = df$GPS_coordinates,
    stringsAsFactors = FALSE)
  list(name = "T7_Market_Infrastructure",
       title = "Table 7. Market infrastructure (Form M observation)",
       note = "Form M direct market observation, one row per market.", df = out)
}

## ============================================================================
## TABLE 8 — consumer behaviour
## ============================================================================
t8 <- function() {
  C <- DATA$C; CPF <- DATA$CPF
  block <- function(field, label) {
    keys <- mc_names(C[[field]])
    ck <- vapply(keys, function(k) sum(C[[field]] == k, na.rm = TRUE), integer(1))
    data.frame(Item = label, Value = keys, n = ck,
               pct = rp(100 * ck / nrow(C), 1))
  }
  rows <- rbind(block("Visit_frequency", "Visit frequency"),
                block("Payment_method", "Payment method"),
                block("Main_reason_choosing_arat", "Main reason for choosing seller"))
  vi <- mean_sd(num(C$Visit_interval_days))
  rows <- rbind(rows, data.frame(Item = "Mean visit interval (days)",
                                 Value = vi["mean"], n = vi["n"], pct = NA))
  keys <- mc_names(CPF$Bought_from)
  if (length(keys)) {
    ck <- vapply(keys, function(k) sum(CPF$Bought_from == k, na.rm = TRUE), integer(1))
    rows <- rbind(rows, data.frame(Item = "Focal purchase source (per purchase)",
                                   Value = keys, n = ck,
                                   pct = rp(100 * ck / nrow(CPF), 1)))
  }
  yes <- CPF[!is.na(CPF$Purchased_today) & CPF$Purchased_today == "Yes", , drop = FALSE]
  mp <- mean_sd(yes$price_kg); mq <- mean_sd(yes$qty_kg)
  rows <- rbind(rows,
    data.frame(Item = "Mean focal-species price paid (BDT/kg)", Value = mp["mean"],
               n = mp["n"], pct = NA),
    data.frame(Item = "Mean purchase size (kg)", Value = mq["mean"],
               n = mq["n"], pct = NA))
  list(name = "T8_Consumer_Behaviour", title = "Table 8. Consumer behaviour",
       note = sprintf("Consumers n=%d; focal purchases n=%d (Yes today n=%d).",
                      nrow(C), nrow(CPF), nrow(yes)),
       df = rows)
}

## ============================================================================
## TABLE 9 — other (non-focal) aquatic products
## ============================================================================
t9 <- function() {
  COF <- DATA$COF
  nm <- mc_names(COF$Fish_name_local)
  rows <- lapply(nm, function(nm_i) {
    rs <- COF[!is.na(COF$Fish_name_local) & COF$Fish_name_local == nm_i, , drop = FALSE]
    data.frame(`Fish (local name)` = nm_i, n = nrow(rs),
               Mean_price_BDT_kg = mn(rs$price_kg),
               Mean_qty_kg = mn(num(rs$Quantity_raw)), check.names = FALSE)
  })
  df <- do.call(rbind, rows)
  list(name = "T9_Other_Fish",
       title = "Table 9. Other aquatic products purchased by consumers",
       note = paste("Non-focal aquatic items consumers reported buying on the interview day",
                    "(Consumer_Other_Fish sheet). Includes crustaceans (Bagda shrimp, Kakra crab) and",
                    "finfish (Khoira, Datina, Moid, Faisya, lobster) - comparison items outside the ten",
                    "focal marine-finfish species of Table 3.4."),
       df = df)
}

## ============================================================================
## TABLE 10 — channel margins & producer's share (chain-complete pool)
## ============================================================================
t10 <- function() {
  rows <- chain_species()
  comp <- rows[!is.na(rows$Total_spread_BDT_kg), , drop = FALSE]
  n_sp <- nrow(comp)
  pl <- function(field) if (n_sp) r2(np_mean(comp[[field]])) else NA_real_
  prod <- pl("Producer_BDT_kg"); arat <- pl("Aratdar_sell_BDT_kg")
  bep  <- pl("Bepari_sell_BDT_kg"); cons <- pl("Consumer_paid_BDT_kg")
  pct <- function(x) if (!is.na(x) && !is.na(cons)) rp(100 * x / cons, 1) else NA_real_
  df <- data.frame(
    Level = c("Aratdar (auction margin, M1/M6)",
              "Bepari/Faria (wholesale margin)",
              "Retailer (margin to consumer)",
              "Total marketing spread (consumer - producer)",
              "Producer share of consumer price"),
    n_species = c(n_sp, n_sp, n_sp, n_sp, n_sp),
    Margin_BDT_kg = c(r2(arat - prod), r2(bep - arat), r2(cons - bep),
                      r2(cons - prod), NA_real_),
    Margin_pct_consumer = c(pct(arat - prod), pct(bep - arat), pct(cons - bep),
                            pct(cons - prod), pct(prod)))
  list(name = "T10_Margin_Summary",
       title = "Table 10. Channel margins and producer's share",
       note = paste("Unweighted means of species-level means over chain-complete species only",
                    "(n_species shown; see Table 3 note). Producer & auction prices from landing-linked",
                    "markets M1/M6 (first-sale proxy, Methodology 3.11c); wholesale price = Bepari sell",
                    "over all markets; retail price = consumer-paid anchor (Form C slips). Margins are",
                    "differences of consecutive level means, so they sum exactly to the total spread and",
                    "PS% + spread% = 100. Margin % is expressed as a share of the pooled consumer price."),
       df = df)
}

## ============================================================================
## TABLE 11 — retail price by species and market (khuchra sell quotes)
## ============================================================================
t11 <- function() {
  po <- DATA$PO
  codes <- sort(unique(DATA$SP$Code))
  mkt_names <- vapply(MKT_ORDER, function(m) DATA$MK$Market_name[DATA$MK$Code == m], "")
  rows <- lapply(codes, function(code) {
    base <- data.frame(Species = sprintf("%s %s", code,
                                         DATA$SP$Local_name[DATA$SP$Code == code]))
    vals <- lapply(MKT_ORDER, function(m) {
      v <- po$sell_kg[po$Actor_type == "Khuchra" & po$Market == m &
                        po$Species_code == code & !is.na(po$sell_kg)]
      if (length(v)) rp(np_mean(v), 0) else NA_real_
    })
    df <- cbind(base, as.data.frame(vals, check.names = FALSE))
    names(df)[-1] <- mkt_names
    df
  })
  df <- do.call(rbind, rows)
  list(name = "T11_Retail_Price_by_Market",
       title = "Table 11. Retail prices by species and market (BDT per kg)",
       note = "Mean retailer (khuchra) selling price, BDT/kg, by market. Blank = not observed.",
       df = df)
}

## ---------------------------------------------------------------------------
## BUILD ALL DESCRIPTIVE TABLES
## ---------------------------------------------------------------------------
build_descriptive <- function() {
  list(t1(), t2(), t2b(), t3(), t4(), t5(), t6(), t7(), t8(), t9(), t10(), t11())
}
