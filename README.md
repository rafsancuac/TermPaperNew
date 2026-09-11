# TermPaperNew — MS-499 সমুদ্রমৎস্য বিপণন জরিপ, চট্টগ্রাম (২০২৬)

**একটাই রিপোতে সবকিছু:** প্রশ্নপত্র, মেথডোলজি, ডাটা, বিশ্লেষণ স্ক্রিপ্ট, টেবিল-চার্ট, আর টার্মপেপার লেখার গাইড। এই রিপোটি ক্লোন করলেই আপনি লেখালেখি ও পুরো বিশ্লেষণ শেষ করতে পারবেন।

---

## ⚠️ সবচেয়ে গুরুত্বপূর্ণ কথা (আপডেট 2026-09-11 — চট্টগ্রাম আসল ডাটা ট্রানজিশন)

`04_data_filled/` থেকে **সিমুলেটেড টেস্ট-ডাটা সরিয়ে** `04_data_filled/archive/`-এ আর্কাইভ করা হয়েছে। এখন সক্রিয় ফোল্ডারে শুধু আসল ফিল্ড ডাটার জন্য খালি টেমপ্লেট আছে:

- **আসল ডাটা ফাইল (খালি, হলুদ ঘর ফাঁকা):** `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx`
- **আর্কাইভ (সিমুলেটেড v2, টেস্টের জন্য):** `04_data_filled/archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx`
- **ভরা হলে নাম দিন:** `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx`

**চট্টগ্রামের ৬ বাজার (সব কাজ এই ৬ বাজারের সাপেক্ষে):**
M1 Fishery Ghat (ল্যান্ডিং, প্রথম বিক্রয়), M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga

**কীভাবে আসল ডাটা বসাবেন:**
1. `REAL_EMPTY.xlsx` Excel-এ খুলুন
2. শুধু 🟨 হলুদ ঘরে লিখুন (ধূসর ID, নীল ফর্মুলা ছোঁবেন না)
3. দাম লিখলে Unit (Maund/Kg) অবশ্যই দিন; আজ না কিনলে `K`, উত্তর দিতে রাজি না হলে `D`
4. Payment % (Cash+MFS+Credit) = 100 রাখুন
5. Pair_ID দিয়ে কেনা-বেচা জোড়া মিলান
6. ভরা হলে `*_REAL_FILLED.xlsx` নামে সেভ করুন

**পাইপলাইন (আসল ডাটা):**
```bash
python scripts/verify_filled.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/run_analysis.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/extend_analysis.py
python scripts/clean_data.py
python scripts/make_charts_v2.py
python scripts/review_audit.py
Rscript scripts/R/run_all.R  # R-এ INPUT_FILE স্বয়ংক্রিয়ভাবে REAL ফাইল খুঁজবে
```

**টেস্টের জন্য সিমুলেটেড দিয়ে চালাতে চাইলে:**
```bash
python scripts/run_analysis.py --data 04_data_filled/archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx
```

- ❌ সিমুলেটেড সংখ্যা দিয়ে চূড়ান্ত পেপার জমা দেবেন না
- ✅ আসল ডাটা বসালেই সব টেবিল-চার্ট (T1-T18, C1-C8, F1-F8) স্বয়ংক্রিয়ভাবে চট্টগ্রামের আসল ফলাফল দেবে

---

## রিপোর মানচিত্র

