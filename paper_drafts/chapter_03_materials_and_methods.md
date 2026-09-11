# CHAPTER 3 — MATERIALS AND METHODS

*This chapter implements Methodology V4 (`02_extracted_text/Methodology_v4_FIXED (references updated).txt`) and, in §3.7.5 and §3.12–3.13, documents the operational conventions that the analysis pipeline actually applies. Design tables are numbered 3.1–3.6 after that document; result tables in Chapter 4 are numbered 1–19 after the `T`-prefixed CSVs in `analysis_outputs/tables/`.*

---

## 3.1 Description of the study area

The study area covers the marine fish marketing network of the **Chattogram metropolitan region**, the principal coastal trade hub of Bangladesh through which a large share of the country's marine landings passes before reaching inland markets (DoF, 2024). Chattogram was selected because it combines all structural segments of the marine fish channel within one urban economy: beach landing points, wholesale assembly markets, intermediary trading yards (*arats*), and dense retail neighbourhoods.

**Six retail-and-wholesale fish markets constitute the empirical frame** (Table 3.1): Fishery Ghat and Patenga, both physically linked to a landing point so that first-sale prices can be observed directly; and Chawkbazar, Kazir Dewri, Karnaphuli Complex and Bahaddarhat, four retail markets distributed across old-town, central and newer residential areas so that consumer-side demand heterogeneity is represented. The final six were fixed using three criteria: **direct landing-point access, wholesale-channel coverage, and geographic spread across the city**. Unlike a purely convenience-based selection, four of the six (Fishery Ghat, Chawkbazar, Kazir Dewri, Karnaphuli Complex) repeat the sites of the author's earlier 2019 baseline study, which supports a decade-level comparison, while Bahaddarhat and Patenga extend the frame to a newer residential retail market and a second landing point.

**Table 3.1: Study markets, code prefixes and channel position**

| Market | Code | Channel position | Primary analytical contribution |
|---|---|---|---|
| Fishery Ghat | M1 | Landing-linked wholesale-cum-retail | First-sale (producer-side) price observations |
| Chawkbazar | M2 | Retail | Retail prices and trade volume quotes |
| Kazir Dewri | M3 | Retail | Retail prices and vendor practices |
| Karnaphuli Complex | M4 | Retail | Retail prices; comparability with the 2019 baseline |
| Bahaddarhat | M5 | Retail | Newer-generation retail turnover |
| Patenga | M6 | Landing-linked retail | Coast-side buy prices supporting producer-share estimation |

## 3.2 Study period and research design

The investigation follows a **descriptive-cum-analytical cross-sectional survey design** executed within a ten-day operational window: one preparation day including pilot testing, approximately five consecutive days of primary data collection distributed over different weekday market sessions, one reserve day for weather or availability contingencies, and the remaining days for data entry, verification and analysis. Field scheduling spreads each *arat* across different weekdays so that systematic differences between busy and slack trading sessions do not contaminate between-market price comparisons. The single-season snapshot character of this design is reported transparently as a limitation in §3.11, and temporal interpretation is restricted to the survey period. In the current implementation the pilot fell on **2 March 2026** and collection on **3–7 March 2026**.

The **unit of inquiry** is an individual market actor interviewed once. The **unit of price observation** is one respondent-by-species quote, expressed in Bangladeshi taka (BDT) per kilogram under fresh, ice-touched, whole-fish condition. Because respondents transact in heterogeneous lots, quantities quoted in maunds are converted using **1 maund = 37.32 kg**, and monetary values are standardised to per-kilogram terms during data preparation. Prices refer to transactions on the interview day, supplemented by the previous high-volume day when trade was thin, and the reference day is recorded on every form.

## 3.3 Target population and sampling procedure

### 3.3.1 Population definition

The target population comprises all market intermediaries handling the selected marine fish species at the six study *arats*, together with purchasing consumers at those *arats*. Three operator categories define the sampling strata:

