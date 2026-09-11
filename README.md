# TermPaperNew — MS-499 সমুদ্রমৎস্য বিপণন জরিপ, চট্টগ্রাম (২০২৬)

**একটাই রিপোতে সবকিছু:** প্রশ্নপত্র, মেথডোলজি, ডাটা, বিশ্লেষণ স্ক্রিপ্ট, টেবিল-চার্ট, আর টার্মপেপার লেখার গাইড। এই রিপোটি ক্লোন করলেই আপনি লেখালেখি ও পুরো বিশ্লেষণ শেষ করতে পারবেন।

---

## ⚠️ সবচেয়ে গুরুত্বপূর্ণ কথা (আপডেট 2026-09-11 — ডাটা প্রোভেন্যান্স)

`04_data_filled/`-এ সক্রিয় ডাটাসেটটি **সিন্থেটিক**:

- **সক্রিয় (সিন্থেটিক):** `04_data_filled/SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx` — `scripts/generate_synthetic_data.py` (seed 20260315) থেকে তৈরি; ৬ বাজার, ১২০ উত্তরদাতা, ৪৯১ PO rows, ১৫ জোড়া
- **খালি টেমপ্লেট (আসল জরিপের জন্য):** `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx`

**এটি আসল ফিল্ড ডাটা নয়।** পেপারের কোথাও এই ডাটাকে পর্যবেক্ষিত ফিল্ড ডাটা হিসেবে উপস্থাপন করা যাবে না — তা গবেষণায় প্রতারণা হবে এবং সহজেই ধরা পড়বে। ডিজাইন, প্রশ্নপত্র, QC গেট, অডিট ও রিপোর্টিং টেমপ্লেট যাচাই করাই এর কাজ।

**চট্টগ্রামের ৬ বাজার (সব কাজ এই ৬ বাজারের সাপেক্ষে):**
M1 Fishery Ghat (ল্যান্ডিং, প্রথম বিক্রয়), M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga

**আসল ডাটা বসানোর নিয়ম:**
1. `REAL_EMPTY.xlsx` Excel-এ খুলুন
2. শুধু 🟨 হলুদ ঘরে লিখুন (ধূসর ID, নীল ফর্মুলা ছোঁবেন না)
3. দাম লিখলে Unit (Maund/Kg) অবশ্যই দিন; আজ না কিনলে `K`, উত্তর দিতে রাজি না হলে `D`
4. Payment % (Cash+MFS+Credit) = 100 রাখুন
5. Pair_ID দিয়ে কেনা-বেচা জোড়া মিলান
6. ভরা হলে `*_REAL_FILLED.xlsx` নামে `04_data_filled/`-এ সেভ করুন

**পাইপলাইন:**
```bash
python scripts/verify_filled.py            # ২৪-চেক QC গেট
python scripts/run_analysis.py             # বর্ণনামূলক T1–T11, T2b, T4b, T19
python scripts/extend_analysis.py          # পরিসংখ্যান T12–T18
python scripts/clean_data.py               # ক্লিনিং → 05_data_cleaned/
python scripts/make_charts_v2.py           # প্রকাশনা-ফিগার (1000 dpi) → charts_v2/
python scripts/review_audit.py             # ৬৫-চেক স্বাধীন অডিট
Rscript scripts/R/MS499_full_analysis.R    # আপনার নিজের Local R-এ দ্বৈত-যাচাই
```

- ❌ সিন্থেটিক সংখ্যা দিয়ে চূড়ান্ত পেপার জমা দেবেন না
- ✅ আসল ডাটা বসালেই সব টেবিল-চার্ট (T1–T19, F1–F8) স্বয়ংক্রিয়ভাবে চট্টগ্রামের আসল ফলাফল দেবে

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
├── paper_drafts/                   লেখা-ড্রাফট (৫টি অধ্যায় — সিন্থেটিক-প্রোভেন্যান্স সতর্কতাসহ)
└── docs/
    ├── DATA_DICTIONARY.md          প্রতিটি শিট-কলামের ব্যাখ্যা, ড্রপডাউন মান, K/D ফ্ল্যাগ, Pair_ID
    ├── WRITING_GUIDE.md            কোন টেবিল/চার্ট পেপারের কোথায় বসবে + সংখ্যাসহ ব্যাখ্যা
    ├── LITERATURE_NOTES.md         অধ্যায় ১-২-এর জন্য ১৩+ প্রকাশিত রেফারেন্স + দাম-বাস্তবতা যাচাই
    └── LITERATURE_NOTES.md         (উপরে দেখুন)
```

## দ্রুত শুরু

```bash
# নির্ভরতা (একবারই):
pip install openpyxl pandas matplotlib numpy pdfplumber

