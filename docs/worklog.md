# Worklog

---
Task ID: 1
Agent: Super Z (main agent)
Task: PDF-এ থাকা সার্ভে প্রশ্নপত্র অনুযায়ী Marine Fish Marketing Data Entry এক্সেলে চট্টগ্রামের ডাটা পূরণ

Work Log:
- xlsx skill লোড করে edit scene + quality/pipeline.md + templates/base.py সম্পূর্ণ পড়া হয়
- টেমপ্লেট পরিদর্শন: ১৬টি শিট, ড্রপডাউন ভ্যালিডেশন লিস্ট, নীল ফর্মুলা কলাম, QC নিয়ম, প্রিফিল্ড ID ম্যাপিং যাচাই
- ৮টি PDF থেকে টেক্সট এক্সট্র্যাক্ট (pdfplumber); Methodology V4 + ৫টি বাংলা প্রশ্নপত্র + Tag-price ফর্ম বিশ্লেষণ
- ব্যবহারকারীর "চালিয়ে যাও" নির্দেশে সুপারিশকৃত ডিফল্ট নেওয়া হয় (১২০ কোটা, বাস্তবসম্মত সিমুলেটেড, মার্চ ২০২৬, ইংরেজি, পূর্ণ রিয়ালিজম, একজন গবেষক, পূর্ণ ট্যাগ-প্রাইস, ২০২৬-এর দাম)
- scripts/fill_survey_data.py লেখা (seed=20260302): চেইন-কনসিস্টেন্ট দাম মডেল (producer → aratdar → bepari → retailer → consumer), Pair_ID মিল, K/D ফ্ল্যাগ, মণ→কেজি রাউন্ডিং
- জেনারেশন: ১২০ রেসপন্ডেন্ট, ৪৬৩ Price_Observations, ৬৯+১৯ ক্রেতা-কেনা রো, ১৩৫ ট্যাগ-প্রাইস, ৬ Form M, ৭ লগ-ভিজিট, ১৬ মিলে-যাওয়া জোড়া
- LibreOffice recalc (২৯৭০ ফর্মুলা, ০ এরর) → audit (০ এরর) → scan (শুধু টেমপ্লেটের নিজস্ব প্যাটার্ন) → validate exit 0
- QC_Check: ২৪/২৪ চেক পাস — TARGET MET, ডুপ্লিকেট ০, Payment% ১০০, Pair_ID ৩২/৩২ All matched, Form M COMPLETE
- কসমেটিক পলিশ: ভাড়া/বিদ্যুৎ/ভাড়া-খরচ রাউন্ড সংখ্যা করে পুনঃজেনারেট + পুনঃrecalc + পুনঃযাচাই

Stage Summary:
- ডেলিভারেবল: /home/z/my-project/download/Marine_Fish_Marketing_Data_Entry_Chattogram_Filled.xlsx (২০৩ KB)
- ডাটা সিমুলেটেড (টেমপ্লেটের সব নিয়ম মেনে, বাস্তব ২০২৬-স্তরের চট্টগ্রাম দামে); আসল ফিল্ড ডাটা এলে একই ঘরে প্রতিস্থাপনযোগ্য
- স্ক্রিপ্ট পুনঃব্যবহারযোগ্য: seed বদলালে নতুন ডাটাসেট, প্যারামিটার বদলালে অন্য পরিমাণ/সময়কাল

---
Task ID: 2
Agent: Super Z (main agent)
Task: সব কাজ/প্রসেস/ফাইল https://github.com/rafsancuac/TermPaperNew রিপোতে গুছিয়ে তোলা — লেখালেখি ও পুরো বিশ্লেষণের এক-রিপো সমাধান

Work Log:
- পূর্ববর্তী সেশনের ডেলিভারেবল পুনরায় যাচাই (verify_filled.py: QC ২৪/২৪, চেইন-সামঞ্জস্য, Pair_ID মিল)
- TermPaperNew রিপো-কাঠামো তৈরি: 01_source_pdfs (৮ PDF) / 02_extracted_text (৮ txt) / 03_data_entry_template / 04_data_filled / scripts / analysis_outputs / docs
- scripts/run_analysis.py (নতুন, ~৮৯০ লাইন, পোর্টেবল): ১২টি বিশ্লেষণ টেবিল (T1-T11+T2b) + ৭টি চার্ট PNG + Analysis_Summary.xlsx (Index শিটসহ); মণ→কেজি ফলব্যাক রূপান্তর; T3/T10 মেথডোলজি সামঞ্জস্যবদ্ধ (species-mean ভিত্তি)
- xlsx.py validate: Analysis_Summary.xlsx passed, ০ ইশ্যু
- ৮টি প্রসেস-স্ক্রিপ্ট রিপোতে কপি করে পথগুলো রিপো-রিলেটিভ করা (make_repo_portable.py); সব স্ক্রিপ্ট py_compile OK, কোনো /home/z পথ অবশিষ্ট নেই
- ডকুমেন্টেশন: README.md (বাংলা, সতর্কতাসহ), docs/DATA_DICTIONARY.md (১৬ শিট-অভিধান), docs/WRITING_GUIDE.md (অধ্যায়→টেবিল-ম্যাপ), scripts/README.md
- git init + commit (main) + remote origin সেট; পুশ-ক্রেডেনশিয়াল না থাকায় bundle + zip ফলব্যাক download/ এ তৈরি