- An **aratdar** operates the physical *arat* infrastructure, provides trading space plus services such as weighing facilities and auction coordination, and earns commission or lease income on transactions routed through his premises. He is a commission-earning facilitator, **not the owner of the fish** — a distinction carried through into the questionnaire design (§3.5) and into the margin definitions (§3.7.2).
- A **bepari/faria** is a mobile wholesaler who buys at landing points or upstream yards, transports consignments, and sells through *arats* either to retailers or to other wholesalers.
- A **khuchra** (retail) vendor sells directly to end-consumers from fixed stalls or vending spots inside the market.

### 3.3.2 Sample size determination

No complete census register of operators exists in these informal markets, so a planning benchmark is first obtained from Cochran's (1977) single-proportion formula, adopting a 95 % confidence level (Z = 1.96), maximum response variance (p = q = 0.5), and an eight percent permissible error (relaxed from the conventional five percent given fixed field resources):

> n₀ = Z² p q / e² = (1.96)²(0.5)(0.5) / (0.08)² ≈ **150** …………… (3.1)

As a robustness check, Yamane's (1967) finite-population formula, applied to an illustrative frame of N = 1,000 operators that plausibly exceeds the number of active intermediaries trading across six *arats* during any session, with the same e = 0.08:

> n = N / (1 + N e²) = 1,000 / (1 + 1,000 × 0.0064) ≈ **135** ………… (3.2)

Both benchmarks (n₀ ≈ 150; n ≈ 135) set an upper planning ceiling. It should be noted that Cochran's formula is designed for estimating a single population proportion, whereas the study's actual inferential targets are continuous price and margin comparisons (§3.8), for which a formal power calculation against an expected effect size would be the methodologically ideal approach. In the absence of a reliable prior effect-size estimate for this market, the proportion-based ceiling is used only as a planning bound, and the field target actually applied is fixed independently below, **on resource and design grounds rather than on the ceiling itself**.

Given the ten-day field window across six markets, the applied field target is **120 valid interviews**, allocated equally across the three trader strata (5 aratdars + 5 beparis/farias + 5 khuchra retailers = 15 traders per market) plus 5 exit-intercepted consumers per market, across six markets (Table 3.3). This is below the Cochran ceiling of 150 but is deliberately chosen over an unequal, retail-heavy split so that **each trader stratum carries equal analytical weight** in the between-stratum comparisons of §3.8. The trade-off — fewer total interviews in exchange for balanced strata — is stated here explicitly rather than left implicit.

### 3.3.3 Allocation and selection of respondents

**Table 3.3: Quota allocation of 120 respondents across the six markets**

| Market | Aratdar | Bepari/Faria | Khuchra retailer | Trader subtotal | Consumer | Total |
|---|---|---|---|---|---|---|
| M1 Fishery Ghat | 5 | 5 | 5 | 15 | 5 | 20 |
| M2 Chawkbazar | 5 | 5 | 5 | 15 | 5 | 20 |
| M3 Kazir Dewri | 5 | 5 | 5 | 15 | 5 | 20 |
| M4 Karnaphuli Complex | 5 | 5 | 5 | 15 | 5 | 20 |
| M5 Bahaddarhat | 5 | 5 | 5 | 15 | 5 | 20 |
| M6 Patenga | 5 | 5 | 5 | 15 | 5 | 20 |
| **Total** | **30** | **30** | **30** | **90** | **30** | **120** |

Markets themselves constitute the primary stratum and were purposively nominated on the criteria in §3.1, because informal operator registers cannot provide an equal-probability frame. Within each selected market, aratdar and bepari/faria participants are drawn purposively among operators active during the survey session, prioritising informants handling the focal species, while khuchra vendors are taken successively along the market rows until the quota fills. Consumer observations use **systematic exit interception** of purchasers leaving the market with visible fish purchases. This **stratified purposive-cum-quota procedure is disclosed honestly rather than presented as probability sampling**, and inferential results are therefore interpreted as analytical generalisation within the studied system rather than statistical generalisation to a wider population.

### 3.3.4 Price matching protocol

To validate quoted margins against actually traded prices, each trader interview records the respondent's principal supply linkage — from whom the respondent purchased and to whom the respondent sold during the session. Whenever a retailer reports purchasing a surveyed species on the interview day and the corresponding seller is also interviewed, the transaction receives a common **pair identifier** linking buyer and seller forms. Matched pairs enable Wilcoxon signed-rank validation of self-reported buy-versus-sell consistency and add an independent quality screen on stated margins. Given the compressed schedule, the number of genuinely matched pairs is expected to be modest (realistically a handful per market); this test should therefore be read as a **diagnostic quality check rather than a fully powered hypothesis test**, and the achieved number of matched pairs is reported alongside the result (Table 12b).

