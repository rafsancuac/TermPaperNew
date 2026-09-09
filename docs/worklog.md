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
