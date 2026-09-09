# MASTER_PROMPT — অন্য কাউকে কাজ/বিশ্লেষণ/লেখালেখি হস্তান্তরের প্রম্পট-প্যাকেজ

কেউ (AI বা মানুষ) এই প্রজেক্টে ঢুকে আগের প্রসেস না জেনেই কাজ চালিয়ে যাক — সেজন্যই এই ফাইল।

## কোন পরিস্থিতিতে কোনটা ব্যবহার করবেন

| যাকে কাজ দিচ্ছেন | কী দিবেন |
|---|---|
| AI-তে রিপো/ফাইল অ্যাক্সেস (Claude Code, Cursor, terminal agent) | **PART 1** + নিচের মধ্যে প্রযোজ্য **TASK ব্লক** |
| শুধু চ্যাট-AI (ChatGPT/Gemini — ফাইল আপলোড যায় বা পেস্ট করা যায়) | **PART 1** + TASK ব্লক + প্রাসঙ্গিক CSV-এর কনটেন্ট পেস্ট |
| প্রম্পট ছোট রাখতে চান / চ্যাটে জায়গা কম | **PART 5** (সংক্ষিপ্ত রূপ) |
| মানুষ-সহকারী | **PART 4** (বাংলা অন-বোর্ডিং) |

> প্রম্পটের ভাষা ইংরেজি রাখা হয়েছে — AI টুলে ইংরেজি প্রম্পট সবচেয়ে নির্ভরযোগ্য, আর পেপারও ইংরেজিতে লিখতে হবে। বাংলা ব্যাখ্যা দরকার হলে প্রম্পটের শেষে এক লাইন যোগ করুন: "Reply in Bengali."

---

## PART 1 — MASTER CONTEXT PROMPT (সবসময় আগে এটা দিন)

নিচের ব্লকটা হুবহু কপি-পেস্ট করুন:

```text
ROLE
You are the research assistant for a university term paper (course MS-499).
Work from the repository contents; treat docs/ and 01_source_pdfs/ as the
ground truth for survey design. Do not invent survey facts that contradict
them. If something is missing, say so explicitly.

PROJECT (one line)
"Marine Fish Marketing System of Chattogram, Bangladesh" — structured survey
of 6 markets and 4 value-chain actor categories; field period 2–7 March 2026
(2 March = pilot day at Fishery Ghat).

REPOSITORY MAP (TermPaperNew)
01_source_pdfs/    8 original PDFs: "Methodology_v4_FIXED (references
                   updated)" (CURRENT version — use this, not plain V4);
                   5 Bengali questionnaires — Form A Aratdar, Form B
                   Bepari/Faria, Form R khuchra/retail, Form C consumer,
                   plus a master questionnaire; and a Tag-price sheet.
02_extracted_text/ Full plain-text extraction of each PDF, page by page.
                   (Bengali glyph order may be jumbled — cross-check with
                   the Excel column names.)
03_data_entry_template/  Blank 16-sheet data-entry workbook.
04_data_filled/    FILLED workbook — ⚠ SIMULATED data, see warning below.
scripts/           run_analysis.py (main pipeline: 12 tables + 7 charts +
                   Analysis_Summary.xlsx), extend_analysis.py (statistical
                   extension: T12–T17 + C8; run AFTER run_analysis.py),
                   verify_filled.py (24 QC checks), review_audit.py (64
                   independent data-audit checks), fill_survey_data.py
                   (regenerate simulated data, seed=20260302),
                   extract_pdfs.py, inspect_*.py, explore_issues.py.
analysis_outputs/  tables/ (T1–T11, T2b, T12–T17; CSV utf-8-sig),
                   charts/ (C1–C8, PNG 150 dpi), Analysis_Summary.xlsx
                   (all tables + Index).
paper_drafts/      chapter 2 (literature review skeleton) and chapter 4
                   (results & discussion) drafts with [SIMULATED] notes.
docs/              DATA_DICTIONARY.md (every sheet & column explained),
                   WRITING_GUIDE.md (chapter→table map + current numbers),
                   LITERATURE_NOTES.md (13+ published references for
                   Chapters 1-2 + price-realism verification),
                   SUPERVISOR_REVIEW.md (supervisor-level audit: found &
                   fixed pipeline bugs, new methodology-consistent chain
                   convention — read before extending the analysis),
                   worklog.md (full process log), MASTER_PROMPT.md (this).

SURVEY DESIGN (Methodology V4)
- Area: Chattogram city & periphery. Markets: M1 Fishery Ghat
  (landing/wholesale), M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli
  Complex, M5 Bahaddarhat, M6 Patenga (near landing).
- Sample: 6 markets × 4 categories × 5 = 120 respondents — 30 Aratdar
  (Form A), 30 Bepari/Faria (Form B: 20 Bepari + 10 Faria), 30 retailers
  (Form R), 30 consumers (Form C).
- 10 focal species S01–S10: Ilish, Rupchanda, Lakkha, Koral, Surma, Churi,
  Poa, Kankoita, Loitta, Harina.
- Value chain: fisher → Aratdar (auction, commission) → Bepari/Faria →
  retailer → consumer.
- Field dates: 2 Mar pilot (M1); 3 Mar M1+M6; 4 Mar M2; 5 Mar M3;
  6 Mar M4; 7 Mar M5.
- Price units: Maund (1 maund = 37.32 kg) and Kg; the template
  auto-converts to BDT/kg.

DATA-ENTRY RULES (immutable)
- Only YELLOW cells are for entry. BLUE columns are formulas (kg
  conversion, per-kg amounts) — never overwrite. GRAY prefilled IDs/codes
  stay as-is.
- Price flags: "K" = not operating today (no price), "D" = declined.
  Flagged prices are excluded from means (n drops — report reduced n).
- Form A/B/R payment shares: Cash + MFS + Credit = 100% per respondent.
- Pair_ID links one buyer's row with one seller's row for the same
  transaction (enables paired tests and margin attribution).
- ID patterns: Respondent_ID = M{1-6}-{A|B|R|C}-{01..05}; price
  observations PO-0001…; species S01–S10.
- The workbook's QC sheet runs 24 checks; verify_filled.py reports them
  (currently 24/24 PASS, TARGET MET = 120 respondents).

⚠ DATA WARNING — READ FIRST
04_data_filled/ contains SIMULATED (script-generated, seed 20260302)
data, built to mimic realistic 2026 Chattogram price levels and to pass
every template validation/QC rule. Purpose: build & test the analysis
pipeline and paper structure BEFORE real field data arrives. NEVER
submit these numbers as final field results. When real data arrives:
enter it in yellow cells only, run verify_filled.py (must pass 24/24),
then run_analysis.py to regenerate every table and chart.

CURRENT STATUS & HEADLINE (SIMULATED) RESULTS
- 120 respondents; 463 price observations; 16 matched buy/sell pairs
  (14 usable); 6 market-observation rows; 7 collection-log visits.
- Producer's (fisher's) share of consumer price: 70.9% (producer price =
  Form A buy quotes at landing-linked markets M1/M6 only; Methodology 3.11c).
- Channel margins (chain-complete species S01–S09, % of consumer taka):
  Aratdar ≈ 25.8 BDT/kg (3.3%), Bepari/Faria ≈ 92.7 (11.7%),
  Retailer (consumer-anchored) ≈ 111.4 (14.1%); total spread 229.9 (29.1%);
  margins + share = exactly 100%.
- Ilish chain example: fisher ≈1,032 → auction ≈1,083 → bepari ≈1,236 →
  consumer ≈1,420 BDT/kg.
- Retailer vendor quotes average ≈2.5% ABOVE consumer-paid prices (bargaining
  gap) — margins use the consumer-paid anchor; quote series are descriptive.
- MFS payment share rises down-chain (Aratdar ~14% → retail ~29%);
  consumers pay ~57% by MFS (bKash 37%, Nagad 20%).
- Top problems: unsold-fish spoilage 31%, supply syndicate 31%,
  frozen-import competition 29%, ice cost 27%.
- Statistics (Methodology 3.8): Wilcoxon on matched pairs p=0.116
  (consistent); Kruskal–Wallis across markets exploratory (cells n≥3):
  significant for S01–S03, S05, S06 (S01 Fishery Ghat vs Bahaddarhat
  survives Dunn–Holm); payment mode × actor χ² p=0.87; stratum margins
  differ (MWU p<0.0001); retailer MC/kg vs net margin Spearman rho=0.43,
  p=0.018.
(Full numbers live in analysis_outputs/ and docs/WRITING_GUIDE.md.)

REPRODUCING / RE-RUNNING
pip install openpyxl pandas matplotlib numpy scipy pdfplumber
python scripts/run_analysis.py                    # tables/charts (T1–T11)
python scripts/extend_analysis.py                 # statistics (T12–T17, C8)
python scripts/run_analysis.py --data OTHER.xlsx  # from another workbook
python scripts/verify_filled.py                   # 24 QC checks
python scripts/fill_survey_data.py                # regenerate simulated

METHOD NOTES (for analysis & writing)
- Margin = next-level price − previous-level price, per kg; species-level
  means, then composition-consistent aggregate over CHAIN-COMPLETE species
  (state this in the Methodology chapter; S10 Harina currently excluded —
  no landing-market auction sell quote).
- Producer price (fisher first-sale) is proxied ONLY from Form A buy quotes
  at landing-linked markets M1 Fishery Ghat & M6 Patenga; retail price P_r
  is the consumer-paid anchor (Form C slips) and the retailer margin is
  P_r − Bepari sell. Under this convention margins telescope to the total
  spread and PS% + spread% = 100 exactly.
- Producer's share = fisher price ÷ consumer price × 100.
- Maund prices converted at 37.32 kg before any averaging.
- K/D-flagged price cells are excluded from means.
- Statistical tests: distribution-free only; within-species across markets
  (never pooled across species); cells n≥5 pre-specified, n≥3 exploratory;
  Holm adjustment after significant omnibus tests.
```

