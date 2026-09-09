# DATA_DICTIONARY — ডাটা এন্ট্রি ওয়ার্কবুকের সম্পূর্ণ অভিধান

ওয়ার্কবুক: `04_data_filled/Marine_Fish_Marketing_Data_Entry_Chattogram_Filled.xlsx`
(টেমপ্লেটের খালি কপি: `03_data_entry_template/`)

**সাধারণ নিয়ম (সব শিটে প্রযোজ্য):**

- কলাম A খালি মার্জিন; ডাটা B কলাম থেকে শুরু। শিট-শিরোনাম ২ নম্বর সারিতে, **হেডার ৪ নম্বর সারিতে, ডাটা ৫ নম্বর সারি থেকে।**
- 🟨 **হলুদ ঘর** = আপনার লেখার জায়গা। 🟦 **নীল ঘর** = ফর্মুলা — কখনো টাচ করবেন না। ⬜ **ধূসর ঘর** = আগে থেকে বসানো আইডি/কোড — অবিকৃত রাখুন।
- তারিখ সবসময় দিন/মাস/বছর ফরম্যাটে (যেমন 05/03/2026)।
- **দাম-ফ্ল্যাগ:** সংখ্যা = দাম; `K` = আজ ওই মাছ কেনেনি/বেচেনি; `D` = উত্তর দিতে রাজি হয়নি; `0` = দাম শূন্য নয়, মান অজানা।
- **ইউনিট:** দাম কলামের পাশের Unit ঘরে `Maund` বা `Kg` — সংখ্যা দিলে ইউনিট বাধ্যতামূলক (QC চেক আছে)। ১ মণ = ৩৭.৩২ কেজি।
- **Respondent_ID স্কিম:** `মার্কেট-অভিনেতা-ক্রমিক`, যেমন `M1-A-01` = Fishery Ghat-এর ১ নম্বর আড়তদার। অভিনেতা-কোড: A=Aratdar, B=Bepari/Faria, R=Khuchra (খুচরা), C=Consumer।

---

## ১. Instructions
শিট-ম্যাপ, রঙের বিধি, K/D ফ্ল্যাগের ব্যাখ্যা — পড়ে নেওয়ার জন্য। কোনো ডাটা নেই।

## ২. Progress_Dashboard
বাজারভিত্তিক অগ্রগতি গণনা (স্বয়ংক্রিয় ফর্মুলা): যেসব সারিতে Interview_Date পূরণ হয়েছে সেগুলো গোনে। লক্ষ্য: ৬ বাজার × ২০ = ১২০। আপনি কিছু লিখবেন না।

## ৩. Data_Collection_Log
মাঠে যাওয়ার দিনলগি: তারিখ, বাজার, সংগ্রাহকের নাম, সেশনের শুরু-শেষ, আগের দিনের দাম ব্যবহার হলো কি না (Yes/No), কত জন ব্যবসায়ী/ভোক্তার ইন্টারভিউ, আবহাওয়া-নোট। C কলাম (Weekday) ফর্মুলা।

## ৪. Unit_Converter
১ মণ = ৩৭.৩২ কেজি — সব রূপান্তর-ফর্মুলার ভিত্তি।

## ৫. Codebook_Markets
| কোড | বাজার | চ্যানেল-অবস্থান |
|---|---|---|
| M1 | Fishery Ghat | ল্যান্ডিং-সংলগ্ন পাইকারি (প্রথম বিক্রয় দেখে) |
| M2 | Chawkbazar | শহুরে খুচরা-কেন্দ্রিক |
| M3 | Kazir Dewri | শহুরে মিশ্র |
| M4 | Karnaphuli Complex | শহুরে মিশ্র |
| M5 | Bahaddarhat | বড় শহুরে মিশ্র |
| M6 | Patenga | বন্দর-কাছের পাইকারি/মিশ্র |

## ৬. Codebook_Species
S01 Ilish (Hilsa shad, *Tenualosa ilisha*) · S02 Rupchanda (Silver pomfret) · S03 Lakkha (Indian salmon) · S04 Koral (Croaker) · S05 Surma · S06 Churi (Hairtail) · S07 Poa (Jewfish) · S08 Kankoita · S09 Loitta (Bombay duck) · S10 Harina — প্রতিটির ইংরেজি ও বৈজ্ঞানিক নাম শিটেই আছে।