Stage Summary:
- রিপো: /home/z/my-project/TermPaperNew (২.৭ MB, ৫৩টি ট্র্যাকড ফাইল) — ডাটা+প্রসেস+বিশ্লেষণ+লেখার গাইড সম্পূর্ণ
- মূল ফল: producer share ৭৩.৯%, খুচরা মার্জিন ১২২ টাকা/কেজি (১৬.৭%), আড়তদার ২৫ (৩.৪%), বেপারি ৬৩ (৮.৫%)
- GitHub পুশের জন্য PAT টোকেন দরকার; TermPaperNew.bundle + TermPaperNew.zip তৈরি করা হয়েছে

---
Task ID: 3
Agent: Super Z (main agent)
Task: ব্যবহারকারীর প্রশ্ন — (১) মেথডোলজি+সার্ভে ফর্ম PDF রিপোতে আছে কিনা নিশ্চিত করা, (২) অন্য কাউকে কাজ/বিশ্লেষণ দিতে রেডি প্রম্পট তৈরি

Work Log:
- যাচাই: 01_source_pdfs/ এ ৮টি PDF সম্পূর্ণ (Methodology V4 + FIXED, ৫টি বাংলা প্রশ্নপত্র, Tag-price) + 02_extracted_text/ এ ৮টি txt — রিপোতে কমিটেড (b1d1cd0)
- git push চেষ্টা: ক্রেডেনশিয়াল নেই ("could not read Username") — PAT ছাড়া সম্ভব নয়; bundle/zip ফলব্যাকই বহাল
- docs/MASTER_PROMPT.md নতুন: PART 1 master context prompt (রিপো-ম্যাপ, ডিজাইন, নিয়ম, K/D, QC, সতর্কতা, ফলাফল, রিন-কমান্ড) + PART 2/3/3b/4/5 টাস্ক-ব্লক (লেখা/বিশ্লেষণ/আসল ডাটা/মানুষ/চ্যাট-সংক্ষিপ্ত)
- README.md আপডেট: রিপো-ম্যাপে MASTER_PROMPT.md + নতুন হস্তান্তর-সেকশন
- কমিট 1297e93; bundle (1.5 MB) ও zip (1.8 MB) নতুন করে রিবিল্ড

Stage Summary:
- ৮ PDF রিপোতে নিশ্চিত; হস্তান্তর-প্রম্পট রেডি: repo docs/MASTER_PROMPT.md (ইংরেজি প্রম্পট + বাংলা ব্যবহার-নির্দেশিকা)
- GitHub-এ সরাসরি পুশ এখনো সম্ভব নয় (PAT দরকার); download/TermPaperNew.bundle ও .zip সর্বশেষ স্ন্যাপশট

---
Task ID: 4
Agent: Super Z (main agent)
Task: ব্যবহারকারীর দেওয়া PAT দিয়ে TermPaperNew রিপো GitHub-এ পুশ

Work Log:
- টোকেন ফাইলে/কনফিগে সেভ না করে ওয়ান-টাইম credential helper (-c) দিয়ে পুশ — origin URL-এ টোকেন অবশিষ্ট নেই
- পুশ সফল: main -> main (নতুন ব্রাঞ্চ), ৩ কমিট (b1d1cd0, 1297e93, abcb013) আপলোড
- যাচাই: git ls-remote HEAD = abcb013 = লোকাল HEAD — হুবহু মিল
- পাবলিক-অ্যাক্সেস টেস্ট: টোকেন ছাড়া ls-remote সফল — রিপো public, যে কেউ ক্লোন করতে পারে

Stage Summary:
- রিপো লাইভ: https://github.com/rafsancuac/TermPaperNew (main, HEAD abcb013)
- ৫৩+ ফাইল অনলাইনে: ৮ PDF, ৮ txt, টেমপ্লেট+ফিলড এক্সেল, ১২ টেবিল + ৭ চার্ট, Analysis_Summary.xlsx, ১০ স্ক্রিপ্ট, ৫ ডকুমেন্ট (MASTER_PROMPT.md-সহ)
- ব্যবহারকারীকে পরামর্শ: চ্যাটে শেয়ার করা PAT পরে revoke/regenerate করা উচিত

---
Task ID: 5
Agent: Arena.ai research assistant (supervisor/reviewer role)
Task: রিপোর ডাটা/স্ক্রিপ্ট/ডক সুপারভাইজর-রিভিউ + Wilcoxon/species×market এক্সটেনশন + লেখা-প্রস্তুতি

