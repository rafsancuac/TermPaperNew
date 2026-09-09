#!/usr/bin/env python3
"""Dump data validation lists + key formulas from the workbook."""
import openpyxl

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PATH = os.path.join(ROOT, "03_data_entry_template", "Marine_Fish_Marketing_Data_Entry (1).xlsx")
wb = openpyxl.load_workbook(PATH)

print("=== DATA VALIDATIONS per sheet ===")
for ws in wb.worksheets:
    dvs = ws.data_validations.dataValidation
    if dvs:
        print(f"\n--- {ws.title} ---")
        for dv in dvs:
            print(f"  cells={str(dv.sqref)[:60]:60s} type={dv.type} formula1={str(dv.formula1)[:120]}")

print("\n\n=== KEY FORMULAS (row 5 of each form sheet = first data row) ===")
for name in ["Form_A_Aratdar", "Form_B_Bepari_Faria", "Form_R_Khuchra", "Form_C_Consumer",
             "Price_Observations", "Consumer_Purchases_Focal", "Consumer_Other_Fish",
             "Tag_Price_Sheet"]:
    ws = wb[name]
    print(f"\n--- {name} ---")
    # header row 4
    hdr = [c.value for c in ws[4]]
    for col_idx, h in enumerate(hdr, 1):
        if h is None:
            continue
        cell = ws.cell(row=5, column=col_idx)
        if cell.value is not None and isinstance(cell.value, str) and cell.value.startswith("="):
            print(f"  col{col_idx:2d} {str(h)[:38]:38s} -> {cell.value[:110]}")

print("\n=== QC_Check (full, formulas) ===")
ws = wb["QC_Check"]
for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=31, values_only=True), 1):
    cells = [str(c) if c is not None else "" for c in row]
    if any(cells):
        print(f"R{row_idx}: " + " | ".join(cells))

print("\n=== Form_M_Market_Observation header + col widths (rows 1-6) ===")
ws = wb["Form_M_Market_Observation"]
for row_idx, row in enumerate(ws.iter_rows(min_row=1, max_row=6, values_only=True), 1):
    cells = [str(c) if c is not None else "" for c in row]
    if any(cells):
        print(f"R{row_idx}: " + " | ".join(cells))

print("\n=== Cell fill colors (yellow/blue/grey map) - Form_A row 4-5 ===")
ws = wb["Form_A_Aratdar"]
for col_idx in range(1, 34):
    c_hdr = ws.cell(row=4, column=col_idx)
    c_data = ws.cell(row=5, column=col_idx)
    fill = c_data.fill
    rgb = None
    if fill and fill.fgColor and fill.fgColor.rgb and fill.patternType:
        rgb = str(fill.fgColor.rgb)
    print(f"col{col_idx:2d} {str(c_hdr.value)[:36]:36s} fill={rgb}")
