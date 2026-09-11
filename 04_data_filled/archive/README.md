# Archive - Simulated Data

এই ফোল্ডারে সিমুলেটেড টেস্ট-ডাটা সংরক্ষিত আছে।

- `SIMULATED_v2_20260911_Chattogram_Filled.xlsx` = 2026-09-11 তারিখে seed 20260911 দিয়ে তৈরি v2 সিমুলেটেড ডাটা (MD5 2bd93fa6)
  - 6 বাজার (M1 Fishery Ghat, M2 Chawkbazar, M3 Kazir Dewri, M4 Karnaphuli Complex, M5 Bahaddarhat, M6 Patenga)
  - 120 জন (Aratdar 30, Bepari/Faria 30, Retailer 30, Consumer 30)
  - 492 Price Observations, 75 Focal Purchases
  - QC 24/24 PASS, review_audit 65 PASS / 0 FAIL
  - হেডলাইন: PS 68.9%, spread 234.88 BDT/kg, মার্জিন 23.15 / 93.78 / 117.95
- `SIMULATED_v1_20260302_Chattogram_Filled.xlsx` = সর্বপ্রথম টেমপ্লেট-ফিল (seed 20260302, MD5 b5952fbb) — ঐতিহাসিক রেফারেন্স; v2-এর লজিক্যাল-ফিক্সের আগের সংস্করণ

এগুলো আসল ফিল্ড ডাটা নয় — শুধু পাইপলাইন টেস্ট ও লেখার কাঠামো তৈরির জন্য।

আসল ফিল্ড ডাটা: `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL*.xlsx` ফাইলে হলুদ ঘরে বসে (বর্তমানে `*_REAL_FILLED.xlsx` সক্রিয়)।

পাইপলাইন টেস্ট করতে:
```
python scripts/run_analysis.py --data 04_data_filled/archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx
```

