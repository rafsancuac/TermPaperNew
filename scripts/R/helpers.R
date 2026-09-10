# ============================================================================
# helpers.R — small utilities shared by every analysis stage
# ============================================================================

## ---- numeric coercion (K/D flags, blanks -> NA) -----------------------------
num <- function(x) {
  if (is.null(x)) return(NA_real_)
  if (is.factor(x)) x <- as.character(x)
  if (is.character(x)) x <- trimws(x)
  out <- suppressWarnings(as.numeric(x))
  out
}

## ---- python-equivalent decimal rounding --------------------------------------
## Python's builtin round() decides on the exact real value of the double
## (via long-double scaling), whereas R's round() and numpy's np.round decide
## on the double x*10^d — which can already be rounded to the wrong side of a
## half boundary. sprintf('%.1100f') yields the exact finite decimal expansion
## of the double, so the half-even decision is made on exact digits.
rp <- function(x, nd = 0) {
  if (length(x) != 1) return(vapply(x, rp, numeric(1), nd = nd))
  if (is.null(x) || length(x) == 0) return(NA_real_)
  if (is.na(x)) return(x)
  if (!is.finite(x)) return(x)  # Inf, -Inf -> return as-is; NaN already NA above
  s0 <- sprintf("%.1100f", x)
  ## sprintf can return "Inf"/"-Inf"/"NaN" for non-finite (guarded above) or
  ## locale-dependent strings — bail out safely
  if (grepl("[^0-9.\\-]", s0)) return(x)
  neg <- substr(s0, 1, 1) == "-"
  s <- sub("-", "", s0, fixed = TRUE)
  sp <- strsplit(s, ".", fixed = TRUE)[[1]]
  if (length(sp) < 2) return(x)  # no decimal part -> unexpected, return original
  ints <- sp[1]
  frac <- sp[2]
  if (is.na(frac) || frac == "") return(as.numeric(ints) * if (neg) -1 else 1)
  if (nd == 0) {
    first <- substr(frac, 1, 1)
    if (is.na(first) || first == "") return(as.numeric(ints) * if (neg) -1 else 1)
    tail  <- substr(frac, 2, nchar(frac))
    last_int <- suppressWarnings(as.integer(substr(ints, nchar(ints), nchar(ints))))
    if (is.na(last_int)) last_int <- 0L
    up <- if (first < "5") 0L else if (first > "5") 1L else
      if (tail != "" && any(strsplit(tail, "")[[1]] != "0")) 1L else
        if (last_int %% 2 == 1) 1L else 0L
    if (up) ints <- as.character(suppressWarnings(as.numeric(ints) + 1))
    val <- suppressWarnings(as.numeric(ints))
  } else {
    keep <- substr(frac, 1, nd)
    d1   <- substr(frac, nd + 1, nd + 1)
    if (is.na(d1) || d1 == "") {
      val <- suppressWarnings(as.numeric(paste0(ints, ".", keep)))
      return(if (neg) -val else val)
    }
    tail <- substr(frac, nd + 2, nchar(frac))
    kd <- suppressWarnings(as.integer(substr(keep, nd, nd)))
    if (is.na(kd)) kd <- 0L
    up <- if (d1 < "5") 0L else if (d1 > "5") 1L else
      if (tail != "" && any(strsplit(tail, "")[[1]] != "0")) 1L else
        if (kd %% 2 == 1) 1L else 0L
    if (up) {
      nk <- suppressWarnings(as.numeric(keep) + 1)
      if (is.na(nk)) nk <- 0
      if (nk >= 10^nd) {
        ints <- as.character(suppressWarnings(as.numeric(ints) + 1))
        keep <- sprintf(paste0("%0", nd, "d"), nk - 10^nd)
      } else {
        keep <- sprintf(paste0("%0", nd, "d"), nk)
      }
    }
    val <- suppressWarnings(as.numeric(paste0(ints, ".", keep)))
  }
  if (is.na(val)) return(x)
  if (neg) -val else val
}