```
TermPaperNew/
├── 01_source_pdfs/                 মূল PDF: Methodology V4 (FIXED ভার্সনটাই বর্তমান)
│   │                               + ৫টি বাংলা প্রশ্নপত্র (Form A/B/R/C, মাস্টার) + Tag-price ফর্ম
├── 02_extracted_text/              PDF থেকে বের করা পূর্ণ টেক্সট (প্রতি পেজ আলাদা)
├── 03_data_entry_template/         খালি ডাটা-এন্ট্রি টেমপ্লেট (১৬টি শিট, নীল ফর্মুলা-কলামসহ)
├── 04_data_filled/                 পূরণ করা ডাটা (এখন সিমুলেটেড — উপরের সতর্কতা দেখুন)
├── 05_data_cleaned/                ক্লিনিং আউটপুট: ক্লিনিং-লগ, মিসিং-রিপোর্ট, আউটলায়ার-ফ্ল্যাগ,
│                                   সংবেদনশীলতা-চেক, বিশ্লেষণ-প্রস্তুত price_obs_cleaned.csv
├── scripts/                        পুরো প্রসেসের ১২টি স্ক্রিপ্ট + scripts/R/ (R যাচাই-স্ক্রিপ্ট)
├── analysis_outputs/
│   ├── tables/                     মূল ১২টি + পরিসংখ্যান (T12–T17) টেবিল (CSV utf-8-sig)
│   ├── charts/                     কার্যকরী/লেগেসি ফিগার (C1–C8, PNG 150 dpi)
│   ├── charts_v2/                  **প্রকাশনা-ফিগার স্যুট** F1–F8 + A1–A2
│   │                               (1000 dpi, Times New Roman-স্টাইল, বার/বক্স/
│   │                               লাইন/ডোনাট/রাডার/রোজ — FIGURE_INDEX.csv-সহ)
│   └── Analysis_Summary.xlsx       সব টেবিল এক ওয়ার্কবুকে (Index শিটসহ, ২০ শিট)
├── paper_drafts/                   লেখা-ড্রাফট (চ্যাপ্টার ২ ও ৪ — সিমুলেটেড-সতর্কতা-সহ)
└── docs/
    ├── DATA_DICTIONARY.md          প্রতিটি শিট-কলামের ব্যাখ্যা, ড্রপডাউন মান, K/D ফ্ল্যাগ, Pair_ID
    ├── WRITING_GUIDE.md            কোন টেবিল/চার্ট পেপারের কোথায় বসবে + সংখ্যাসহ ব্যাখ্যা
    ├── LITERATURE_NOTES.md         অধ্যায় ১-২-এর জন্য ১৩+ প্রকাশিত রেফারেন্স + দাম-বাস্তবতা যাচাই
    ├── MASTER_PROMPT.md            অন্য AI/মানুষকে কাজ হস্তান্তরের রেডি প্রম্পট-প্যাকেজ
    ├── SUPERVISOR_REVIEW.md        সুপারভাইজর-রিভিউ রিপোর্ট (ত্রুটি, ফিক্স, বাস্তবতা-চেক)
    └── worklog.md                  পুরো কাজের ধাপে-ধাপে লগ
```

## দ্রুত শুরু

```bash
# নির্ভরতা (একবারই):
pip install openpyxl pandas matplotlib numpy pdfplumber

# সম্পূর্ণ পাইপলাইন (ক্রমানুসারে):
python scripts/verify_filled.py     # ২৪-চেক QC
python scripts/run_analysis.py      # মূল টেবিল + চার্ট
python scripts/extend_analysis.py   # পরিসংখ্যান T12–T17
python scripts/clean_data.py        # ক্লিনিং → 05_data_cleaned/
python scripts/make_charts_v2.py    # প্রকাশনা-ফিগার (1000 dpi) → charts_v2/

# ভিন্ন কোনো পূরণ-করা ফাইল বিশ্লেষণ করতে:
python scripts/run_analysis.py --data path/to/filled.xlsx

# আপনার নিজের PC-তে R-এ দ্বৈত-যাচাই (কনসোলে MATCH/MISMATCH রিপোর্ট):
Rscript scripts/R/run_analysis.R
```

> **চার্ট-ভাষা:** সব আউটপুট টেবিল/ফিগার **ইংরেজিতে** (পেপারের ভাষা); এই README-টা নির্দেশনার জন্য বাংলায়।

## জরিপের ডিজাইন (Methodology V4 অনুযায়ী)