## 3.4 Selection of fish species

Ten commercially important marine species form the analytical core of the study, selected against four criteria: **persistent presence** across all six survey *arats* during preliminary reconnaissance; **substantial share** in daily trade volume or value at Chattogram retail outlets; **coverage of high-, medium- and low-price tiers** so that margin behaviour can be compared across market segments; and **documented importance** in national marine fisheries statistics. Scientific names throughout Table 3.4 follow FishBase (2026).

**Table 3.4: 10 marine fish species selected for this study**

| Code | Local name | English common name | Scientific name | Tier |
|---|---|---|---|---|
| S01 | Ilish | Hilsa shad | *Tenualosa ilisha* | High |
| S02 | Rupchanda | Silver pomfret | *Pampus argenteus* | High |
| S03 | Lakkha | Indian salmon (four-finger threadfin) | *Eleutheronema tetradactylum* | High |
| S04 | Koral/Kurl | Asian sea bass | *Lates calcarifer* | High |
| S05 | Surma | Indian mackerel | *Rastrelliger kanagurta* | Medium |
| S06 | Churi | Largehead ribbonfish | *Trichiurus lepturus* | Medium |
| S07 | Poa | Pama croaker | *Otolithoides pama* | Medium |
| S08 | Kankoita | Thorny/Indian anchovy | *Stolephorus indicus* | Low |
| S09 | Loitta | Bombay duck | *Harpadon nehereus* | Low |
| S10 | Harina | Chacunda gizzard shad | *Anodontostoma chacunda* | Low |

Two taxonomic corrections were applied to the initial candidate list. Species **S03** (previously Bagda chingri / giant tiger prawn, *Penaeus monodon*) has been replaced with **Lakkha** (*Eleutheronema tetradactylum*), a high-value marine finfish, so that all ten entries are true fish and consistent with the study's title and scope; prawn is a crustacean and its inclusion in a "marine fish species" study would be a taxonomic inconsistency. Species **S08** is narrowed to *Stolephorus indicus* specifically, rather than a mixed anchovy genus group, so that each code maps to one identifiable species for per-species price analysis.

Should the pilot round reveal that any species is scarcely transacted at the study markets, a **pre-specified substitution rule** applies: the affected species is replaced by the closest-tier available alternative observed during the pilot, the change and its justification are recorded with date and supervisor acknowledgement before large-scale collection begins, and no further substitutions occur thereafter so that the instrument remains stable throughout the survey.

## 3.5 Instruments and data collection procedure

Data were collected through **pre-structured, interviewer-administered instruments** prepared in Bangla to guarantee conceptual equivalence with respondents, accompanied by an English analytical specification for the researcher. The instrument battery comprises five coordinated forms whose items map one-to-one onto the variables defined in §3.6; nothing outside these fields was collected, in line with the minimised-data principle adopted for this study. Each physical Bangla form carries its Form ID (A, B, R, M or C) printed in its header so that field forms, data entry and this methodology stay unambiguously cross-referenced.

**Trader questionnaires (Form A – Aratdar; Form B – Bepari/Faria; Form R – Khuchra retailer).** A shared structural template underlies all three, with actor-specific filtering. Common modules capture basic demographics (age, education, duration in marine fish trade), principal supply linkage, quantities handled per day in kilograms, buy-and-sell quotations for each focal species, mode of payment (cash, bKash/Nagad, credit), and actor-specific cost modules.

On **Form A**, the price-grid columns record the *auction-clearing prices the aratdar facilitates* — what the fisherman receives and what the bepari pays — as **pass-through prices, not the aratdar's own trading margin**. His income is captured separately as commission/lease income in the cost module, so that his margin is not double-counted once as a price spread and again as commission. This design decision is what makes the aratdar's margin in Tables 3 and 10 a genuine auction spread rather than an artefact.

