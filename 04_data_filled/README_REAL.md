# আসল ফিল্ড ডাটা — চট্টগ্রাম (MS-499)

## ফাইল
- `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx` = খালি টেমপ্লেট, শুধু ID/মার্কেট প্রিফিল, হলুদ ঘর ফাঁকা — এখানেই আসল ডাটা বসবে
- ভরা হলে নাম বদলে `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx` করুন (বা যেকোনো নাম, config.R স্বয়ংক্রিয়ভাবে REAL ফাইলকে অগ্রাধিকার দেয়)

## চট্টগ্রামের 6 বাজার
- M1 Fishery Ghat (ল্যান্ডিং-সংলগ্ন, প্রথম বিক্রয়)
- M2 Chawkbazar (শহুরে খুচরা)
- M3 Kazir Dewri (শহুরে মিশ্র)
- M4 Karnaphuli Complex (শহুরে মিশ্র)
- M5 Bahaddarhat (বড় শহুরে মিশ্র)
- M6 Patenga (বন্দর-কাছের পাইকারি/মিশ্র)

## কীভাবে ভরবেন
1. Excel-এ REAL_EMPTY ফাইল খুলুন
2. শুধু 🟨 হলুদ ঘরে লিখুন (ধূসর ID, নীল ফর্মুলা ছোঁবেন না)
3. দাম লিখলে Unit (Maund/Kg) অবশ্যই দিন; না কিনলে K, উত্তর দিতে রাজি না হলে D
4. Form A/B/R-এ Cash+MFS+Credit = 100 রাখুন
5. Interview_Date 02-07 March 2026-এর মধ্যে
6. Pair_ID দিয়ে কেনা-বেচা জোড়া মিলান

## যাচাই ও বিশ্লেষণ
```bash
python scripts/verify_filled.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/run_analysis.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/extend_analysis.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/clean_data.py --data 04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx
python scripts/make_charts_v2.py
python scripts/review_audit.py
```

R-এ:
```r
setwd("path/to/TermPaperNew")
INPUT_FILE <- "04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx"
source("scripts/R/run_all.R")
```

## সিমুলেটেড ডাটা কোথায়?
`04_data_filled/archive/` ফোল্ডারে আর্কাইভ করা আছে — টেস্টের জন্য ব্যবহার করতে পারেন, কিন্তু চূড়ান্ত পেপারে আসল ডাটা ব্যবহার করুন।
