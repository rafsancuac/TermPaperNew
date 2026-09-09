# scripts/ — পুরো প্রসেসের স্ক্রিপ্ট

সব স্ক্রিপ্টই রিপো-রুট থেকে আপেল হয় (`python scripts/<name>.py`), কোনো হার্ডকোডেড পথ নেই — যেকোনো মেশিনে চলবে।

নির্ভরতা: `pip install openpyxl pandas matplotlib numpy scipy pdfplumber`

| ক্রম | স্ক্রিপ্ট | কী করে | কখন চালাবেন |
|---|---|---|---|
| ১ | `extract_pdfs.py` | 01_source_pdfs-এর সব PDF থেকে টেক্সট বের করে 02_extracted_text-এ .txt লেখে | PDF যোগ/বদলালে |
| ২ | `inspect_template.py` | টেমপ্লেটের ১৬ শিটের কাঠামো (হেডার, ডাটা-রেঞ্জ) | বোঝার জন্য, দরকার নেই প্রতিবার |
| ৩ | `inspect_codebooks.py` | বাজার/প্রজাতি কোডবুক দেখায় | 〃 |
| ৪ | `inspect_validations.py` | প্রতিটি শিটের ড্রপডাউন ভ্যালিডেশন লিস্ট | 〃 |
| ৫ | `inspect_formats.py` | কোন কলাম কী ফরম্যাট (তারিখ/সংখ্যা/ফরম্যাট-কোড) | 〃 |
| ৬ | `fill_survey_data.py` | খালি টেমপ্লেটে **সিমুলেটেড** চট্টগ্রাম ডাটা ভরে (seed=20260302) → 04_data_filled | নতুন সিমুলেটেড ডাটাসেট দরকার হলে (উপরের `rng = random.Random(...)` লাইনে seed বদলান) |
| ৭ | `verify_filled.py` | QC_Check-এর ২৪টি চেক (Status=কলাম E থেকে; fail হলে exit≠0), Progress_Dashboard, ভ্যালিডেশন-সারভাইভাল, চেইন-সামঞ্জস্য, Pair_ID, পেমেন্ট-যোগফল যাচাই | প্রতিবার ডাটা বদলানোর পরে |
| ৮ | `run_analysis.py` | **মূল বিশ্লেষণ** → analysis_outputs/ (১২ টেবিল CSV, ৭ চার্ট PNG, Analysis_Summary.xlsx) | প্রতিবার ডাটা বদলানোর পরে |
| ৯ | `extend_analysis.py` | **পরিসংখ্যান-এক্সটেনশন** → T12–T17 CSV + C8 PNG + Analysis_Summary.xlsx-এ শিট (Wilcoxon, species×market spread/KW/Dunn–Holm, χ², MWU, Spearman) | run_analysis.py-এর পরে |
| ১০ | `clean_data.py` | **ডাটা-ক্লিনিং** (S1 কাঠামো → S2 K/D-মিসিং → S3 রেঞ্জ-লজিক → S4 Tukey-আউটলায়ার-ফ্ল্যাগ → S5 সংবেদনশীলতা) → 05_data_cleaned/ (লগ+রিপোর্ট+ক্লিনড CSV) | extend_analysis.py-এর পরে |
| ১১ | `make_charts_v2.py` | **প্রকাশনা-ফিগার স্যুট** F1–F8+A1–A2 (1000 dpi, Times-স্টাইল সেরিফ, টাইটেল উপরে-মাঝ, লিজেন্ড নিচে-মাঝ, মেজর+মাইনর গ্রিড, ভ্যালু-লেবেল) → analysis_outputs/charts_v2/ + FIGURE_INDEX.csv | clean_data.py-এর পরে (পেপারে এগুলোই ব্যবহার করুন) |
| ১২ | `review_audit.py` | ৬৫-চেক স্বাধীন অডিট (কোটা, চেইন-মনোটোনিসিটি, T3/T10 পুনর্গণনা ইত্যাদি) | সব আউটপুটের পরে |
| — | `R/run_analysis.R` | **R-এ স্বাধীন পুনর্গণনা** — Python পাইপলাইনের টেবিল/টেস্ট R-এ মিরর করে কনসোলে [OK/!!] MATCH/MISMATCH যাচাই-রিপোর্ট ছাপে; r_outputs/tables+charts-এ CSV/ফিগার লেখে | আপনার নিজের PC-তে দ্বৈত-যাচাইয়ের জন্য (openxlsx দরকার; ggplot2 থাকলে ফিগারও) |
| — | `inspect_filled_for_analysis.py` | পূরণ-করা ফাইলের হেডার/রো-কাউন্ট ডাম্প (ডেভ-টুল) | ডিবাগের দরকার হলে |
| — | `explore_issues.py` | অডিট-প্রোব (producer-price scope, additivity, pair usability, সেল-কভারেজ) — শুধু প্রিন্ট করে | রিভিউ/ডিবাগে |

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
   → (অপশনাল) Rscript scripts/R/run_analysis.R  — দ্বৈত-যাচাই
```

টেকনিক্যাল নোট:
- `fill_survey_data.py` শুধু হলুদ ঘর লেখে; নীল ফর্মুলা ও ধূসর প্রিফিল অবিকৃত রাখে। ফর্মুলার ক্যাশড মান পাইথনে কম্পিউট হয় না বলে `run_analysis.py` নিজে মণ→কেজি রূপান্তর হিসাব করে ফলব্যাক হিসেবে — তাই ফ্রেশ-জেনারেটেড ফাইলেও বিশ্লেষণ ঠিক চলে।
- `run_analysis.py --data <path>` দিয়ে যেকোনো পূরণ-করা কপি বিশ্লেষণ করা যায়।