**Form B** adds transport fares, icing quantity and expenditure, commission paid to aratdars, and transit damage percentages. **Form R** covers stall rent, icing cost, wash-water and tool expenses, self-reported spoilage percentages, and customer composition.

**Market observation checklist (Form M).** One checklist per market, completed by direct physical observation of twelve infrastructure characteristics — market type and hours, retail stall count, transport access, platform condition, roofing, drainage, electricity, ice availability, sanitation, water supply, and lease/toll arrangement — each marked with its evidence source (direct observation vs. verbal confirmation), plus GPS coordinates and photo references.

**Consumer exit slip (Form C).** Five purchasers leaving each market complete a two-to-three-minute intercept slip recording focal-species purchases with price paid, quantities, any other fish bought, and payment mode — an **independent consumer-side check on retailer sell prices**.

**Supplementary tag-price sheet (optional).** Where field time permits, posted or spoken display prices of all fish observable at each market are transcribed once per visit, at zero interview burden, enriching the descriptive appendix without entering the formal hypothesis tests.

### 3.5.1 Interviewing schedule and pilot

Interviews are conducted during the morning trading window, when wholesale arrivals and early transactions concentrate, and extend into late-morning retail peaks at retail yards. Fieldwork opens with a **one-day pilot** at one market on approximately five respondents covering every stratum: interviewer phrasing, skip-pattern integrity, species recognisability, maund-to-kilogram conversions and response times are checked, after which only supervisor-approved corrections are applied. Questionnaire and species-list versions are **frozen** before systematic collection begins.

## 3.6 Variables and their measurement

**Table 3.5: Variable definitions, instrumentation and analytical roles**

| Variable | Instrument source | Scale / unit | Analytical role |
|---|---|---|---|
| Respondent identifiers | Header block, all forms | Codes M1–M6, actor class, serial | Stratification and linkage keys |
| Age; education; trade experience | Trader socio-economics module | Years; grade; years | Actor profile descriptive statistics |
| Quantity handled | Trader trade module | kg/day (maund converted) | Volume weights; cost normalisation |
| Buy price by species | Species grid (traders) | BDT/kg | Producer-side price proxy (P<sub>p</sub>) |
| Sell price by species | Species grid (traders); Form C | BDT/kg | Retail price anchor (P<sub>r</sub>); margin construction |
| Pair identifier | Link-tracing fields | Match code | Wilcoxon signed-rank validation sample |
| Marketing costs | Actor-specific cost modules | BDT + frequency codes | Per-kilogram marketing cost (MC) |
| Commission | Form A, B modules | % per lot or BDT/kg | Channel margin decomposition |
| Damage / spoilage | Self-reported % of lot value | % | Loss adjustment; robustness note |
| Payment mode mix | Payment module, all forms | Cash / MFS / credit | Chi-square test of mode shares |
| Market facilities | Form M observation | Graded checklist items | Contextual profile of arats |
| Tag prices (optional) | Optional sheet, observed | BDT/kg, all species | Appendix descriptive diversity table |

## 3.7 Analytical framework for marketing performance

### 3.7.1 Marketing cost

For every trader *i* in stratum *k*, total marketing cost per kilogram is the sum of itemised cash expenses (rent/toll, electricity where applicable, transport including loading/unloading, wages, commission paid, icing, tools and washing water, and other sundries), normalised to the kilogram basis by quantity handled:

> MC<sub>ki</sub> = ( Σ c<sub>ri</sub> ) / Q<sub>ki</sub> , r = 1 … R …………….. (3.3)

where c<sub>ri</sub> = expense on cost item *r* by respondent *i*; Q<sub>ki</sub> = quantity handled per day by respondent *i* in stratum *k*; R = number of applicable cost items.

This is applied to **all three strata**, not to retailers alone as in much of the published literature, because the wholesale tiers are where the largest per-kilogram costs fall and omitting them would bias the net-margin and efficiency indicators of §3.7.3–3.7.4.

### 3.7.2 Segment margins and profit

The absolute margin earned at any channel segment equals the spread between the respondent's recorded selling and buying prices for the same species-day quote, and segment profit deducts marketing cost from that spread:

> M<sub>ki</sub> = P<sub>si</sub> − P<sub>bi</sub> …………………… (3.4)
> π<sub>ki</sub> = M<sub>ki</sub> − MC<sub>ki</sub> ………………… (3.5)

where P<sub>si</sub> and P<sub>bi</sub> = selling and buying prices per kilogram quoted by respondent *i*; π<sub>ki</sub> = net profit of the segment operator per kilogram.

### 3.7.3 Channel-level indicators

Following the marketing-margin framework of Kohls and Uhl (1980), four standard chain-level indicators are computed per species and market combination, using mean prices over valid observations, where P<sub>r</sub> = mean retail price per kilogram (validated by consumer slips) and P<sub>p</sub> = mean producer-side, first-sale price per kilogram:

> Price spread = P<sub>r</sub> − P<sub>p</sub> ………………….. (3.6)
> GMM% = [ (P<sub>r</sub> − P<sub>p</sub>) / P<sub>r</sub> ] × 100 ……………… (3.7)
> NMM% = [ (P<sub>r</sub> − P<sub>p</sub> − ΣMC) / P<sub>r</sub> ] × 100 ………… (3.8)
> PS% = ( P<sub>p</sub> / P<sub>r</sub> ) × 100 ………………… (3.9)

where ΣMC = summed per-kilogram marketing costs of all surveyed segments in the chain; GMM% = gross marketing margin percentage; NMM% = net marketing margin percentage; PS% = producer's share of the consumer's taka.

### 3.7.4 Marketing efficiency

Operational efficiency follows Shepherd's (1965) ratio of output value to input costs, applied on a per-kilogram chain basis; values above unity indicate that more of the final price remains as product value than is consumed by marketing services:

> ME = P<sub>r</sub> / ( ΣMC + ΣM ) ……………… (3.10)

where ME = Shepherd-type efficiency index; ΣM = summed segment margins along the chain. As a complementary **producer-referenced** measure, following Acharya and Agarwal's (1987) convention that efficiency assessment should also be judged from the producer's side, the same ratio is recomputed with P<sub>p</sub> in place of P<sub>r</sub>. The two versions are **reported side by side rather than treated as interchangeable**, since they answer different questions: value delivered to the consumer per unit cost, versus value retained by the producer per unit cost.

### 3.7.5 Operational conventions for constructing the price chain

Equations 3.6–3.10 require four conventions that the source document states in principle (§3.11c) but which must be made operational before they can be computed reproducibly. All four are fixed in the analysis scripts and are stated here because they materially affect every headline figure.

**(a) Producer price is taken from the landing-linked markets only.** P<sub>p</sub> is the Form A purchase quote at **M1 Fishery Ghat and M6 Patenga**, where an aratdar's buy price is the net auction price paid to the fisherman. Aratdar buy quotes at the four city markets (M2–M5) are *downstream* wholesale purchases, not first sales, and are excluded from P<sub>p</sub> by construction. This is the proxy status acknowledged in §3.11c, carried explicitly into every producer-share figure.

**(b) The retail anchor is the price consumers actually paid.** P<sub>r</sub> is the **Form C consumer-paid price**, not the retailer's own selling quote. The retailer's own quote is retained in Table 3 alongside it, because the gap between the two is itself informative (Chapter 4, §4.3), but it is not used to compute margins. Anchoring on the realised consumer price is what makes the three segment margins telescope to the spread and makes PS% + GMM% = 100 exactly.

**(c) Chain completeness is a joint test.** A species enters the pooled chain figures only if it has valid quotations at all four chain levels **and** at least **three consumer-purchase observations** (MIN_CONS = 3) **and** appears in at least **three markets** (MIN_MARKETS = 3). The market-coverage floor is applied as well as the consumer-slip floor so that a species can never be flagged descriptive-only under the §3.8 rule while still contributing to the pooled estimate. Species failing the test are reported descriptively with the reason recorded in the `Reporting_status` column of Table 3.

**(d) Costs are converted to a common daily basis and physical losses are valued.** Mixed-frequency expense items are converted to BDT per trading day using **26 trading days per month and 312 per year**, then divided by the respondent's own throughput (eq. 3.3). Physical losses — retailer spoilage and bepari transit damage — are valued at the respondent's own mean purchase price, because an unsold or damaged kilogram is a genuine cost and eq. 3.5 defines profit as margin minus cost. Excluding them would overstate segment profit by the value of the fish that never sold.