---

## PART 2 — TASK ব্লক: পেপার লেখা (PART 1-এর পরে যোগ করুন)

```text
TASK — WRITE THE TERM PAPER
Write the term paper in formal academic English following the 5-chapter
structure in docs/WRITING_GUIDE.md. Start with the chapter(s) I name in
my next message.
Rules:
1. Use ONLY numbers from analysis_outputs/tables/*.csv (or the numbers
   quoted above). Never invent a number. If a figure is missing, write
   [MISSING] and continue.
2. Under every table: "Source: Field survey, March 2026" and the n.
3. Chapter 3 (Methodology) must mirror Methodology_v4_FIXED (see
   02_extracted_text/) — markets, 120-sample design, species, dates,
   maund→kg conversion, K/D flags, margin & producer's-share formulas.
4. Chapter 4: follow the mapping in WRITING_GUIDE.md (T1→4.1, T2/T2b→4.2,
   T3/T10+C1/C2→4.3, T11+C6→4.4, T4→4.5, T5+C3→4.6, T6+C5→4.7, T7→4.8,
   T8/T9→4.9). Figures C1–C7 are inserted as "Figure 4.x" with captions.
5. Remind me (in a comment / footnote, not in body text) that current
   numbers come from SIMULATED data and must be re-pulled after real
   data entry.
6. Length: ~1,000–1,500 words per chapter; Results chapter may be longer.
```

## PART 3 — TASK ব্লক: বিশ্লেষণ / নতুন কাট (PART 1-এর পরে যোগ করুন)