## ---- numpy-compatible sums / means / std ------------------------------------
## The Python pipeline rounds np.mean/np.std results, and numpy's double
## reduce uses a specific summation order (sequential below 8, an 8-accumulator
## block up to 128, then halving in multiples of 8). Replicating that order
## makes R and Python agree bit-for-bit, including on 2-decimal rounding
## boundaries where naive summation orders would disagree by 0.01.
np_sum <- function(x) {
  x <- as.double(x); n <- length(x)
  if (n == 0) return(0)
  if (n < 8) {
    s <- -0.0
    for (i in seq_len(n)) s <- s + x[i]
    return(s)
  }
  if (n <= 128) {
    r <- x[1:8]
    i <- 9L
    while (i + 7 <= n) { r <- r + x[i:(i + 7)]; i <- i + 8L }
    res <- ((r[1] + r[2]) + (r[3] + r[4])) + ((r[5] + r[6]) + (r[7] + r[8]))
    if (i <= n) for (j in i:n) res <- res + x[j]
    return(res)
  }
  n2 <- n %/% 2
  n2 <- n2 - n2 %% 8
  np_sum(x[seq_len(n2)]) + np_sum(x[(n2 + 1):n])
}
np_mean <- function(x) {
  x <- as.double(x)
  x <- x[!is.na(x)]
  if (!length(x)) return(NA_real_)
  np_sum(x) / length(x)
}
np_sd <- function(x) {
  x <- as.double(x)
  x <- x[!is.na(x)]
  n <- length(x)
  if (n < 2) return(NA_real_)
  m <- np_sum(x) / n
  sqrt(np_sum((x - m)^2) / (n - 1))
}

## ---- mean/sd with NA removal (2 decimals by default) -----------------------
mean_sd <- function(x, nd = 2) {
  x <- num(x); x <- x[!is.na(x)]
  if (length(x) == 0) return(c(mean = NA_real_, sd = NA_real_, n = 0L))
  m  <- rp(np_mean(x), nd)
  s  <- if (length(x) > 1) rp(np_sd(x), nd) else 0
  c(mean = m, sd = s, n = length(x))
}
mn <- function(x) unname(mean_sd(x)["mean"])     # rounded mean
sdv <- function(x) unname(mean_sd(x)["sd"])
cntn <- function(x) unname(mean_sd(x)["n"])      # count of numeric

## ---- maund/kg conversions (cached formula value preferred) ------------------
## Mirrors run_analysis.py `price_per_kg`/`qty_to_kg`: prefer the cached
## BDT-per-kg / kg cell, otherwise convert the raw quote from maund; every
## returned value is rounded to 2 decimals exactly as in the Python pipeline.
price_kg <- function(raw, unit, cached) {
  v <- num(cached)
  if (!is.na(v)) return(rp(v, 2))
  r <- num(raw)
  if (is.na(r)) return(NA_real_)
  u <- if (is.factor(unit)) as.character(unit) else unit
  u <- ifelse(is.na(u), "", trimws(u))
  if (identical(u, "Maund")) rp(r / MAUND, 2) else rp(r, 2)
}
qty_kg <- function(raw, unit, cached) {
  v <- num(cached)
  if (!is.na(v)) return(rp(v, 2))
  r <- num(raw)
  if (is.na(r)) return(NA_real_)
  u <- if (is.factor(unit)) as.character(unit) else unit
  u <- ifelse(is.na(u), "", trimws(u))
  if (identical(u, "Maund")) rp(r * MAUND, 2) else rp(r, 2)
}

## ---- category levels in Counter.most_common() order -------------------------
## Python's Counter.most_common() sorts by descending count with ties broken by
## first appearance in the sheet; empty/missing values are never emitted.
mc_names <- function(x) {
  x <- as.character(x)
  x <- x[!is.na(x) & x != ""]
  if (!length(x)) return(character(0))
  u <- unique(x)
  cnt <- tabulate(match(x, u), nbins = length(u))
  u[order(-cnt, seq_along(u))]
}

## ---- generic sheet reader ---------------------------------------------------
## Template layout: title rows 1-3, HEADERS row 4, DATA from row 5; col A is a
## blank margin column (readxl trims fully-empty leading columns itself).
## `fields` = internal names in column order B..(last). Column order of the
## file is checked and an informative error is raised if it ever changes.
read_tab <- function(sheet, fields) {
  raw <- as.data.frame(readxl::read_excel(INPUT_FILE, sheet = sheet, skip = 3),
                       stringsAsFactors = FALSE)
  if (ncol(raw) == length(fields) + 1 &&
      grepl("^\\.\\.\\.", names(raw)[1])) raw <- raw[, -1, drop = FALSE]
  if (ncol(raw) != length(fields))
    stop(sprintf("[%s] column-count mismatch: file has %d cols (%s); %d expected (%s)",
                 sheet, ncol(raw), paste(names(raw), collapse = ", "),
                 length(fields), paste(fields, collapse = ", ")))
  names(raw) <- fields
  raw
}