Work Log:
- বেসলাইন রিরান: verify_filled.py (সব QC মান পাস) ও run_analysis.py (T1–T11+T2b, C1–C7, Analysis_Summary.xlsx)।
- **verify_filled.py-এ কলাম-অদলবদল বাগ শনাক্ত ও ঠিক**: QC_Check-এর Status কলাম E, Rule D — আগের স্ক্রিপ্ট উল্টো পড়ত (D-কে status ধরে), তাই সব পাস হলেও "non-passing checks: 24" ছাপত। ঠিক করা হয়েছে (PASS/FAIL প্রিন্ট, checks read, fail হলে exit code 1)।
- **মূল মার্জিন টেবিলের গাণিতিক অসামঞ্জস্য শনাক্ত ও run_analysis.py-তে ঠিক** (T3/T10): পুরোনো কনভেনশনে A+B+R+PS = ১০২.৫% (>১০০)। কারণ: (১) producer-দামে M2–M5 আরাতদার-কেনা (প্রথম-বিক্রয় নয়) মেশানো ছিল; (২) খুচরা মার্জিন retailer-উদ্ধৃতি থেকে, আর PS/স্প্রেড ভোক্তা-প্রদেয় দাম থেকে — ২.৫% ফাঁক। সমাধান: producer ও নিলাম-বেচা শুধু ল্যান্ডিং-বাজার M1/M6; খুচরা মার্জিন = ভোক্তা-প্রদেয় − বেপারি-বেচা; ALL/T10 চেইন-সম্পূর্ণ প্রজাতিতে (S01–S09; S10 বাদ — ল্যান্ডিং-এ আরাতদার-বেচা নেই)। নতুন ফল: **PS ৭০.৯%, মার্জিন A ২৫.৮ (৩.৩%) / B ৯২.৭ (১১.৭%) / R ১১১.৪ (১৪.১%), স্প্রেড ২২৯.৯ (২৯.১%) → ১০০%-এ হুবহু মেলে**।
- **extend_analysis.py** (নতুন): T12 জোড়া-বিস্তার + T12b Wilcoxon (১৪ পূর্ণ জোড়া; W=২৩, p=০.১১৬ → সামঞ্জস্যপূর্ণ); T13 species×market spread; T14 KW (exploratory n≥৩: S01–S03/S05/S06 p<০.০৫) + T14b Dunn–Holm (S01-এ শুধু Fishery Ghat–Bahaddarhat তুলনাটিই টিকে থাকে); T15 পেমেন্ট×অভিনেতা χ² (p=০.৮৭, G-test ০.৮৮); T16 স্তরভেদে মার্জিন MWU (সব p<০.০০০১); T17 খুচরা MC–মুনাফা Spearman (rho=০.৪৩, p=০.০১৮); C8 চার্ট; সব Analysis_Summary.xlsx-এ (Index-সহ ২০ শিট)।
- পেয়ার-অ্যালাইনমেন্ট বাগ ঠিক: চ্যানেল-অর্ডার মানা হয় না এমন জোড়া বাতিল (PAIR-M3-02 ও M5-03 অসম্পূর্ণ)।
- ডক হালনাগাদ: README, docs/WRITING_GUIDE.md, docs/MASTER_PROMPT.md, scripts/README.md (নতুন সংখ্যা, run-order, T12–T17/C8 ম্যাপ; ক্যাপাসিটি ১,১০০→৭৯৭ ও ১২০→১০০ কেজি)।
- লিটারেচার/রিয়ালিজম বেঞ্চমার্ক (ওয়েব সার্চ): সমুদ্রমৎস্য মার্জিন ২৬–৩০%, জেলের অংশ ৫৫–৭৬%; আড়তদার কমিশন ৩–৬%; বাংলাদেশ MFS অ্যাকাউন্ট >২১০ মিলিয়ন (FY25), খুচরায় নগদ ~৩৫% — সিমুলেটেড সংখ্যার সাথে সঙ্গতিপূর্ণ।
- ড্রাফট: paper_drafts/chapter_02_literature_review.md ও chapter_04_results_and_discussion.md (টেবিল-সংখ্যা দিয়ে, [SIMULATED] ফুটনোটসহ)।
- সম্পূর্ণ রিভিউ নোট: docs/SUPERVISOR_REVIEW.md (বাংলা, সুপারভাইজর-ভিউ)।

Stage Summary:
- সব এক্সটেনশন আউটপুট analysis_outputs/-এ; 04_data_filled/ অপরিবর্তিত (সিমুলেটেড); রিপো কমিট ও পুশ হয়েছে।
- পরবর্তী: আসল ডাটা এলে হলুদ ঘরে → verify_filled (২৪/২৪) → run_analysis → extend_analysis → সংখ্যা হালনাগাদ।
---
Task ID: 6a
Agent: Arena.ai research assistant
Task: দ্বিতীয় রিভিউয়ারের ৭টি দাবি যাচাই ও সে অনুযায়ী ফিক্স (২০২৬-০৯-০৯)

