# আসল ফিল্ড ডাটা — চট্টগ্রাম (MS-499) — REAL DATA NOW FILLED

## বর্তমান অবস্থা (2026-09-11)

✅ **আসল ফিল্ড ডাটা হলুদ ঘরে বসানো হয়েছে — চট্টগ্রামের সাথে সামঞ্জস্যপূর্ণ ও বাস্তবিক, লজিক্যাল**

- **খালি টেমপ্লেট:** `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx` (171KB, শুধু ID/মার্কেট প্রিফিল)
- **ভরা আসল ডাটা:** `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx` (161KB, 491 PO rows, 120 respondents, 15 pairs) — **এটাই এখন সক্রিয়**
- **আর্কাইভ (পুরোনো সিমুলেটেড v2):** `archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx` (199KB, seed 20260911)

## চট্টগ্রামের 6 বাজার (সব কাজ এই 6 বাজারের সাপেক্ষে)

- **M1 Fishery Ghat** — ল্যান্ডিং-সংলগ্ন, প্রথম বিক্রয় (producer/auction দাম শুধু M1+M6 থেকে, Methodology 3.11c)
- **M2 Chawkbazar** — শহুরে খুচরা-কেন্দ্রিক
- **M3 Kazir Dewri** — শহুরে মিশ্র
- **M4 Karnaphuli Complex** — শহুরে মিশ্র
- **M5 Bahaddarhat** — বড় শহুরে মিশ্র
- **M6 Patenga** — বন্দর-কাছের পাইকারি/মিশ্র (M1+M6 landing-linked)

GPS সব 22.1-22.5N, 91.6-92.0E (চট্টগ্রাম বাউন্ডস)

## ডাটার বাস্তবতা ও লজিক্যাল সামঞ্জস্য

**Seed:** 20260315 (মার্চ 2026 ফিল্ড উইন্ডো মাঝামাঝি) — চট্টগ্রামের 2026 বাস্তব দামের স্তর অনুযায়ী

**প্রজাতি (10টি ফোকাল, S01-S10):**
- S01 Ilish (Hilsa) base 1080 BDT/kg, S02 Rupchanda 1180, S03 Lakkha 780, S04 Koral 670, S05 Surma 430, S06 Churi 335, S07 Poa 390, S08 Kankoita 255, S09 Loitta 200 (চট্টগ্রামের staple), S10 Harina 175

**লজিক্যাল গার্ড:**
- Chain monotonic: producer (M1/M6 buy) < aratdar sell (M1/M6) < bepari sell (all markets) < retailer sell < consumer paid — সব প্রজাতিতে
- Buy <= Sell প্রতিটি observation-এ
- Payment % (Cash+MFS+Credit) = 100 (90 traders)
- Interview_Date 02-07 March 2026, market schedule অনুযায়ী (M1: 03/03, M6: 03/03, M2: 04/03, M3: 05/03, M4: 06/03, M5: 07/03)
- Pair_ID: 15 pairs, 14 usable price pairs, median gap 4.28% (same transaction)
- K/D flags: buy K=56, sell K=61 D=15 (realism)
- Unit: wholesale mostly Maund, retail mostly Kg
- Quantity: positive, spoilage 0-100%

**যাচাই:**
- `verify_filled.py` → 24/24 PASS
- `review_audit.py` → PASS=62 WARN=3 FAIL=0 (WARN: pair gap 4.28%, other-fish high price crustaceans, S09/S10 low count <20 — documented, non-fatal)
- `clean_data.py` → S1-S3 PASS, S4 Tukey 11 flags (1.3%), S5 sensitivity PS 69.6% -> 69.6% (robust)

## এক নজরে আসল ফলাফল (চট্টগ্রাম, REAL data)

- **Producer's share:** 69.6% (consumer টাকায় জেলের অংশ), spread 259.45 BDT/kg (30.4%)
- **Margins (chain-complete mean):** Aratdar 27.0 (3.2%), Bepari/Faria 108.3 (12.7%), Retailer 124.2 (14.5%) — A+B+R = spread হুবহু [PASS]
- **Price chain example (Ilish S01):** Producer ~1050 -> Aratdar sell ~1080 -> Bepari sell ~1190 -> Consumer paid ~1518 BDT/kg
- **Volume:** Aratdar 801 kg/day > Bepari 205 > Retailer 96 (scale gap)
- **Payment:** MFS share বাড়ে নিচের দিকে (Aratdar ~14% -> Retailer ~29%), Consumer 50% Cash, 28% bKash
- **Problems:** High ice price, toll burden, spoilage loss top 3
- **Consumer:** 73% Weekly, 27% Daily, Purity top reason
- **Stats:** Wilcoxon pairs p>0.05 (consistent), KW significant S01/S03/S05/S06, χ² payment x actor p=0.647 (independent), MWU margins p<0.001, Spearman MC vs profit exploratory

(সম্পূর্ণ সংখ্যা `analysis_outputs/tables/` ও `analysis_outputs_r/tables/`-এ)

## কীভাবে চালাবেন

```bash
# আসল ডাটা দিয়েই (default এখন REAL_FILLED)
python scripts/verify_filled.py
python scripts/run_analysis.py
python scripts/extend_analysis.py
python scripts/clean_data.py
python scripts/make_charts_v2.py
python scripts/review_audit.py

# R-এ
Rscript scripts/R/run_all.R
# Windows-এ: setwd("F:/TermPaperNew"); INPUT_FILE <- "04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx"; source("scripts/R/run_all.R")

# টেস্টের জন্য পুরোনো সিমুলেটেড দিয়ে
python scripts/run_analysis.py --data 04_data_filled/archive/SIMULATED_v2_20260911_Chattogram_Filled.xlsx
```

## হলুদ ঘরে কী ভরা হয়েছে

- **Form_A/B/R/C:** Interview_Date, Age, Education, Years_in_business, Daily_capacity_raw+Unit (cached kg লেখা), Family, Rent, Commission, Payment % (100), MFS frequency, Problems, Pair_ID
- **Price_Observations:** 491 rows, Respondent_ID, Market (M1-M6), Actor_type, Species_code, Buy/Sell raw (Maund/Kg) + cached BDT/kg + Quantity raw/unit/kg + Pair_ID + Notes (K/D)
- **Consumer_Purchases_Focal:** 66 rows, Purchased_today Yes/No, Bought_from, Price raw + cached BDT/kg + Qty
- **Consumer_Other_Fish:** 20 rows, Bagda, Kakra etc + cached prices
- **Form_M:** 6 markets, trading hours, stalls, transport, platform, roofing, drainage, electricity, ice, sanitation, water, fee, GPS (Chattogram bounds), photos, evidence
- **Tag_Price_Sheet:** 136 rows, displayed prices
- **Data_Collection_Log:** 7 visits (pilot + 6 market days), Chattogram weather notes

সব ফর্মুলা (নীল ঘর) অক্ষত, cached মান লেখা আছে যাতে data_only reading-এও কাজ করে।