# সম্পূর্ণ পাইপলাইন (ক্রমানুসারে):
python scripts/verify_filled.py     # ২৪-চেক QC
python scripts/run_analysis.py      # মূল টেবিল + চার্ট
python scripts/extend_analysis.py   # পরিসংখ্যান T12–T18
python scripts/clean_data.py        # ক্লিনিং → 05_data_cleaned/
python scripts/make_charts_v2.py    # প্রকাশনা-ফিগার (1000 dpi) → charts_v2/

# ভিন্ন কোনো পূরণ-করা ফাইল বিশ্লেষণ করতে:
python scripts/run_analysis.py --data path/to/filled.xlsx

# আপনার নিজের Local R-এ দ্বৈত-যাচাই (স্বয়ংসম্পূর্ণ, T1–T19 + ফিগার):
Rscript scripts/R/MS499_full_analysis.R
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

## এক নজরে ফলাফল (চট্টগ্রাম — সিন্থেটিক ডাটাসেট, 2026-09-11)

> বিশ্লেষণ-পদ্ধতি ২০২৬-০৯-০৯-এ সংশোধন করা হয়েছে যাতে টেবিলগুলো মেথডোলজির সাথে সামঞ্জস্যপূর্ণ ও গাণিতিকভাবে যোগ-সংগত হয়: producer/আরাতদার-নিলামের দাম শুধু **ল্যান্ডিং-সংলগ্ন বাজার M1 ও M6** থেকে নেওয়া হয় (প্রথম বিক্রয় প্রক্সি), আর খুচরা মার্জিন **ভোক্তার দেওয়া দাম (Form C)**-এ অ্যাংকর করা। ফলে margin + producer share = ১০০% সঠিকভাবে মেলে।
> ডাটা: `04_data_filled/SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx` (**সিন্থেটিক**, seed 20260315, 491 PO rows, 120 respondents, 15 pairs)। আসল ডাটা নয় — প্রোভেন্যান্স দেখুন `04_data_filled/README_SYNTHETIC.md`।