## 3.8 Statistical analysis

Analysis runs in **R statistical software** (R Core Team, 2025) with an annotated script retained for full reproducibility (`scripts/R/MS499_full_analysis.R`), cross-checked against an independent Python implementation (`scripts/run_analysis.py`, `scripts/extend_analysis.py`) that reproduces the same tables cell-for-cell. Price and margin distributions in informal fish markets rarely satisfy normality or homogeneity of variance — confirmed here by **Shapiro–Wilk screening on the pooled series before any test is applied** (Table 18) — so the inferential battery relies on distribution-free procedures throughout, evaluated two-sidedly at the five percent significance level. Table 3.6 maps each research question onto its variable set and designated test, **fixing the analytic plan before data inspection**.

**Table 3.6: Analytical questions mapped to statistical tests and decision rules (α = 0.05)**

| Research question | Data | Test statistic | Decision rule |
|---|---|---|---|
| Do prices of the same species differ across markets? | Species-wise price observations by market (n ≥ 5 cells) | Kruskal–Wallis H (Kruskal & Wallis, 1952); post-hoc Dunn (Dunn, 1964) with Holm adjustment | Reject H₀ when p < 0.05 |
| Do margins differ across trader categories? | Segment margins by stratum | Mann–Whitney U per pair of strata | Reject H₀ when p < 0.05 |
| Are self-reported buy-sell quotes internally consistent? | Matched pair identifiers | Wilcoxon signed-rank on paired differences | Non-significance corroborates consistency |
| Does payment-mode adoption differ across actor types? | Mode mixes by actor class | Chi-square; Fisher fallback for sparse cells | Reject H₀ when p < 0.05 |
| Is marketing cost associated with segment profit? | Per-kilogram MC versus π pairs | Spearman rank correlation | Sign and strength of rho, 95 % CI |
| Normality screening preceding all tests | Pooled price and margin series | Shapiro–Wilk W | p > 0.05 needed to justify parametric alternatives; else nonparametric used |

Multiple pairwise contrasts following significant omnibus tests use **Holm's (1979) step-down familywise error control**. Because species compositions differ across respondents, **inter-market comparisons are always executed within a single species, never pooled across species**. Species appearing at fewer than three markets with fewer than five observations per cell are reported descriptively only.

> **Exploratory-threshold disclosure.** The design allocates five respondents per stratum per market, so **no species can reach five quotes per market cell for every market, and no species meets the pre-registered n ≥ 5 rule**. All inter-market tests are therefore executed and reported at an explicitly labelled **exploratory threshold (n ≥ 3 in ≥ 3 markets)**, flagged as such in Table 14, and read as descriptive of this sample rather than as confirmatory inference. This is a design limitation rather than an analytical choice (§3.11) and is restated in Chapters 4 and 5.

## 3.9 Data quality assurance

Interviewers receive one structured training session covering consent administration, species coding, maund-to-kilogram conversion, skip patterns and the pair-linking rule, immediately followed by the pilot round (§3.5.1). Completed forms are checked **same-day against arithmetic range constraints**, and daily field debriefs resolve anomalies while memory remains fresh. Approximately **ten percent of trader respondents** are re-approached through short callback verification of key fields (quantity handled, commission rates).

During entry, respondent identifiers are screened for duplication, pair identifiers are reconciled across linked forms, and **implausible entries are flagged rather than deleted** so that exclusion decisions remain documented and traceable. Buy-price records that traders decline to disclose retain their analytical role under an explicitly flagged proxy convention approved before analysis.

Beyond the field procedures, three **automated gates** are checked at the end of every analysis run: the three segment margins must telescope to the total spread; the producer's share and the spread percentage must sum to 100; and the pooled producer's share in Table 3 must equal that in Table 10. An independent audit script (`scripts/review_audit.py`) re-derives 65 checks from the workbook without reference to the analysis outputs.