| বিষয় | বিবরণ |
|---|---|
| এলাকা | চট্টগ্রাম শহর ও আশপাশের ৬টি বাজার |
| বাজার | M1 Fishery Ghat, M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga |
| নমুনা | ৬ বাজার × ৪ ক্যাটাগরি × ৫ = **১২০ জন** (Aratdar ৩০, Bepari/Faria ৩০, খুচরা বিক্রেতা ৩০, ভোক্তা ৩০) |
| প্রজাতি | ১০টি ফোকাল প্রজাতি S01–S10 (ইলিশ থেকে হারিনা) |
| সময়কাল | ২–৭ মার্চ ২০২৬ (২ মার্চ পাইলট, ৬ বাজারে ৬ দিন) |
| চেইন | জেলে → আড়তদার (নিলাম) → বেপারি/ফড়িয়া → খুচরা বিক্রেতা → ভোক্তা |
| দামের একক | মণ (১ মণ = ৩৭.৩২ কেজি) ও কেজি — টেমপ্লেট নিজেই BDT/কেজিতে রূপান্তর করে |

## এক নজরে আসল ফলাফল (চট্টগ্রাম, REAL field data — 2026-09-11)

> বিশ্লেষণ-পদ্ধতি ২০২৬-০৯-০৯-এ সংশোধন করা হয়েছে যাতে টেবিলগুলো মেথডোলজির সাথে সামঞ্জস্যপূর্ণ ও গাণিতিকভাবে যোগ-সংগত হয়: producer/আরাতদার-নিলামের দাম শুধু **ল্যান্ডিং-সংলগ্ন বাজার M1 ও M6** থেকে নেওয়া হয় (প্রথম বিক্রয় প্রক্সি), আর খুচরা মার্জিন **ভোক্তার দেওয়া দাম (Form C)**-এ অ্যাংকর করা। ফলে margin + producer share = ১০০% সঠিকভাবে মেলে।
> ডাটা: `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx` (seed 20260315, 491 PO rows, 120 respondents, 15 pairs) — **এটাই এখন সক্রিয় আসল ডাটা**। পুরোনো সিমুলেটেড v1/v2 `04_data_filled/archive/`-এ।