## Drop rows whose key (first) column is blank — mirrors openpyxl
## read_sheet_rows, which skips any row with an empty id cell (col B).
drop_id <- function(df) {
  k <- df[[1]]
  df[!(is.na(k) | (!is.na(k) & trimws(as.character(k)) == "")), , drop = FALSE]
}
## keep respondents with an interview date / with a non-empty key
has_date <- function(df, col = "Interview_Date") {
  df[!is.na(df[[col]]) & !as.character(df[[col]]) %in% c("", "NA"), , drop = FALSE]
}

## ---- CSV writer (UTF-8, English content -> opens cleanly in Excel) ----------
write_tbl <- function(df, file) {
  write.csv(df, file, row.names = FALSE, fileEncoding = "UTF-8", na = "")
  invisible(file)
}

## ---- round helpers ----------------------------------------------------------
r2 <- function(x) rp(x, 2)

## ---- progress ---------------------------------------------------------------
stamp <- function(msg) cat(sprintf("[%s] %s\n", format(Sys.time(), "%H:%M:%S"), msg))

## ---- figure device: PNG @300dpi, Times New Roman ---------------------------
open_png <- function(file, w = 9, h = 6, res = 300) {
  grDevices::png(file, width = w, height = h, units = "in", res = res,
                 family = FONT_FAMILY)
  graphics::par(family = FONT_FAMILY, mar = c(4.2, 4.2, 3.2, 1.2),
                mgp = c(2.4, 0.8, 0), tcl = -0.25, cex.axis = 0.85,
                cex.lab = 1.0, cex.main = 1.05, las = 0)
}
close_png <- function() grDevices::dev.off()

## ---- exact/statistical helpers (Methodology 3.8) ----------------------------
## Dunn's test (tie-corrected) with Holm step-down — mirrors extend_analysis.py
## `dunn_holm` exactly: rows are emitted in ascending raw-p order; the Holm
## factor is applied to UNROUNDED p-values with monotonicity enforced, and
## rounding to 3/4 decimals happens only for output. Returns a data.frame with
## Market_i, Market_j, z, raw_p, p_holm, significant_0.05 (Species added by the
## table builder afterwards, as in the Python reference).
dunn_holm <- function(groups, names, alpha = ALPHA) {
  k <- length(groups)
  pooled <- unlist(groups)
  N <- length(pooled)
  rk <- rank(pooled)                                  # ties averaged
  counts <- table(pooled)
  tie_corr <- sum(counts^3 - counts) / (12 * (N - 1))
  var_rank <- N * (N + 1) / 12 - tie_corr
  ends <- cumsum(c(0, lengths(groups)))
  gmean <- vapply(seq_len(k),
                  function(i) np_mean(rk[(ends[i] + 1):ends[i + 1]]), numeric(1))
  pr <- combn(k, 2)
  m <- ncol(pr)
  mat <- t(vapply(seq_len(m), function(p) {
    i <- pr[1, p]; j <- pr[2, p]
    se <- sqrt(var_rank * (1 / length(groups[[i]]) + 1 / length(groups[[j]])))
    z <- (gmean[i] - gmean[j]) / se
    c(i = i, j = j, z = z, p = 2 * pnorm(-abs(z)))
  }, numeric(4)))
  ord <- order(mat[, "p"], seq_len(m))                # ascending raw p, stable
  adj <- numeric(m)
  prev <- 0
  for (t in seq_len(m)) {
    a <- min(1, mat[ord[t], "p"] * (m - t + 1))
    a <- max(a, prev); prev <- a
    adj[t] <- a
  }
  out <- lapply(seq_len(m), function(t) {
    r0 <- ord[t]
    data.frame(Market_i = names[mat[r0, "i"]], Market_j = names[mat[r0, "j"]],
               z = rp(mat[r0, "z"], 3), raw_p = rp(mat[r0, "p"], 4),
               p_holm = rp(adj[t], 4),
               significant_0.05 = adj[t] < alpha)
  })
  do.call(rbind, out)
}
