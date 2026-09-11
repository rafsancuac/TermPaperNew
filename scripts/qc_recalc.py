#!/usr/bin/env python3
"""Recompute the QC_Check sheet and the derived (blue) columns in Python.

Why this exists
---------------
The workbook's QC_Check sheet and the blue "derived" columns (capacity in kg,
price per kg, quantity in kg) are spreadsheet formulas. They only carry a
*value* after a spreadsheet engine has recalculated and saved the file. When
the workbook is regenerated on a machine without LibreOffice/Excel, those
cached values are absent, and any consumer reading with ``data_only=True``
sees ``None``.

Two failure modes followed from that, both of which this module closes:

1. ``verify_filled.py`` treated a ``None`` status as a pass, so an
   unrecalculated workbook reported "24/24 PASS" on the strength of nothing.
2. ``run_analysis.py`` read ``Daily_capacity_kg`` with no fallback, so an
   unrecalculated workbook broke Tables 2 and 4b.

Reimplementing the 24 COUNTIF/SUMPRODUCT checks in Python makes the pipeline
independent of any spreadsheet engine: the numbers are produced the same way
every time, on every machine.

The formulas reproduced here are the ones in ``QC_Check!C6:E29`` of
``03_data_entry_template/Marine_Fish_Marketing_Data_Entry (1).xlsx``.
"""
import openpyxl

MAUND = 37.32

# QC row -> (short key, human label, rule text). Statuses are derived below.
# Column letters follow the template so the mapping stays auditable.
SHEET_COLS = {
    "Form_A_Aratdar": dict(rid="B", date="D", cash="Y", mfs="Z", credit="AA", pair="AF"),
    "Form_B_Bepari_Faria": dict(rid="B", date="D", cash="Y", mfs="Z", credit="AA", pair="AG"),
    "Form_R_Khuchra": dict(rid="B", date="D", cash="R", mfs="S", credit="T", pair="Z"),
    "Form_C_Consumer": dict(rid="B", date="D"),
    "Price_Observations": dict(rid="C", buy="G", sell="H", unit="I", pair="O"),
    "Consumer_Purchases_Focal": dict(rid="B", price="G", unit="H"),
    "Consumer_Other_Fish": dict(rid="B", price="E", unit="F"),
    "Form_M_Market_Observation": dict(date="D"),
}
ROW_RANGES = {
    "Form_A_Aratdar": (5, 40), "Form_B_Bepari_Faria": (5, 40),
    "Form_R_Khuchra": (5, 40), "Form_C_Consumer": (5, 40),
    "Price_Observations": (5, 504), "Consumer_Purchases_Focal": (5, 354),
    "Consumer_Other_Fish": (5, 104), "Form_M_Market_Observation": (5, 10),
}


def col_index(letter):
    n = 0
    for ch in str(letter).upper():
        n = n * 26 + (ord(ch) - 64)
    return n


def column(wb, sheet, key):
    """All values in a sheet column over the template's data rows."""
    ws = wb[sheet]
    ci = col_index(SHEET_COLS[sheet][key])
    r0, r1 = ROW_RANGES[sheet]
    return [ws.cell(row=r, column=ci).value for r in range(r0, r1 + 1)]