```text
TASK — ANALYSIS
Run and/or extend the analysis on 04_data_filled (or a workbook I give
with --data). Baseline outputs: T1–T11 + T2b and charts C1–C7 from
scripts/run_analysis.py — read that script before extending.
Aligned extensions, in priority order:
1. Wilcoxon signed-rank test on Pair_ID matched buy/sell prices
   (16 pairs) — price spread significance.
2. Price-spread decomposition by species × market (extend T11/C6).
3. Cross-tab: payment method × actor type, with chi-square.
4. Form M infrastructure scores vs retail price level by market.
Constraints:
- Respect K/D flags, maund→kg (37.32), composition-consistent
  aggregation; charts stay English-labeled, 150 dpi.
- Write new outputs to analysis_outputs/ following existing naming
  (T12, T13… / C8, C9…) and add rows to Analysis_Summary.xlsx Index.
- Do not modify 04_data_filled or the template; results are derived.
```

## PART 3b — TASK ব্লক: আসল ডাটা ঢোকানো (যখন ফিল্ড ডাটা আসবে)

```text
TASK — REAL DATA REPLACEMENT
Real field data has arrived. Take a fresh copy of 03_data_entry_template/,
enter the real data in YELLOW cells only (blue formula and gray ID columns
untouched; K/D flags where applicable; payment % = 100; Pair_IDs kept
consistent). Then:
  python scripts/verify_filled.py --data <file>   (must pass 24/24)
  python scripts/run_analysis.py --data <file>
Regenerate every number in the drafted chapters from the new tables.
Delete all simulated-data warnings from the final text at that point.
```

---

## PART 4 — মানুষ-সহকর্মীর জন্য (বাংলা)

১. শুরুতে `README.md` পড়ুন — রিপোর মানচিত্র ও সতর্কতা ওখানেই।
২. ডাটা বুঝতে `docs/DATA_DICTIONARY.md` (১৬ শিটের প্রতিটি কলাম, K/D ফ্ল্যাগ, Pair_ID)।
৩. লেখালেখির জন্য `docs/WRITING_GUIDE.md` — কোন টেবিল/চার্ট কোন অধ্যায়ে, সংখ্যাসহ।
৪. নিজে বিশ্লেষণ চালাতে: `pip install openpyxl pandas matplotlib numpy pdfplumber` → `python scripts/run_analysis.py`।
৫. **মনে রাখুন:** `04_data_filled`-এর ডাটা এখন সিমুলেটেড — চূড়ান্ত জমায় দেওয়ার আগে আসল ডাটা ঢোকান।

## PART 5 — সংক্ষিপ্ত চ্যাট-প্রম্পট (ফাইল অ্যাক্সেস ছাড়া AI-কে)

```text
I am writing an MS-499 term paper: "Marine Fish Marketing System of
Chattogram, Bangladesh" — survey of 6 markets (Fishery Ghat, Chawkbazar,
Kazir Dewri, Karnaphuli Complex, Bahaddarhat, Patenga), 120 respondents
(30 Aratdar, 30 Bepari/Faria, 30 retailers, 30 consumers), 10 focal
species, 2–7 March 2026. Chain: fisher → Aratdar (auction) → Bepari →
retailer → consumer; 1 maund = 37.32 kg; producer's share = fisher price
÷ consumer price. Current dataset (SIMULATED, for drafting only) gives:
producer's share 73.9%, retailer margin 122 BDT/kg (16.7%), Bepari 63
(8.5%), Aratdar 25 (3.4%); MFS use rises down-chain; top problems
syndicate 31%, spoilage 31%, import competition 29%. TASK: <এখানে কাজ লিখুন —
e.g., "draft Chapter 4.3 (price chain & margins) from the numbers above">.
I will paste the exact tables next. [Then paste the relevant CSV contents.]
```

---

**অনুশংসা:** যাকে কাজ দিন, শেষে এই লাইনটাও দিন — *"Before finishing, read docs/worklog.md and append what you did; keep outputs inside the repo."* এতে কাজের ধারাবাহিকতা বজায় থাকবে।
