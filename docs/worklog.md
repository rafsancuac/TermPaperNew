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