## ৭. Form_A_Aratdar (আড়তদার, Form A — ৩০ জন)
| কলাম | মান |
|---|---|
| B–C | Respondent_ID, Market (পূর্বনির্ধারিত) |
| D | Interview_Date |
| E Age / F Education | বছর; Illiterate / Primary / Secondary / Higher_Secondary |
| G Years_in_business | ব্যবসার বয়স |
| H–I–J | Daily_capacity_raw + Unit (Maund/Kg/Piece) → J কেজিতে (ফর্মুলা) |
| K Family_members | পরিবারের সদস্য |
| L–M–N | Rent: Pay/Receive, টাকা, Monthly/Yearly |
| O–P | Commission_basis: Lot/Kg/**Percent** + হার |
| Q–R | বিদ্যুৎ বিল + কালান কীভাবে (Monthly/Yearly) |
| S–T | Workers_count, দৈনিক মজুরি (টাকা) |
| U–V | যন্ত্রপাতি/কুলার মেরামত খরচ + কালান |
| W–X | অন্য খরচের বিবরণ + টাকা |
| Y–Z–AA | পেমেন্ট %: Cash + MFS + Credit = **১০০** |
| AB | MFS ব্যবহার: Regular / Occasional / Never |
| AC–AE | সমস্যা ১–৩ (প্রশ্নপত্রের তালিকা থেকে) |
| AF | Pair_ID |
| AG | Notes |

## ৮. Form_B_Bepari_Faria (বেপারি ও ফড়িয়া, Form B — ৩০ জন)
A-এর সব সাধারণ কলাম + নিজস্ব: E Actor_subtype (Bepari/Faria), F Business_pattern (Year_round/Seasonal), N Source_location (মাছ কোথা থেকে আনে), O Supplier_category (Fisherman/Aratdar/Other), P–R যাত্রা ভাড়া ও সংখ্যা, S লোডিং-আনলোডিং খরচ, T–U বরফের ব্যবহার ও খরচ, V–W আড়তদারকে কমিশন (Percent_of_lot / BDT_per_lot), X পথে নষ্টের %, AC Credit_sales_share (Almost_all/Some/None)। Pair_ID = AG।

## ৯. Form_R_Khuchra (খুচরা বিক্রেতা, Form R — ৩০ জন)
দোকান/ভ্যান ভাড়া (দিন), বরফ খরচ (দিন), ধোয়া-পানি-অন্য (দিন), নষ্ট হওয়ার %, P Buys_from (Aratdar/Bepari/Faria/Wholesaler/Other), Q Sells_to (Household/Hawker/Hotel/Institutional/Other), V Sells_on_credit, Pair_ID = Z।

## ১০. Form_C_Consumer (ভোক্তা, Form C — ৩০ জন)
সাক্ষাৎকারের সময়, সম্মতি (Yes/No), G Visit_frequency (Daily/Weekly), H দুই কেনার মাঝের দিন, I Payment_method (Cash/bKash/Nagad_app/Credit), J বিক্রেতা বাছাইয়ের প্রধান কারণ (Price/Variety/Proximity/Purity/Familiar_shop/Other), K Pair_ID।

## ১১. Price_Observations (মূল দাম-শিট — ৪৬৩টি রেকর্ড)
প্রতি ব্যবসায়ী × প্রতি প্রজাতি এক সারি: Obs_ID (পূর্বনির্ধারিত), কার Respondent_ID, বাজার, Actor_type (Aratdar/Bepari_Faria/Khuchra), Species_code, **G কেনার দাম (raw) / H বেচার দাম (raw) / I Unit** → J/K ফর্মুলা BDT/কেজি বের করে; L–M–N ওই লটের পরিমাণ → কেজি; O Pair_ID; P Notes।
> চেইন-যুক্তি: আড়তদারের G (কেনা) = জেলে পায়; আড়তদারের H (বেচা) = বেপারি দেয়; বেপারির H = খুচরা বিক্রেতা দেয়; খুচরার H = ভোক্তা দেয়।

## ১২. Consumer_Purchases_Focal (ভোক্তার ফোকাল-প্রজাতি কেনা — ৬৯)
E Purchased_today (Yes/No), F Bought_from (Retailer/Hawker), G দাম raw + H Unit → I ফর্মুলা, J–L পরিমাণ।

## ১৩. Consumer_Other_Fish (অন্য মাছ — ১৯)
মাছের স্থানীয় নাম (মুক্ত লেখা), দাম, পরিমাণ, কোথায় কিনেছে।

## ১৪. Form_M_Market_Observation (৬ বাজারের প্রত্যক্ষ পর্যবেক্ষণ)
বাজারের ধরন (Wholesale/Retail/Mixed), ট্রেডিং আওয়ার, খুচরা দোকান সংখ্যা, H–P অবকাঠামো রেটিং (Transport: Good/Medium/Poor; Platform: Complete-Partial-None স্কেল; Electricity/Water: Regular/Irregular/None; Ice: Available/Not_available; Sanitation ইত্যাদি), Q Fee_arrangement (Aratdar/Committee/Mixed), S GPS।

## ১৫. Tag_Price_Sheet (দোকানের ট্যাগ/চার্ট-দাম — ১৩৬)
তারিখ, বাজার, দোকান নম্বর, সংগ্রাহকের ইনিশিয়াল, মাছের নাম, দাম raw + Unit → ফর্মুলা কেজিতে।

## ১৬. QC_Check (২৪টি স্বয়ংক্রিয় চেক)
পেমেন্ট-শতাংশের যোগফল ১০০, দাম-ইউনিট জোড়া, Price_Obs-এর সব ID যেন Form A/B/R-এ থাকে, ভোক্তা-কেনার ID যেন Form C-তে থাকে, Pair_ID দুই পক্ষে মিল, ছয় বাজারে Form M, মোট ইন্টারভিউ = ১২০ — সব "OK / TARGET MET / All matched / COMPLETE" দেখালে ডাটা জমা-দেওয়ার যোগ্য।

---

**Pair_ID যুক্তি:** একই লেনদেনের দুই পক্ষকে জোড়া দেয় (যেমন `PAIR-M1-01`: আড়তদারের বেচার দাম ↔ বেপারি/খুচরার কেনার দাম, একই প্রজাতি)। এতে Wilcoxon জোড়া-পরীক্ষা ও চেইন-সামঞ্জস্য যাচাই সম্ভব। এক বাজারে ২–৪টি জোড়া যথেষ্ট।
