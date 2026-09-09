#!/usr/bin/env python3
"""compare_r_py.py — cell-level diff of R outputs vs the Python reference
outputs. Numbers must agree after rounding both sides to 2 decimals; text must
match exactly (after stripping). Run:  python3 scripts/compare_r_py.py
"""
import os, sys
import pandas as pd
import numpy as np

PY = os.path.join("analysis_outputs", "tables")
RX = os.path.join("analysis_outputs_r", "tables")


def norm(x):
    if pd.isna(x):
        return None
    if isinstance(x, str):
        s = x.strip()
        return s if s != "" else None
    return x


def same_cell(a, b):
    a, b = norm(a), norm(b)
    if a is None or b is None:
        return a is None and b is None
    # numeric check
    for v in (a, b):
        if isinstance(v, str):
            break
    else:
        return abs(float(a) - float(b)) < 1e-6
    try:
        fa, fb = float(str(a).replace(",", "")), float(str(b).replace(",", ""))
        return abs(fa - fb) < 0.011
    except ValueError:
        pass
    # text compare (case & space exact)
    sa = str(a).strip() if not isinstance(a, str) else a.strip()
    sb = str(b).strip() if not isinstance(b, str) else b.strip()
    return sa == sb


def main():
    files = sorted(f for f in os.listdir(PY) if f.endswith(".csv"))
    nfail_tot, nwarn_tot = 0, 0
    for f in files:
        p = os.path.join(PY, f)
        r = os.path.join(RX, f)
        if not os.path.exists(r):
            print(f"[MISSING] R output {f}"); nfail_tot += 1; continue
        a = pd.read_csv(p)
        b = pd.read_csv(r)
        # column union order = python order then r extras
        cols = list(a.columns) + [c for c in b.columns if c not in a.columns]
        if list(a.columns) != list(b.columns):
            print(f"[COLS] {f}: py={list(a.columns)} vs r={list(b.columns)}")
            nfail_tot += 1
        if len(a) != len(b):
            print(f"[ROWS] {f}: py={len(a)} vs r={len(b)}"); nfail_tot += 1
        nmis, shown = 0, 0
        for i in range(max(len(a), len(b))):
            for c in cols:
                if i < len(a) and c in a.columns:
                    av = a.at[i, c]
                else:
                    av = np.nan
                if i < len(b) and c in b.columns:
                    bv = b.at[i, c]
                else:
                    bv = np.nan
                if not same_cell(av, bv):
                    nmis += 1
                    if shown < 5:
                        print(f"  [DIFF] {f} row{i} col '{c}': py={av!r} r={bv!r}")
                        shown += 1
        if nmis:
            print(f"[FAIL] {f}: {nmis} cell diffs")
            nfail_tot += 1
        else:
            print(f"[PASS] {f} ({len(a)}x{len(cols)})")
    print(f"\n==> files with diffs: {nfail_tot}")
    sys.exit(1 if nfail_tot else 0)


if __name__ == "__main__":
    main()