**Handling of non-response flags.** The workbook uses two-letter flags on raw price cells: **K** = business not operating on the interview day (a *valid skip* — the respondent is retained in all counts but that day's prices are undefined) and **D** = refused / do not know (*item non-response* — excluded from the affected statistic and reported in `missing_report.csv`). Neither is imputed; flagged cells simply reduce the *n* of the affected statistic, and *n* is disclosed in every table.

## 3.10 Ethical considerations

Participation is voluntary and based on **verbal informed consent**:

1. The interviewer reads a standard statement in Bangla explaining the study purpose, the academic-only use of information, anonymity protections, and the right to decline any question or withdraw entirely without consequence.
2. Personal identifiers are replaced by coded IDs at collection time; contact details are not recorded on forms, and electronic files reside exclusively on a password-protected device accessible to the researcher.
3. Reported results aggregate to group level so that no individual operator can be identified from published tables or figures.
4. The protocol follows the academic norms of the departmental term-paper course, and supervisor endorsement of instruments constitutes the institutional review of the survey plan.

## 3.11 Limitations of the methodology

Five limitations bound the interpretation of findings.

**(a)** The **cross-sectional design captures one seasonal episode**. Margins in marine markets vary intra-week and seasonally, so temporal extrapolation beyond the survey window is avoided, and any seasonal claim in the discussion should be sourced from prior published data rather than presented as a within-study finding.

**(b)** **Purposive nomination of markets combined with quota-convenience selection within strata precludes design-based population inference.** Results generalise analytically to comparable channel settings rather than statistically to all Chattogram operators.

**(c)** **Producer-side prices are proxied from first-sale quotations at landing-linked markets rather than from boat-level fisher interviews**, and this proxy status is carried explicitly into the producer-share calculations (operationalised in §3.7.5a).

**(d)** **Cost and loss variables rest partly on respondent recall and self-assessment**, especially spoilage percentages. Day-referencing of quantities and percentage-format questioning mitigate but cannot eliminate recall error.

**(e)** **The field sample size (120) was fixed on resource and stratum-balance grounds** rather than derived from a power calculation matched to the study's actual continuous-variable tests; the Cochran/Yamane figures in §3.3.2 should be read as a proportion-based planning ceiling, not as a formal power guarantee for the Kruskal–Wallis/Mann–Whitney comparisons of §3.8.

Two further limitations are specific to the implementation and are disclosed here rather than at the results stage. **(f)** The **pre-registered n ≥ 5 per-cell rule of §3.8 is unreachable by design** (§3.8 exploratory-threshold disclosure), so all inter-market inference is exploratory. **(g)** The **survey window opens at the start of the annual hilsa conservation ban** (Chapter 1, §1.7); the ban is not a measured variable in this study, and Ilish results should be read with that context in mind.

## 3.12 Data management, processing and software

**Entry and storage.** Data are entered into a structured Excel workbook (`04_data_filled/`) whose 16 sheets mirror the five instruments plus derived and QC sheets. Cell colour encodes editability: **yellow** cells receive raw field entries, **grey** ID columns are fixed, and **blue** cells hold derived values. A dedicated recalculation script (`scripts/qc_recalc.py`) reimplements the derived columns and all 24 QC checks in Python and writes the results as **literal values**, so the workbook reads identically in Excel, in pandas and in R without requiring a spreadsheet engine to recalculate it. Without that step the QC cells would be empty and the verification gate would be checking nothing.

**Verification.** `scripts/verify_filled.py` applies the 24-check QC gate (quota balance, ID well-formedness, date range, arithmetic constraints, payment-share sums, sell ≥ buy) and must pass 24/24 before any analysis is run.

**Cleaning.** `scripts/clean_data.py` executes five documented stages without modifying the source workbook: **S1** structural validation (IDs, quotas, dates, duplicates); **S2** missing-data audit distinguishing K from D; **S3** range and logic checks (age 18–80, experience ≤ age − 12, strictly positive prices and quantities, spoilage 0–100 %, payment shares summing to 100, sell ≥ buy); **S4** Tukey outlier screening (1.5 × IQR) computed separately for each species × actor × price-side group with at least eight numeric quotes; **S5** sensitivity re-estimation of the headline chain with flagged outliers excluded. In the current dataset **10 of the numeric price cells (1.0 %) fall outside their fences**. Consistent with common practice for genuinely right-skewed fish-market price data with small per-cell samples, **flagged values are retained in the baseline analysis and listed in `outlier_flags.csv`**; a difference of about two percentage points or less in the producer share between the baseline and the outlier-excluded chain is interpreted as robust to outliers.

**Analysis software.** Descriptive tables (Tables 1–11, 2b, 4b, 19) are produced by `scripts/run_analysis.py` and the inferential battery (Tables 12–18) by `scripts/extend_analysis.py`, both in **Python 3** with pandas, NumPy, SciPy and openpyxl. The full set is independently reproduced in **R** (`scripts/R/MS499_full_analysis.R`, base R plus `readxl` and `openxlsx` only, so that it runs on a stock local R installation), and the two engines are compared cell-for-cell by `scripts/compare_r_py.py`. Charts are generated by `scripts/make_charts_v2.py`. Every script is deterministic and re-runnable; the complete command sequence is given in `scripts/README.md`.

## 3.13 Implementation status and data provenance

The design described in §3.1–3.11 is the design **as specified and as implemented in the pipeline**. The workbook currently analysed, however, is a **synthetic realisation** of that design rather than collected field data.

`04_data_filled/SYNTHETIC_v3_20260315_Chattogram_Filled.xlsx` was generated by `scripts/generate_synthetic_data.py` from `random.Random(20260315)`. It populates all 16 sheets with the full structure the instruments specify — 120 respondents (30 per stratum) across the six markets, ten focal species, 491 price-observation rows, 15 linked buyer–seller pairs, the complete cost modules and the Form M checklists — and it reproduces the market, species, unit and flag conventions of §3.2–3.7 exactly, including the 1 maund = 37.32 kg conversion and the K/D flags. **Every element of §3.1–3.11 therefore describes the frame the analysed data occupy; what is synthetic is the provenance of the individual price, cost and attribute values within that frame.**

This is stated rather than obscured because it governs what may be claimed. The design, the instruments, the quality gate, the operational conventions of §3.7.5, the statistical plan of §3.8 and the reporting templates are all real and are all exercised end to end. The **numbers** in Chapter 4 are properties of the generator, not of Chattogram's markets, and no figure derived from them may be cited as an empirical finding — a point restated in the provenance note to Chapter 4 and developed in its §4.11.

Switching to real field data requires no change to any method in this chapter. The blank template `Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_EMPTY.xlsx` holds the yellow input cells empty with grey IDs and blue derived columns intact; the analyst fills the yellow cells only, runs `verify_filled.py` (24/24), then `run_analysis.py`, `extend_analysis.py`, `clean_data.py`, `make_charts_v2.py`, `review_audit.py` and `scripts/R/MS499_full_analysis.R`, and every table regenerates. Chapter 4's structure, caveats and reconciliation logic carry over unchanged; its numbers are replaced.

---

### References cited in this chapter

Acharya, S. S., & Agarwal, N. L. (1987). *Agricultural marketing in India*. Oxford & IBH Publishing.

Cochran, W. G. (1977). *Sampling techniques* (3rd ed.). John Wiley & Sons.

Department of Fisheries (DoF). (2024). *Yearbook of fisheries statistics of Bangladesh 2023–24* (Vol. 41). Fisheries Resources Survey System, Ministry of Fisheries and Livestock, Government of Bangladesh.

Dunn, O. J. (1964). Multiple comparisons using rank sums. *Technometrics, 6*(3), 241–252.

FishBase. (2026). *FishBase world database of fishes*. https://www.fishbase.se

Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics, 6*(2), 65–70.

Kohls, R. L., & Uhl, J. N. (1980). *Marketing of agricultural products*. Macmillan.

Kruskal, W. H., & Wallis, W. A. (1952). Use of ranks in one-criterion variance analysis. *The Annals of Mathematical Statistics, 23*(3), 525–540.

R Core Team. (2025). *R: A language and environment for statistical computing*. R Foundation for Statistical Computing. https://www.R-project.org/

Shepherd, G. S. (1965). *Marketing farm products: Economic analysis* (6th ed.). Iowa State University Press.

Yamane, T. (1967). *Statistics: An introductory analysis* (2nd ed.). Harper & Row.