def _isnum(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _nonblank(v):
    return v is not None and str(v).strip() != ""


def compute_qc(wb):
    """Return {row: (value, status)} for QC_Check rows 6..29."""
    out = {}

    # --- rows 6-9: rows entered per form -----------------------------------
    counts = {}
    for row, sh in ((6, "Form_A_Aratdar"), (7, "Form_B_Bepari_Faria"),
                    (8, "Form_R_Khuchra"), (9, "Form_C_Consumer")):
        vals = column(wb, sh, "date")
        n = sum(1 for v in vals if _nonblank(v))
        counts[sh] = n
        out[row] = (n, "OK" if n <= 36 else "Over capacity")

    # --- row 10: total interviews ------------------------------------------
    total = sum(counts.values())
    status = ("TARGET MET" if total == 120
              else "In progress" if total < 120 else "Over quota")
    out[10] = (total, status)

    # --- rows 11-14: duplicate respondent IDs ------------------------------
    for row, sh in ((11, "Form_A_Aratdar"), (12, "Form_B_Bepari_Faria"),
                    (13, "Form_R_Khuchra"), (14, "Form_C_Consumer")):
        ids = [v for v in column(wb, sh, "rid") if _nonblank(v)]
        seen = {}
        for i in ids:
            seen[i] = seen.get(i, 0) + 1
        dup_rows = sum(c for c in seen.values() if c > 1)
        out[row] = (dup_rows, "OK" if dup_rows == 0 else "Fix duplicates")

    # --- rows 15-17: payment shares must sum to 100 ------------------------
    for row, sh in ((15, "Form_A_Aratdar"), (16, "Form_B_Bepari_Faria"),
                    (17, "Form_R_Khuchra")):
        c = column(wb, sh, "cash")
        m = column(wb, sh, "mfs")
        k = column(wb, sh, "credit")
        bad = 0
        for i in range(len(c)):
            if _nonblank(c[i]):
                s = (c[i] or 0) + (m[i] or 0) + (k[i] or 0)
                if abs(float(s) - 100.0) > 1e-9:
                    bad += 1
        out[row] = (bad, "OK" if bad == 0 else "Check rows")

    po_buy = column(wb, "Price_Observations", "buy")
    po_sell = column(wb, "Price_Observations", "sell")
    po_unit = column(wb, "Price_Observations", "unit")
    po_rid = column(wb, "Price_Observations", "rid")

    # --- rows 18-19: numeric price recorded without a unit -----------------
    for row, series in ((18, po_buy), (19, po_sell)):
        bad = sum(1 for i, v in enumerate(series)
                  if _isnum(v) and not _nonblank(po_unit[i]))
        out[row] = (bad, "OK" if bad == 0 else "Fill Unit column")

    # --- row 20: price rows whose respondent ID is unknown -----------------
    known = set()
    for sh in ("Form_A_Aratdar", "Form_B_Bepari_Faria", "Form_R_Khuchra"):
        known |= {v for v in column(wb, sh, "rid") if _nonblank(v)}
    bad = sum(1 for v in po_rid if _nonblank(v) and v not in known)
    out[20] = (bad, "OK" if bad == 0 else "Fix IDs")

    cpf_price = column(wb, "Consumer_Purchases_Focal", "price")
    cpf_unit = column(wb, "Consumer_Purchases_Focal", "unit")
    cpf_rid = column(wb, "Consumer_Purchases_Focal", "rid")
    cof_price = column(wb, "Consumer_Other_Fish", "price")
    cof_unit = column(wb, "Consumer_Other_Fish", "unit")
    cof_rid = column(wb, "Consumer_Other_Fish", "rid")

    # --- rows 21-22: consumer-sheet prices missing a unit ------------------
    for row, series, unit in ((21, cpf_price, cpf_unit), (22, cof_price, cof_unit)):
        bad = sum(1 for i, v in enumerate(series)
                  if _isnum(v) and not _nonblank(unit[i]))
        out[row] = (bad, "OK" if bad == 0 else "Fill Unit column")

    # --- rows 23-24: consumer-sheet rows with an unknown respondent --------
    cons_ids = {v for v in column(wb, "Form_C_Consumer", "rid") if _nonblank(v)}
    for row, series in ((23, cpf_rid), (24, cof_rid)):
        bad = sum(1 for v in series if _nonblank(v) and v not in cons_ids)
        out[row] = (bad, "OK" if bad == 0 else "Fix IDs")

    # --- rows 25-26: K/D flag usage (informational) ------------------------
    for row, series in ((25, po_buy), (26, po_sell)):
        n = sum(1 for v in series if str(v).strip() in ("K", "D"))
        out[row] = (n, "Info")

    # --- rows 27-28: pair linkage ------------------------------------------
    po_pair = column(wb, "Price_Observations", "pair")
    n_pairs = sum(1 for v in po_pair if _nonblank(v))
    trader_pairs = set()
    for sh in ("Form_A_Aratdar", "Form_B_Bepari_Faria", "Form_R_Khuchra"):
        trader_pairs |= {v for v in column(wb, sh, "pair") if _nonblank(v)}
    matched = sum(1 for v in po_pair if _nonblank(v) and v in trader_pairs)
    out[27] = (n_pairs, "Info")
    if n_pairs == 0:
        out[28] = (matched, "No pairs yet")
    else:
        out[28] = (matched, "All matched" if matched == n_pairs else "Some unmatched")

    # --- row 29: market observation forms ----------------------------------
    n_mkt = sum(1 for v in column(wb, "Form_M_Market_Observation", "date")
                if _nonblank(v))
    out[29] = (n_mkt, "COMPLETE" if n_mkt == 6 else "In progress")
    return out


def write_qc_values(path):
    """Write the computed QC values and statuses into the workbook.

    Replaces the formulas in ``QC_Check!C6:E29`` with their computed literals
    so that any reader (including Excel, which will show the same numbers)
    sees real values. Called after regenerating a dataset on a machine with
    no spreadsheet engine.
    """
    wb = openpyxl.load_workbook(path)
    computed = compute_qc(wb)
    ws = wb["QC_Check"]
    for row, (val, status) in computed.items():
        ws.cell(row=row, column=3).value = val
        ws.cell(row=row, column=5).value = status
    wb.save(path)
    return computed


def fill_derived_columns(path):
    """Write the derived (blue) columns as literals.

    ``Daily_capacity_kg`` on Forms A/B/R, ``Buy/Sell_BDT_per_kg`` and
    ``Quantity_kg`` on the price and consumer sheets. Formulas are replaced
    by their numeric results so the analysis scripts - and Excel - both read
    identical values without needing a recalculation pass.
    """
    wb = openpyxl.load_workbook(path)

    def set_val(sheet, header, r, value):
        ws = wb[sheet]
        ci = None
        for c in range(1, ws.max_column + 1):
            if ws.cell(row=4, column=c).value == header:
                ci = c
                break
        if ci:
            ws.cell(row=r, column=ci).value = value

    for sheet in ("Form_A_Aratdar", "Form_B_Bepari_Faria", "Form_R_Khuchra"):
        ws = wb[sheet]
        hdr = {}
        for c in range(1, ws.max_column + 1):
            h = ws.cell(row=4, column=c).value
            if h:
                hdr[h] = c
        for r in range(5, 41):
            raw = ws.cell(row=r, column=hdr.get("Daily_capacity_raw", 0)).value \
                if "Daily_capacity_raw" in hdr else None
            unit = ws.cell(row=r, column=hdr["Daily_capacity_unit"]).value \
                if "Daily_capacity_unit" in hdr else None
            if "Daily_capacity_kg" in hdr:
                if _isnum(raw):
                    ws.cell(row=r, column=hdr["Daily_capacity_kg"]).value = round(
                        raw * MAUND if str(unit) == "Maund" else raw, 2)
                else:
                    ws.cell(row=r, column=hdr["Daily_capacity_kg"]).value = None

    # Price_Observations
    ws = wb["Price_Observations"]
    hdr = {ws.cell(row=4, column=c).value: c
           for c in range(1, ws.max_column + 1) if ws.cell(row=4, column=c).value}
    for r in range(5, 505):
        unit = ws.cell(row=r, column=hdr["Unit"]).value
        for src, dst in (("Buy_price_raw", "Buy_BDT_per_kg"),
                         ("Sell_price_raw", "Sell_BDT_per_kg")):
            raw = ws.cell(row=r, column=hdr[src]).value
            ws.cell(row=r, column=hdr[dst]).value = (
                round(raw / MAUND if str(unit) == "Maund" else raw, 2)
                if _isnum(raw) else None)
        qraw = ws.cell(row=r, column=hdr["Quantity_raw"]).value
        qunit = ws.cell(row=r, column=hdr["Quantity_unit"]).value
        ws.cell(row=r, column=hdr["Quantity_kg"]).value = (
            round(qraw * MAUND if str(qunit) == "Maund" else qraw, 2)
            if _isnum(qraw) else None)

    # Consumer_Purchases_Focal
    ws = wb["Consumer_Purchases_Focal"]
    hdr = {ws.cell(row=4, column=c).value: c
           for c in range(1, ws.max_column + 1) if ws.cell(row=4, column=c).value}
    for r in range(5, 355):
        unit = ws.cell(row=r, column=hdr["Unit"]).value
        raw = ws.cell(row=r, column=hdr["Price_raw"]).value
        ws.cell(row=r, column=hdr["Price_BDT_per_kg"]).value = (
            round(raw / MAUND if str(unit) == "Maund" else raw, 2)
            if _isnum(raw) else None)
        qraw = ws.cell(row=r, column=hdr["Quantity_raw"]).value
        qunit = ws.cell(row=r, column=hdr["Quantity_unit"]).value
        ws.cell(row=r, column=hdr["Quantity_kg"]).value = (
            round(qraw * MAUND if str(qunit) == "Maund" else qraw, 2)
            if _isnum(qraw) else None)

    # Consumer_Other_Fish
    ws = wb["Consumer_Other_Fish"]
    hdr = {ws.cell(row=4, column=c).value: c
           for c in range(1, ws.max_column + 1) if ws.cell(row=4, column=c).value}
    for r in range(5, 105):
        unit = ws.cell(row=r, column=hdr["Unit"]).value
        for src, dst in (("Price_raw", "Price_BDT_per_kg"),):
            raw = ws.cell(row=r, column=hdr[src]).value
            ws.cell(row=r, column=hdr[dst]).value = (
                round(raw / MAUND if str(unit) == "Maund" else raw, 2)
                if _isnum(raw) else None)
        if "Quantity_raw" in hdr and "Quantity_kg" in hdr:
            qraw = ws.cell(row=r, column=hdr["Quantity_raw"]).value
            qunit = ws.cell(row=r, column=hdr["Quantity_unit"]).value
            ws.cell(row=r, column=hdr["Quantity_kg"]).value = (
                round(qraw * MAUND if str(qunit) == "Maund" else qraw, 2)
                if _isnum(qraw) else None)

    wb.save(path)


if __name__ == "__main__":
    import sys
    p = sys.argv[1] if len(sys.argv) > 1 else None
    if not p:
        print("usage: python scripts/qc_recalc.py <workbook.xlsx>")
        raise SystemExit(1)
    fill_derived_columns(p)
    vals = write_qc_values(p)
    bad = [r for r, (v, s) in vals.items()
           if s not in ("OK", "TARGET MET", "Info", "COMPLETE",
                        "All matched", "No pairs yet")]
    print(f"Recalculated {len(vals)} QC checks; non-passing: {len(bad)}")