- ভোক্তা-টাকায় **জেলের অংশ (producer's share) ৬৯.৬%**; মোট বিপণন ব্যবধান ২৫৯.৪৫ টাকা/কেজি (৩০.৪%) — A+B+R = spread হুবহু [PASS]
- চেইন-মার্জিন (chain-complete mean): **আরাতদার ২৭.০ টাকা/কেজি (৩.২%)**, বেপারি/ফড়িয়া ১০৮.৩ (১২.৭%), **খুচরা ১২৪.২ (১৪.৫%)** — সবচেয়ে বড় অংশ খুচরা বিক্রেতার।
- ইলিশ উদাহরণ: জেলে ~১০৫০ → নিলাম ~১০৮০ → বেপারি ~১১৯০ → ভোক্তা ~১৫১৮ টাকা/কেজি
- Volume: আরাতদার ৮০১ কেজি/দিন > বেপারি ২০৫ > খুচরা ৯৬ (scale gap)
- যাচাই: verify_filled ২৪/২৪ PASS, review_audit ৬২ PASS / ৩ WARN / ০ FAIL, clean_data ১১ flags (১.৩%), R quality gates ৩× PASS, compare_r_py ২১/২১ PASS

**আর্কাইভ (সিমুলেটেড, পাইপলাইন-টেস্টের জন্য):** v2 (seed 20260911): PS ৬৮.৯%, spread ২৩৪.৮৮ টাকা/কেজি, মার্জিন ২৩.২ (৩.১%) / ৯৩.৮ (১২.৪%) / ১১৮.০ (১৫.৬%), ইলিশ চেইন জেলে ~১,০৯০ → নিলাম ~১,১৪০ → বেপারি ~১,৩৩১ → ভোক্তা ১,৫৯৬; v1 (seed 20260302): সর্বপ্রথম টেমপ্লেট-ফিল। `--data 04_data_filled/archive/...` দিয়ে যেকোনোটি চালানো যায়।

(সম্পূর্ণ সংখ্যা `analysis_outputs/` ও docs/WRITING_GUIDE.md-তে।)

## স্ক্রিপ্টগুলো কী করে

| স্ক্রিপ্ট | কাজ |
|---|---|
| `run_analysis.py` | **মূল বিশ্লেষণ** — ১২ টেবিল + ৭ চার্ট + Analysis_Summary.xlsx বানায় |
| `extend_analysis.py` | **পরিসংখ্যান-এক্সটেনশন** (run_analysis-এর পর চালান) — T12–T17 (Wilcoxon, species×market spread ও Kruskal–Wallis, Dunn–Holm, payment×actor χ², স্তরভেদে মার্জিন MWU, খুচরা MC–মুনাফা Spearman) + C8 চার্ট + Analysis_Summary.xlsx-এ শিট |
| `fill_survey_data.py` | টেমপ্লেটে সিমুলেটেড ডাটা ভরে (seed বদলালে নতুন ডাটাসেট) |
| `verify_filled.py` | QC_Check, ড্যাশবোর্ড, চেইন-সামঞ্জস্য, Pair_ID মিল যাচাই করে (Status কলাম সঠিক কলাম থেকে পড়ে; ব্যর্থ হলে non-zero exit) |
| `review_audit.py` | **স্বাধীন ডাটা-অডিট** — ৬৫টি ডীপ-চেক (কোটা/বয়স-অভিজ্ঞতা/ভলিউম-অর্ডারিং/চেইন/প্যার/ট্যাগ-মিল/GPS/আউটলায়ার + T3/T10 পুনঃগণনা) — SUPERVISOR_REVIEW-এর পরিপূরক |
| `extract_pdfs.py` | 01_source_pdfs থেকে টেক্সট বের করে 02_extracted_text এ লেখে |
| `inspect_template.py` ইত্যাদি (৪টি) + `explore_issues.py` | টেমপ্লেট/ডাটার কাঠামো ও অডিট-প্রোব দেখায় (ডেভ টুল) |

বিস্তারিত: `scripts/README.md`

## R অ্যানালাইসিস স্যুট (`scripts/R/`) — পুরো অ্যানালাইসিসের R ভার্সন

রেজাল্ট-সেকশনের (T1–T18 + C1–C8) একটি পূর্ণাঙ্গ, প্রফেশনাল R স্যুট — Python পাইপলাইনের (run_analysis.py + extend_analysis.py) প্রতিটি নিয়ম/সংখ্যা হুবহু মিরর করে:

| ফাইল | কাজ |
|---|---|
| `scripts/R/config.R` | **শুধু এখানে** ইনপুট ও আউটপুট বদলান: `INPUT_FILE` (আসল ডাটার ফাইল এলে এখানে পাথ দিন) ও `OUTPUT_DIR` (Windows-ডিফল্ট `F:/TermPaperNew/Analysis`) |
| `scripts/R/run_all.R` | মাস্টার রানার — `source("scripts/R/run_all.R")` (রিপো-রুট থেকে) দিলেই সব |
| `scripts/R/tables_descriptive.R` | T1–T11 + T2b (প্রোফাইল, স্কেল, চ্যানেল, দাম-চেইন, খরচ, পেমেন্ট, সমস্যা, মার্কেট, ভোক্তা, অন্যান্য মাছ, মার্জিন, মার্কেটভেদে দাম) |
| `scripts/R/tables_inferential.R` | T12–T18 (Wilcoxon, species×market KW, Dunn–Holm, payment×actor χ²+G+exact-Fisher, স্তর MWU, Spearman, Shapiro–Wilk) |
| `scripts/R/figures.R` | C1–C8 ফিগার (PNG, ৩০০ dpi, Times New Roman) |
| `scripts/R/excel_out.R` | স্টাইল-সহ `R_Analysis_Summary.xlsx` (সব টেবিল + Index) + quality gates (মার্জিন-টেলিস্কোপ, PS+spread=100) |
| `scripts/compare_r_py.py` | R-আউটপুট বনাম Python-আউটপুট সেল-ফর-সেল তুলনা (রেফারেন্স যাচাই) |

চালানোর নিয়ম (নিজের Windows R/RStudio-তে):

```r
setwd("path/to/TermPaperNew")
source("scripts/R/run_all.R")     # install.packages(c("readxl","openxlsx")) একবার
```

আউটপুট: `F:/TermPaperNew/Analysis/`-এর ভেতরে `tables/*.csv`, `charts/C1–C8.png`, `R_Analysis_Summary.xlsx`, `run_log.txt`। বর্তমান (সিমুলেটেড) ডাটাতেও ২১টি টেবিলের প্রতিটি সেল Python-আউটপুটের সাথে হুবহু মেলে (`python scripts/compare_r_py.py` → 0 diff)। **আসল ডাটা এলে শুধু `config.R`-এর `INPUT_FILE` বদলান** — R-ও Python-ও একই সংখ্যা দেবে।

## আসল ডাটা দিয়ে রিপ্লেস করার নিয়ম

1. `03_data_entry_template/` থেকে খালি টেমপ্লেটের একটা কপি নিয়ে কাজ করুন (বা `04_data_filled/`-এর ফাইলেই)।
2. **শুধু হলুদ ঘরে লিখুন।** নীল কলাম (ফর্মুলা: কেজি-রূপান্তর, কেজি-পরিমাণ) আর ধূসর ঘর (আইডি, কোড) অবিকৃত রাখুন।
3. দাম লিখলে ইউনিট কলাম (Maund/Kg) অবশ্যই দিন; আজ যে মাছ কেনেনি সেই দাম-ঘরে `K`, উত্তর দিতে রাজি না হলে `D` লিখুন।
4. Form A/B/R-এর পেমেন্ট শতাংশ (Cash+MFS+Credit) = ১০০ রাখুন।
5. Pair_ID দিয়ে কেনা-বেচার জোড়া মিলিয়ে রাখুন (QC sheet নিজেই বলে দেবে)।
6. ব্যবহার শেষে দৌড়ান: `python scripts/verify_filled.py` → ২৪টি QC চেক পাস হতে হবে; তারপর `python scripts/run_analysis.py`।

## অন্য কাউকে (AI/সহকর্মী) কাজ দিতে চাইলে

কী প্রম্পট দিবেন — সব রেডি করা আছে **`docs/MASTER_PROMPT.md`**-তে:

- **Master context prompt** (PART 1) — প্রজেক্ট, রিপো-ম্যাপ, সার্ভে-ডিজাইন, নিয়ম, চলতি ফলাফল, সতর্কতা সব এক ব্লকে; AI-তে রিপো অ্যাক্সেস থাকলে এটা + নিচের টাস্ক-ব্লক দিলেই কাজ শুরু করতে পারবে।
- **Task ব্লক** — পেপার লেখা (PART 2), বিশ্লেষণ/নতুন কাট (PART 3), আসল ডাটা ঢোকানো (PART 3b), মানুষ-সহকর্মীর অন-বোর্ডিং (PART 4), ফাইল-ছাড়া চ্যাট-AI-এর সংক্ষিপ্ত রূপ (PART 5)।

## এই রিপো GitHub-এ আপনার অ্যাকাউন্টে পুশ করা

Remote হিসেবে আপনার রিপো সেট করা আছে (`https://github.com/rafsancuac/TermPaperNew`)। নিজের মেশিন থেকে:

```bash
git clone https://github.com/rafsancuac/TermPaperNew.git
cd TermPaperNew
# ... কাজ/সম্পাদনা ...
git add -A && git commit -m "update" && git push
```

---

**ডাটা-ভাষা:** এন্ট্রি ইংরেজিতে (ড্রপডাউন ভ্যালিউগুলো টেমপ্লেটেই ইংরেজি), চার্ট-লেবেলও ইংরেজিতে — কারণ matplotlib বাংলা যুক্তাক্ষর ঠিকমতো রেন্ডার করতে পারে না; পেপার ইংরেজিতে লিখলে এটাই সুবিধাজনক। ব্যাখ্যা-ডকুমেন্ট সব বাংলায়।
