#!/usr/bin/env python3
"""Extract text from all PDF questionnaires."""
import os

try:
    import pdfplumber
    ENGINE = "pdfplumber"
except ImportError:
    try:
        from pypdf import PdfReader
        ENGINE = "pypdf"
    except ImportError:
        ENGINE = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD = os.path.join(ROOT, "01_source_pdfs")
pdfs = [f for f in os.listdir(UPLOAD) if f.endswith(".pdf")]

print(f"Engine: {ENGINE}\n")

def extract_pdfplumber(path):
    import pdfplumber
    out = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            txt = page.extract_text() or ""
            out.append(f"--- PAGE {i+1} ---\n{txt}")
    return "\n".join(out)

def extract_pypdf(path):
    from pypdf import PdfReader
    reader = PdfReader(path)
    out = []
    for i, page in enumerate(reader.pages):
        txt = page.extract_text() or ""
        out.append(f"--- PAGE {i+1} ---\n{txt}")
    return "\n".join(out)

for f in sorted(pdfs):
    path = os.path.join(UPLOAD, f)
    print("=" * 80)
    print(f"FILE: {f}")
    print("=" * 80)
    try:
        if ENGINE == "pdfplumber":
            text = extract_pdfplumber(path)
        else:
            text = extract_pypdf(path)
        # write full text to a .txt file for later reference
        txt_path = os.path.join(ROOT, "02_extracted_text", f.replace(".pdf", ".txt"))
        os.makedirs(os.path.dirname(txt_path), exist_ok=True)
        with open(txt_path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"[saved to {txt_path}, {len(text)} chars]")
    except Exception as e:
        print(f"ERROR: {e}")
    print()