- ভোক্তা-টাকায় **জেলের অংশ (producer's share) ৭২.৪%**; মোট বিপণন ব্যবধান ২৫১.৩৫ টাকা/কেজি (২৭.৬%) — A+B+R = spread হুবহু [PASS]
- চেইন-মার্জিন (chain-complete mean): **আরাতদার ২৯.৯৪ টাকা/কেজি (৩.৩%)**, বেপারি/ফড়িয়া ১০৪.৮৭ (১১.৫%), **খুচরা ১১৬.৫৪ (১২.৮%)** — সবচেয়ে বড় অংশ খুচরা বিক্রেতার।
- ইলিশ উদাহরণ: জেলে ১,০৪৫.০২ → নিলাম ১,০৯৩.৪০ → বেপারি ১,২৫৭.৫৫ → ভোক্তা ১,৪৫৬.৫০ টাকা/কেজি
- Volume: আরাতদার ৮০১ কেজি/দিন > বেপারি ২০৫ > খুচরা ৯৬ (scale gap)
- যাচাই: verify_filled ২৪/২৪ PASS, review_audit ৬০ PASS / ৫ WARN / ০ FAIL, clean_data ১০ flags (১.০%), R quality gates ৩× PASS, compare_r_py ২২/২৩ PASS

**আর্কাইভ (সিমুলেটেড, পাইপলাইন-টেস্টের জন্য):** v2 (seed 20260911): PS ৬৮.৯%, spread ২৩৪.৮৮ টাকা/কেজি, মার্জিন ২৩.২ (৩.১%) / ৯৩.৮ (১২.৪%) / ১১৮.০ (১৫.৬%), ইলিশ চেইন জেলে ~১,০৯০ → নিলাম ~১,১৪০ → বেপারি ~১,৩৩১ → ভোক্তা ১,৫৯৬; v1 (seed 20260302): সর্বপ্রথম টেমপ্লেট-ফিল। `--data 04_data_filled/archive/...` দিয়ে যেকোনোটি চালানো যায়।

(সম্পূর্ণ সংখ্যা `analysis_outputs/` ও docs/WRITING_GUIDE.md-তে।)

## স্ক্রিপ্টগুলো কী করে

| স্ক্রিপ্ট | কাজ |
|---|---|
| `run_analysis.py` | **মূল বিশ্লেষণ** — ১২ টেবিল + ৭ চার্ট + Analysis_Summary.xlsx বানায় |
| `extend_analysis.py` | **পরিসংখ্যান-এক্সটেনশন** (run_analysis-এর পর চালান) — T12–T17 (Wilcoxon, species×market spread ও Kruskal–Wallis, Dunn–Holm, payment×actor χ², স্তরভেদে মার্জিন MWU, খুচরা MC–মুনাফা Spearman) + C8 চার্ট + Analysis_Summary.xlsx-এ শিট |
| `generate_synthetic_data.py` | সিন্থেটিক ডাটাসেট তৈরি (seed বদলালে নতুন ডাটাসেট) |
| `qc_recalc.py` | ডেরাইভড (নীল) কলাম + ২৪ QC চেক Python-এ পুনর্গণনা করে **লিটারেল ভ্যালু** হিসেবে লেখে — যাতে স্প্রেডশিট-ইঞ্জিন ছাড়াই Excel/pandas/R-এ একই ফল পড়া যায় |
| `verify_filled.py` | QC_Check, ড্যাশবোর্ড, চেইন-সামঞ্জস্য, Pair_ID মিল যাচাই করে (Status কলাম সঠিক কলাম থেকে পড়ে; ব্যর্থ হলে non-zero exit) |
| `review_audit.py` | **স্বাধীন ডাটা-অডিট** — ৬৫টি ডীপ-চেক (কোটা/বয়স-অভিজ্ঞতা/ভলিউম-অর্ডারিং/চেইন/প্যার/ট্যাগ-মিল/GPS/আউটলায়ার + T3/T10 পুনঃগণনা) — বর্তমানে ৬০ PASS / ৫ WARN / ০ FAIL |
| `extract_pdfs.py` | 01_source_pdfs থেকে টেক্সট বের করে 02_extracted_text এ লেখে |

বিস্তারিত: `scripts/README.md`

## R অ্যানালাইসিস স্ক্রিপ্ট (`scripts/R/`) — আপনার Local R/RStudio-এ

**একটিই স্ক্রিপ্ট: `scripts/R/MS499_full_analysis.R`** — সব টেবিল (T1–T19) + ৭টি ফিগার + `R_Analysis_Summary.xlsx`।

| ফাইল | কাজ |
|---|---|
| `scripts/R/MS499_full_analysis.R` | সম্পূর্ণ স্বয়ংসম্পূর্ণ বিশ্লেষণ — উপরের `INPUT_FILE` বদলালেই আসল ডাটা; `OUTPUT_DIR`, `MAKE_CHARTS`, `MAUND`, `MIN_CONS`, `MIN_MARKETS` সব কনফিগ এক জায়গায় |
| `scripts/compare_r_py.py` | R-আউটপুট বনাম Python-আউটপুট সেল-ফর-সেল তুলনা (রেফারেন্স যাচাই) → বর্তমানে **২২/২৩ টেবিল হুবহু মিল** |

**ডিপেন্ডেন্সি সর্বনিম্ন: base R + `readxl` + `openxlsx`** — dplyr/ggplot2/tidyr দরকার নেই, তাই স্টক R-ইনস্টলেই চলে।

```r
install.packages(c("readxl","openxlsx"))   # একবার
setwd("path/to/TermPaperNew")
source("scripts/R/MS499_full_analysis.R")
```

আউটপুট: `analysis_outputs_r/`-এর ভেতরে `tables/*.csv`, `charts/*.png`, `R_Analysis_Summary.xlsx`। মিল যাচাই: `python scripts/compare_r_py.py`। বাকি থাকা ১টি পার্থক্য হলো T15-এর Fisher-exact p — Monte-Carlo (B=100,000) অনুমান, ইঞ্জিনভেদে ৩য় দশমিকে সরতে পারে; এটি ত্রুটি নয় এবং টেবিল-নোটে নথিভুক্ত।

## আসল ডাটা দিয়ে রিপ্লেস করার নিয়ম

1. `03_data_entry_template/` থেকে খালি টেমপ্লেটের একটা কপি নিয়ে কাজ করুন (বা `04_data_filled/`-এর ফাইলেই)।
2. **শুধু হলুদ ঘরে লিখুন।** নীল কলাম (ফর্মুলা: কেজি-রূপান্তর, কেজি-পরিমাণ) আর ধূসর ঘর (আইডি, কোড) অবিকৃত রাখুন।
3. দাম লিখলে ইউনিট কলাম (Maund/Kg) অবশ্যই দিন; আজ যে মাছ কেনেনি সেই দাম-ঘরে `K`, উত্তর দিতে রাজি না হলে `D` লিখুন।
4. Form A/B/R-এর পেমেন্ট শতাংশ (Cash+MFS+Credit) = ১০০ রাখুন।
5. Pair_ID দিয়ে কেনা-বেচার জোড়া মিলিয়ে রাখুন (QC sheet নিজেই বলে দেবে)।
6. ব্যবহার শেষে দৌড়ান: `python scripts/verify_filled.py` → ২৪টি QC চেক পাস হতে হবে; তারপর `python scripts/run_analysis.py`।

## অন্য কাউকে (AI/সহকর্মী) কাজ দিতে চাইলে

কী প্রম্পট দিবেন — নিচের তিনটি ডকেই যথেষ্ট:

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