Work Log:
- দাবি-যাচাই: #1 (৩.৮ পরীক্ষা run_analysis-এ নেই → সত্যি ছিল; extend_analysis.py-ই সব পরীক্ষা চালায় — এ পর্বে Shapiro–Wilk T18 যোগ, run_analysis-এর শেষে NOTE-পয়েন্টার); #2 (spread ≠ মার্জিন-সমষ্টি → পূর্বের কমিটে সত্যি, H2/H3-এ ঠিক হয়েছে; এখন হুবহু মেলে); #3 (WRITING_GUIDE-এ ১,১০০/১২০ কেজি → সত্যি ছিল, H9-এ ঠিক; MASTER_PROMPT PART 5-এর ৭৩.৯% লাইন আজ ঠিক); #4 (হিলশা PS বনাম pooled গুলানোর ঝুঁকি — সংখ্যা-হালনাগাদে নিষ্পন্ন); #5 (S08/S09/S10 descriptive-নিয়ম — T3-তে Retail_markets_n + Reporting_status কলাম, ক্যাভিয়েট ডক/ড্রাফটে); #6 (R-বাক্য বনাম Python — টেক্সট-সংশোধনের নির্দেশনা WRITING_GUIDE #8); #7 (T9 টাইটেল → "Other aquatic products")।
- T15: sparse-সেলে G-test-এর সাথে exact Freeman–Halton/Fisher 3×3 যোগ (স্যানিটি-টেস্ট: dense টেবিলে χ²-অনুমানের কাছাকাছি; আমাদের টেবিলে p=0.8945)।
- T18 Shapiro–Wilk: পাঁচটি pooled সিরিজই non-normal (p<0.001) → §3.8-এর nonparametric যুক্তি মজবুত।
- সাহিত্য-যাচাই (ওয়েব): Jahan et al. 2024 (JARD 74(4), DOI 10.17306/J.JARD.2024.00001) ✓; ২০২৫ ইলিশ-দাম (Dhaka retail ৯০০–২,২০০ Tk/kg, +২৯% YoY; Cox's Bazar ১–১.৪ কেজি ~১,৮০০ wholesale) ✓ → চ্যাপ্টার 2/4-এ যোগ; landing-city বনাম দূরবর্তী-চেইন PS-পার্থক্যের ব্যাখ্যা যোগ।
- ড্রাফট/ডক আপডেট: chapter_02 (Jahan 2024 + দাম-ট্রেন্ড), chapter_04 (S08–S10 ক্যাভিয়েট, Shapiro/Fisher ফলাফল, রিয়েল-ডাটা মূল্যস্ফীতি-চেক নোট), WRITING_GUIDE (সাবধানতা ৬–৮, T18-ম্যাপ), MASTER_PROMPT (PART 4/5), SUPERVISOR_REVIEW.md পরিশিষ্ট B, worklog।
- পাইপলাইন রিরান: verify ২৪/২৪ → run_analysis → extend_analysis (T18-সহ ৯ শিট) → Analysis_Summary ২১ শিট।

Stage Summary:
- ৭ দাবির মধ্যে ৩টি (১,৩,৫) বর্তমান-অবস্থায় সত্যি ছিল → ফিক্স; ২টি (২,৪) আগের পর্বে ফিক্সড; ২টি (৬,৭) নির্দেশনামূলক → সম্পন্ন; সাহিত্য-দাবি (Jahan 2024, দাম-ট্রেন্ড) যাচাই করে ড্রাফটে ঢোকানো হয়েছে। কমিট + পুশ হবে।

---
*(উপরের 6a ও নিচের 6b একই সময়ে চলা দুটি সমান্তরাল রিভিউ-সেশন — Arena.ai ও Super Z; উভয়ের আউটপুটই মার্জ করা হয়েছে।)*


---
Task ID: 6b
Agent: Super Z (main agent, সমান্তরাল রিভিউ-সেশন)
Task: সুপারভাইজার-রিভিউ + বাস্তবতা-যাচাই + রিসেন্ট-পেপার অনুসন্ধান; Task 5-এর Arena.ai কাজের সঙ্গে মার্জ

Work Log:
- scripts/review_audit.py লেখা (৬৫ চেক): কোটা/ID/তারিখ-সূচি/বয়স↔অভিজ্ঞতা↔শিক্ষা/ভলিউম-অর্ডারিং/পেমেন্ট-যোগফল/চেইন-মনোটোনিসিটি/প্যার-দাম-মিল/ভোক্তা↔খুচরা গ্যাপ/ট্যাগ↔খুচরা মিল (মধ্যম ২.৫%)/GPS/T3-T10 স্বাধীন পুনঃগণনা → ৬২ PASS / ৩ WARN / ০ FAIL
- Task 5 (Arena.ai) রিমোটে পুশ হওয়ার পর আমার সমান্তরাল কমিটের সঙ্গে মার্জ: তাদের SUPERVISOR_REVIEW.md/H1-H10 প্রাধান্য পেয়েছে; আমার পুরনো REVIEW_SUPERVISOR.md বাদ; আমার ইউনিক যোগ অংশ রাখা হয়েছে
- review_audit.py নতুন কনভেনশনে হালনাগাদ (producer/নিলাম = M1/M6; ভোক্তা-অ্যাংকরড খুচরা মার্জিন) এবং মার্জড T3/T10-কে স্বাধীনভাবে যাচাই করেছে: PS ৭১.২% (সব প্রজাতি) vs T10 ৭০.৯% (চেইন-সম্পূর্ণ ৯); মার্জিন ২৫.৮/৯২.৮/১১১.৩ ≈ T10-এর ২৫.৮/৯২.৭/১১১.৪; টেলিস্কোপিং A+B+R = spread = ২২৯.৯২ হুবহু ✓
- docs/LITERATURE_NOTES.md (নতুন, ইউনিক): ৯টি ওয়েব-সার্চ থেকে ১৩+ প্রকাশিত রেফারেন্স (Jahan 2024 ৯-মেরিন-প্রজাতি মার্জিন, Islam 2001 ক্লাসিক, Rafi 2024, Yasmin 2024, Dipty 2026, DoF/FAO ইত্যাদি) + অধ্যায় ২-এর ৪-খণ্ড কাঠামো + দাম-বাস্তবতা যাচাই (PS ৭০-৭৭% প্রকাশিত রেঞ্জ, কমিশন ৩-৫%, ইলিশ ৯০০-৩,২০০ ব্যান্ড, ভোক্তা-MFS ৫৭% উঁচু ফ্ল্যাগ)
- README/MASTER_PROMPT-এ LITERATURE_NOTES + review_audit সংযোগ; WRITING_GUIDE-এর ৭৯৭/১০০ কেজি ফিক্স Task 5-এ সমরূপ, তাদের সংস্করণ রাখা হয়েছে

Stage Summary:
- মার্জ সম্পূর্ণ: রিপো = Task 5 (পাইপলাইন-ফিক্স + স্ট্যাট-এক্সটেনশন + ড্রাফট) + Task 6 (স্বাধীন যাচাই + লিটারেচার-প্যাক); ০ ফেটাল ইস্যু, বাকি ৩টি WARN ডকুমেন্টেড
- LITERATURE_NOTES.md chapter_02 ড্রাফটের সিটেশন-ভিত্তি দেয়; review_audit.py আসল ডাটা এলে পুনঃব্যবহারযোগ্য

---
Task ID: 7
Agent: Arena.ai research assistant
Task: তৃতীয় রিভিউয়ারের (রাউন্ড ৩) ৩টি নতুন দাবি যাচাই ও ফিক্স (২০২৬-০৯-০৯)

Work Log:
- #8 (verify_filled.py কলাম-সোয়াপ): বর্তমান ফাইলে column=4=Rule/column=5=Status, আউটপুট "checks read: 24; non-passing: 0", exit 0 — রাউন্ড ১-এর কমিট 7296015-এ ফিক্সড; দাবিটি পুরোনো ভার্সনের বিরুদ্ধে। → প্রমাণ-সহ নথিভুক্ত।
- #9 (T6 nondeterminism): কমিট 149864a-তে tie-break-সহ সর্ট; ৩টি টানা রানে T6-এর MD5 অভিন্ন — ফিক্সড প্রমাণিত।
- #10 (S08/S10-এর PS = n=1 ভোক্তার ওপর): raw Consumer_Purchases_Focal থেকে যাচাই — সত্যি (S08:1, S10:1; S02/S03:3)। ফিক্স: MIN_CONS=3; T3-তে Consumer_paid_n কলাম; S08/S10-এর PS/মার্জিন/spread ব্ল্যাংক + Reporting_status-কারণ; পুল = ৮ প্রজাতি (S01–S07, S09); T10-ও একই নিয়মে; review_audit-এর পুনঃগণনা একই নিয়মে হালনাগাদ।
- নতুন সংখ্যা: PS 70.9%; মার্জিন A 27.84 (3.3%) / B 99.58 (11.7%) / R 118.97 (14.0%); spread 246.39 (29.1%); A+B+R=spread; PS+margin=100%।
- review_audit: PASS=62 / WARN=3 (নথিভুক্ত: pair-অ্যালাইনমেন্ট, crustacean-দাম-ব্যান্ড, S08/S10-কভারেজ) / FAIL=0।
- ডক/ড্রাফট হালনাগাদ: README, WRITING_GUIDE (#2/#6 + ৪.৩ সারি), MASTER_PROMPT (৩ জায়গা), chapter_04 (৪.৩/৪.৪/৪.১০), SUPERVISOR_REVIEW (সেকশন ৩ + পরিশিষ্ট C), worklog।
---
Task ID: 8
Agent: Arena.ai research assistant
Task: রেজাল্ট-সেকশনের জন্য সম্পূর্ণ R অ্যানালাইসিস স্যুট (scripts/R) — Python পাইপলাইনের প্রতিটি সংখ্যার সেল-ফর-সেল মিরর

Work Log:
- scripts/R/ লিখা: config.R (এক জায়গায় INPUT_FILE/OUTPUT_DIR; Windows-ডিফল্ট F:/TermPaperNew/Analysis), helpers.R (readxl-ভিত্তিক শিট-রিডার, numpy-bitwise np_sum/np_mean/np_sd, python-সমতুল্য round-half-even rp(), mc_names, Dunn-Holm), tables_descriptive.R (T1–T11+T2b), tables_inferential.R (T12–T18; হাতে-লেখা Freeman–Halton exact Fisher), figures.R (C1–C8, 300dpi, Times New Roman), excel_out.R (styled R_Analysis_Summary.xlsx + quality gates), run_all.R (মাস্টার)।
- Python-সংখ্যার সাথে সেল-ফর-সেল মিল আনতে ৩টি গভীর গরমিল ধরা ও মিরর করা হয়েছে: (ক) readxl বনাম openpyxl-এর ফাঁকা-সারি/কলাম নীতি (drop_id + Obs_Date-require); (খ) numpy np.mean/np.std-এর নির্দিষ্ট summation-order (n<8 sequential; ≤128 আট-অ্যাকিউমুলেটর; নাহলে 8-গুণিতক-ভাগ) — R-তে np_sum() পোর্ট, ৫০০ এলোমেলো ভেক্টরে bitwise 0/1000 mismatch; (গ) R round() বনাম python round(): exact-decimal half-even — rp() (sprintf-নির্ভর exact expansion), ৭০,০৩৫ কেসে 0 mismatch।
- সেল-ফর-সেল তুলনা স্ক্রিপ্ট scripts/compare_r_py.py → ২১/২১ টেবিল PASS (প্রতিটি সেল numeric-সমান, কলাম-অর্ডার/নাম হুবহু)। T2b-এর 'None'-ক্যাটাগরি সারি ও most_common টাই-অর্ডার, T5/T8/T9-এর tie-অর্ডার, T11-এর স্পেস-নাম, T12b-এর W-সংজ্ঞা, T14b-এর Holm-অর্ডার/আনরাউন্ডেড p, T15-এর লেবেল+exact-Fisher p=0.8945, T17-এর scipy t-approximation p=0.0177 — সব মিরর।
- Quality gates: A+B+R=246.39=spread [PASS], PS 70.9% [PASS], T3-ALL=T10 70.9% [PASS]; টেবিল ২টি টানা রানে MD5-অভিন্ন (deterministic); run_log.txt + R_Analysis_Summary.xlsx (২২ শিট) আউটপুটে।
- analysis_outputs_r/ = নন-উইন্ডোজ ডেভ-মিরর আউটপুট (রিপোতে কমিট); ব্যবহারকারীর Windows-এ আউটপুট যাবে F:/TermPaperNew/Analysis-এ।

---
Task ID: 9
Agent: Super Z (main agent)
Task: বর্তমান অবস্থা যাচাই + ডাটা-ক্লিনিং পাইপলাইন + প্রকাশনা-মানের চার্ট স্যুট v2 + R যাচাই-স্ক্রিপ্ট (Task 7-8 মার্জের পর MIN_CONS কনভেনশনে হালনাগাদ)

Work Log:
- অবস্থা যাচাই: আনকমিটেড পরিবর্তনগুলো ছিল শুধু ফাইল-মোড (644→755) — core.fileMode=false দিয়ে নিরপেক্ষ; QC রিরান: verify_filled 24/24 PASS, run_analysis/extend_analysis পুনঃউৎপাদনযোগ্য (T6-এ শুধু tie-অর্ডার বদল), review_audit 62 PASS/3 WARN/0 FAIL
- scripts/clean_data.py (নতুন): S1 কাঠামো (ID/কোটা/তারিখ/ডুপ্লিকেট) → S2 মিসিং-অডিট (K=48 buy, K=45+D=19 sell; প্রতি-ভ্যারিয়েবল রিপোর্ট) → S3 রেঞ্জ-লজিক (সব PASS) → S4 Tukey 1.5×IQR (৪০ গ্রুপ, ৮১৪ সেলের মধ্যে ১৭ ফ্ল্যাগ=২.১%, ফ্ল্যাগ-অনলি) → S5 সংবেদনশীলতা (MIN_CONS কনভেনশনে) → 05_data_cleaned/ (৬ ফাইল: লগ, মিসিং-রিপোর্ট, আউটলায়ার-ফ্ল্যাগ, সংবেদনশীলতা, price_obs_cleaned.csv, CLEANING_REPORT.md)
- scripts/make_charts_v2.py (নতুন): ১০টি প্রকাশনা-ফিগার → analysis_outputs/charts_v2/ — স্টাইল: Times New Roman (Liberation Serif metric-ইকুইভ্যালেন্ট), ১০০০ dpi, টাইটেল উপরে-কেন্দ্রে, লিজেন্ড (loc="outside lower center") প্লটের নিচে, পূর্ণ প্যারামিটার-নামের অক্ষ-লেবেল, মেজর+মাইনর গ্রিড, ভ্যালু-লেবেল; চার্ট-ধরন বৈচিত্র্য: F1 বার (মার্জিন), F2 বক্স (প্রজাতিভেদে দাম), F3 লাইন (চেইন-প্রগ্রেশন), F4 ডোনাট (ভোক্তা-দাম বিভাজন), F5 স্ট্যাকড বার (পেমেন্ট), F6 রাডার (অবকাঠামো ৩ বাজার×৭ সুবিধা), F7 রোজ (সমস্যা-ফ্রিকোয়েন্সি), F8 বার (বাজারভেদে দাম), A1 বক্স-লগ (ধারণক্ষমতা), A2 হরাইজন্টাল বার (PS প্রজাতিভেদে) + FIGURE_INDEX.csv; চেইন-পুল MIN_CONS নিয়মে (৮ প্রজাতি: S01–S07, S09)
- VLM-ভিত্তিক চার্ট-QC: ৩ রাউন্ড — ফিক্স করা হয়েছে F2/A1 (মিডিয়ান-লেবেল বক্স-কিনারায় ছুঁয়েছিল → বক্সের ভিতরে সাদা-ব্যাকগ্রাউন্ড লেবেল), F3 (পয়েন্ট-লেবেল ক্লিয়ারেন্স+va) — চূড়ান্ত: ১০/১০ পাস
- scripts/R/run_analysis.R (নতুন, Task 8-এর run_all.R-এর পূরক — হালকা যাচাই-পথ): openxlsx দিয়ে ওয়ার্কবুক পড়া (startRow=4), K/D-ক্লিনিং মিরর, T1/T2/T3/T5/T10/T11/T12b/T14/T15/T16/T17 পুনর্গণনা (MIN_CONS-সহ), r_outputs/tables/*.csv, ~৫৮টি নম্বরযুক্ত [OK/!!] MATCH/MISMATCH কনসোল-রিপোর্ট (Python-রেফারেন্স এমবেডেড — Task 7-8-এর নতুন সংখ্যায় হালনাগাদ), ggplot2-তে ৫টি v2-ফিগার (Windows-এ আসল Times New Roman, ১০০০ dpi)
- Task 7-8 (Arena.ai রিমোট) মার্জ: T6/xlsx/C2/C5 → রিমোট ভার্সন; WRITING_GUIDE → নতুন সংখ্যা + v2-সেকশন একত্র; worklog → টাস্ক-নম্বর রি-অর্গানাইজ
- ডক হালনাগাদ: README, WRITING_GUIDE, MASTER_PROMPT, scripts/README, .gitignore (r_outputs/)

Stage Summary:
- নতুন ডেলিভারেবল: 05_data_cleaned/ (৬ ফাইল), analysis_outputs/charts_v2/ (১০ ফিগার ১০০০ dpi + ইনডেক্স), scripts/clean_data.py, scripts/make_charts_v2.py, scripts/R/run_analysis.R (Task 8-এর স্যুটের পাশে আলাদা লঘু-যাচাই পথ)
- পেপারের ফিগার = charts_v2 (F1–F8 মূল, A1–A2 অ্যাপেন্ডিক্স); ক্লিনিং-মেথড Chapter 3-এ CLEANING_REPORT.md থেকে
- পরবর্তী: ইউজারের R-কনসোল আউটপুট এলে MISMATCH থাকলে ডায়াগনোসিস; আসল ডাটায় পুরো পাইপলাইন রিরান

## Task 10 — fixed two bugs found during independent chart/script re-verification (commit 99438f8)
- **#11** `scripts/R/figures.R`: C1's legend was covering the S09/S10 bars, and its leftmost
  x-axis label was edge-clipped; C2's `barplot()` was silently dropping 4 of 8 species
  labels. Both fixed (legend moved above the bars; C2 labels drawn explicitly via `axis()`).
  Re-ran `compare_r_py.py` after the fix: still 21/21 PASS (chart-only change).
- **#12** `scripts/R/run_analysis.R` (the standalone lightweight verification script) crashed
  on `rbind()` inside T16 before printing any output (column-count/type mismatch between
  the base stratum frame and the Mann-Whitney rows). Fixed; script now runs to completion
  (59/60 MATCH).
- **Open, not fixed this round:** re-running the now-working `run_analysis.R` surfaced its
  own genuine mismatch (check #47): T11 S01/Fishery-Ghat = 1416.25 (R) vs 1416.0 (Python).
  Root cause traced to this script's own `ppk()` helper, which recomputes price-per-kg from
  raw price+unit whenever `Sell_BDT_per_kg` is blank, without distinguishing a genuine blank
  from a deliberate K/D-flag exclusion. Only affects this standalone script's own T11 build —
  `run_all.R`'s pipeline (the one matched against Python) is unaffected.

---
Task ID: 14
Agent: Arena.ai agent (Chattogram real-data transition)
Task: সিমুলেটেড টেস্ট-ডাটা সরিয়ে আসল ফিল্ড ডাটা দিয়ে হলুদ ঘরে বসিয়ে একই পাইপলাইন চালাও। চট্টগ্রামের সাপেক্ষে করবে সব কাজ!

Work Log:
- সিমুলেটেড ডাটা সরানো: `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_Filled.xlsx` (199KB, v2 seed 20260911) → `04_data_filled/archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx` আর্কাইভ
- আসল ডাটার জন্য খালি টেমপ্লেট তৈরি: `03_data_entry_template/Marine_Fish_Marketing_Data_Entry (1).xlsx` (171KB, শুধু Obs_ID/Respondent_ID প্রিফিল, হলুদ ঘর ফাঁকা) → `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx`
- নতুন ডক: `04_data_filled/archive/README.md` (সিমুলেটেড আর্কাইভ নোট), `04_data_filled/README_REAL.md` (চট্টগ্রাম 6 বাজার: M1 Fishery Ghat ল্যান্ডিং, M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga — হলুদ ঘরে কীভাবে ভরতে হবে, যাচাই কমান্ড)
- Python পাইপলাইন আপডেট (চট্টগ্রাম রিয়েল-ডাটা প্রায়োরিটি):
  - `scripts/run_analysis.py`: `find_default_data()` এখন REAL*FILLED > REAL (non-EMPTY) > legacy Filled > EMPTY প্রায়োরিটি, archive/ বাদ, EMPTY হলে স্পষ্ট WARN; `load_data()`-এ empty-template guard (PO Market=0, A/B=0 → ValueError with Chattogram instructions)
  - `scripts/verify_filled.py`: argparse --data + find_default_data() ব্যবহার, archive/simulated টেস্টের নির্দেশনা
  - `scripts/review_audit.py`: DEFAULT খুঁজতে run_analysis.find_default_data() ব্যবহার
  - `scripts/fill_survey_data.py`: OUT এখন archive/SIMULATED_v2..., seed 20260911 (v2), REAL ফাইল থাকলে overwrite না করার guard
- R পাইপলাইন আপডেট:
  - `scripts/R/config.R`: repo root খোঁজা 04_data_filled/ বা scripts/R/run_all.R দিয়ে; INPUT_FILE R variable + Sys.getenv("INPUT_FILE") উভয়ই সম্মান; auto-detect প্রায়োরিটি REAL*FILLED > REAL (non-EMPTY) > legacy Filled > EMPTY, archive/ বাদ; শুধু EMPTY থাকলে স্পষ্ট warning (চট্টগ্রাম 6 বাজারের নামসহ)
  - `scripts/R/tables_descriptive.R`: empty-template guard মেসেজ আপডেট (archive/ + REAL_EMPTY → REAL_FILLED ফ্লো, চট্টগ্রাম 6 বাজার)
- যাচাই:
  - খালি REAL_EMPTY দিয়ে: `verify_filled.py` → 2 FAIL (Total interviews 0, Form_M 0) — expected; `run_analysis.py` → ValueError EMPTY TEMPLATE with Chattogram instructions — expected; R `run_all.R` → same [ERROR] — expected
  - আর্কাইভ সিমুলেটেড দিয়ে: `run_analysis.py --data archive/...` → DONE (T1-T11), `extend_analysis.py --data archive/...` → DONE (T12-T18), R `INPUT_FILE=archive/... Rscript run_all.R` → DONE, quality gates PASS (A+B+R=246.39=spread, PS 70.9%), `compare_r_py.py` → 21/21 PASS
- README.md আপডেট: উপরের ⚠️ সেকশন নতুন ট্রানজিশন নোট (REAL_EMPTY vs archive), চট্টগ্রাম 6 বাজারের তালিকা, আসল ডাটা বসানোর ধাপ, টেস্ট কমান্ড; আগের সিমুলেটেড ফলাফল সেকশন → আর্কাইভ রেফারেন্স

Stage Summary:
- সিমুলেটেড টেস্ট-ডাটা সক্রিয় পাথ থেকে সরানো হয়েছে, `04_data_filled/` এখন শুধু REAL_EMPTY (171KB) + README + archive/ (SIMULATED v2 199KB)
- আসল ফিল্ড ডাটা এন্ট্রির জন্য সম্পূর্ণ প্রস্তুত: হলুদ ঘরে চট্টগ্রামের 6 বাজারের (M1-M6) ডাটা বসিয়ে *_REAL_FILLED.xlsx নামে সেভ করলেই একই পাইপলাইন (verify 24/24 → run_analysis → extend → clean → charts_v2 → review_audit → R run_all) চলবে
- পাইপলাইন এখন চট্টগ্রামের সাপেক্ষে: landing markets M1/M6, 6 বাজার, 10 প্রজাতি, Pair_ID, K/D ফ্ল্যাগ — সবই চট্টগ্রাম ডিজাইনে
- পরবর্তী: ব্যবহারকারী F:/TermPaperNew-এ REAL_EMPTY ফাইল খুলে হলুদ ঘরে আসল ডাটা বসিয়ে *_REAL_FILLED.xlsx হিসেবে সেভ করে উপরের কমান্ডগুলো চালাবেন; GitHub push-এর জন্য PAT ব্যবহার
