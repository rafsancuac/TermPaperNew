# scripts/ — পুরো প্রসেসের স্ক্রিপ্ট

সব স্ক্রিপ্টই রিপো-রুট থেকে আপেল হয় (`python scripts/<name>.py`), কোনো হার্ডকোডেড পথ নেই — যেকোনো মেশিনে চলবে।

নির্ভরতা: `pip install openpyxl pandas matplotlib numpy scipy pdfplumber`

| ক্রম | স্ক্রিপ্ট | কী করে | কখন চালাবেন |
|---|---|---|---|
| ১ | `extract_pdfs.py` | 01_source_pdfs-এর সব PDF থেকে টেক্সট বের করে 02_extracted_text-এ .txt লেখে | PDF যোগ/বদলালে |
| ২ | `generate_synthetic_data.py` | পরিষ্কার-লেবেলযুক্ত **সিন্থেটিক** ডাটাসেট তৈরি করে (seed=20260315) → `04_data_filled/SYNTHETIC_v3_*_Filled.xlsx`; শুধু হলুদ ঘর লেখে, নীল ফর্মুলা/ধূসর প্রিফিল অবিকৃত | পাইপলাইন-টেস্টের জন্য নতুন সিন্থেটিক ডাটাসেট দরকার হলে |
| ২b | `qc_recalc.py` | ডেরাইভড (নীল) কলাম + ২৪টি QC চেক Python-এ পুনর্গণনা করে **লিটারেল ভ্যালু** হিসেবে লেখে — স্প্রেডশিট-ইঞ্জিন ছাড়াই Excel/pandas/R-এ একই ফল | `generate_synthetic_data.py`-এর সাথে সাথে (এটা ছাড়া QC সেল ফাঁকা থাকে) |
| ৩ | `verify_filled.py` | QC_Check-এর ২৪টি চেক (Status=কলাম E থেকে; fail হলে exit≠0), Progress_Dashboard, ভ্যালিডেশন-সারভাইভাল, চেইন-সামঞ্জস্য, Pair_ID, পেমেন্ট-যোগফল যাচাই | প্রতিবার ডাটা বদলানোর পরে |
| ৪ | `run_analysis.py` | **মূল বিশ্লেষণ** → analysis_outputs/ (১২ টেবিল CSV, ৭ চার্ট PNG, Analysis_Summary.xlsx) | প্রতিবার ডাটা বদলানোর পরে |
| ৫ | `extend_analysis.py` | **পরিসংখ্যান-এক্সটেনশন** → T12–T17 CSV + C8 PNG + Analysis_Summary.xlsx-এ শিট (Wilcoxon, species×market spread/KW/Dunn–Holm, χ², MWU, Spearman) | run_analysis.py-এর পরে |
| ৬ | `clean_data.py` | **ডাটা-ক্লিনিং** (S1 কাঠামো → S2 K/D-মিসিং → S3 রেঞ্জ-লজিক → S4 Tukey-আউটলায়ার-ফ্ল্যাগ → S5 সংবেদনশীলতা) → 05_data_cleaned/ (লগ+রিপোর্ট+ক্লিনড CSV) | extend_analysis.py-এর পরে |
| ৭ | `make_charts_v2.py` | **প্রকাশনা-ফিগার স্যুট** F1–F8+A1–A2 (1000 dpi, Times-স্টাইল সেরিফ, টাইটেল উপরে-মাঝ, লিজেন্ড নিচে-মাঝ, মেজর+মাইনর গ্রিড, ভ্যালু-লেবেল) → analysis_outputs/charts_v2/ + FIGURE_INDEX.csv | clean_data.py-এর পরে (পেপারে এগুলোই ব্যবহার করুন) |
| ৮ | `review_audit.py` | ৬৫-চেক স্বাধীন অডিট (কোটা, চেইন-মনোটোনিসিটি, T3/T10 পুনর্গণনা ইত্যাদি; pair-চেক চ্যানেল-অর্ডার-সচেতন, other-fish ব্যান্ড চিংড়ি/লবস্টার-সচেতন) | সব আউটপুটের পরে |
| — | `R/MS499_full_analysis.R` | **স্বয়ংসম্পূর্ণ R-স্ক্রিপ্ট** — T1–T19 সব টেবিল + ৭ ফিগার + `R_Analysis_Summary.xlsx`; base R + `readxl` + `openxlsx` (dplyr/ggplot2 দরকার নেই) → স্টক R-এ চলে | আপনার নিজের Local R/RStudio-তে দ্বৈত-যাচাইয়ের জন্য |

**সাধারণ কাজের ফ্লো (আসল ডাটার জন্য):**
```
টেমপ্লেটে হলুদ ঘরে ডাটা লিখুন (Excel-এ হাতে)
   → python scripts/verify_filled.py     (২৪টি QC পাস — নিশ্চিত করুন)
   → python scripts/run_analysis.py       (টেবিল+চার্ট রিফ্রেশ)
   → python scripts/extend_analysis.py    (পরিসংখ্যান টেবিল রিফ্রেশ)
   → python scripts/clean_data.py         (ক্লিনিং-লগ+আউটলায়ার+সংবেদনশীলতা)
   → python scripts/make_charts_v2.py     (প্রকাশনা-ফিগার 1000 dpi)
   → python scripts/review_audit.py       (৬৫-চেক অডিট)
   → পেপারে সংখ্যা/ফিগার তুলে নিন
   → (অপশনাল) Rscript scripts/R/MS499_full_analysis.R  — দ্বৈত-যাচাই
```

টেকনিক্যাল নোট:
- `generate_synthetic_data.py` শুধু হলুদ ঘর লেখে; নীল ফর্মুলা ও ধূসর প্রিফিল অবিকৃত রাখে। **v3 (seed 20260315):** বাজার-দিন দাম-অ্যাংকর (W/RC), সেশনের ভেতরে ভোক্তার সময়, নিরপেক্ষ প্রজাতি-নির্বাচন, সোর্স-নির্ভর কেনা-দাম, "D"-ফ্ল্যাগ সংশোধন, পেয়ার-সুরক্ষা ও ৪টি কভারেজ-গার্ড (ভোক্তা ≥৩ / ল্যান্ডিং ≥২ / PO ≥২০ / রিটেইল-বাজার ≥৩ প্রতি প্রজাতি) — জেনারেশনের শেষে সেলফ-চেক ফেল করলে ফাইলই লেখা হয় না। ফর্মুলার ক্যাশড মান পাইথনে কম্পিউট হয় না বলে `run_analysis.py` নিজে মণ→কেজি রূপান্তর হিসাব করে ফলব্যাক হিসেবে — তাই ফ্রেশ-জেনারেটেড ফাইলেও বিশ্লেষণ ঠিক চলে।
- `run_analysis.py --data <path>` দিয়ে যেকোনো পূরণ-করা কপি বিশ্লেষণ করা যায়।
