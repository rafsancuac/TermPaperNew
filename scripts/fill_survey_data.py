#!/usr/bin/env python3
"""
Fill Marine_Fish_Marketing_Data_Entry template with realistic simulated
Chattogram survey data (MS-499, Methodology V4, March 2026 window).

v2 (2026-09-11) -- correctness release. Fixes over v1:
 1. Consumer interview times drawn INSIDE each market's visit session
    (v1 had 12/30 consumers timestamped outside the logged session).
 2. Market-day price anchors: one wholesale anchor W and one retail anchor
    RC per market x species; every actor's quote derives from the same
    anchor (law of one price within a market-day; consumers pay the same
    retail level the retailers of that market quote, minus small haggle).
 3. Active-species selection is an UNBIASED random sample (v1 truncated
    to the first five species in code order, starving S06-S10 at landing
    markets: S09 had only 4 aratdar quotes, S10 none at all).
 4. Availability / demand raised for S08, S10 and hard coverage guards:
    every species gets >=3 bought-today consumer rows, >=2 landing aratdar
    buy+sell quotes, >=20 Price_Observation rows and retailer sell quotes
    in >=3 markets, so T3/T10 are chain-complete for all ten species.
 5. Declined buy prices now use flag "D" (v1 wrongly wrote "K", which
    means "not handled today" -- contradicting the numeric sell price
    on the same row).
 6. Pair species protected from K/D/not-yet-sold flags on both sides,
    so every matched pair is complete (Wilcoxon n improves).
 7. Bepari / retailer buy prices depend on the DECLARED source
    (Fisherman vs Aratdar vs Faria vs Other), and M2-M5 retailers no
    longer claim "Fisherman" as source (no landing at retail markets).
 8. Ilish base calibrated to 1120 BDT/kg (lean-season March 2026 level;
    jatka conservation window keeps marine landings thin).

Rules honoured (unchanged from v1):
- Only YELLOW entry cells written; BLUE formula columns & GREY prefilled
  codes untouched.
- Dropdown validation values used verbatim.
- Payment % columns sum to exactly 100.
- Dates as date objects (cells formatted dd/mm/yyyy).
- Price chain internally consistent: producer -> aratdar -> bepari ->
  retailer -> consumer.
- Fixed RNG seed for reproducibility.
"""
import random
from datetime import date

import openpyxl

import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "03_data_entry_template", "Marine_Fish_Marketing_Data_Entry (1).xlsx")
# Simulated test data goes to archive/ — never overwrite REAL field data
OUT_SIM = os.path.join(ROOT, "04_data_filled", "archive", "SIMULATED_v2_20260911_Chattogram_Filled.xlsx")
OUT_LEGACY = os.path.join(ROOT, "04_data_filled", "Marine_Fish_Marketing_Data_Entry_Chattogram_Filled.xlsx")
# Default OUT is archive version; legacy path kept for backward compat but warns
OUT = OUT_SIM

rng = random.Random(20260911)  # v2 seed = 2026-09-11 (Chattogram realistic, see worklog Task 13)

# ----------------------------------------------------------------------------
# 1. CONFIG
# ----------------------------------------------------------------------------
MARKETS = {
    "M1": dict(name="Fishery Ghat", date=date(2026, 3, 3), mult=1.00,
               session=("04:30", "09:00"), cons=("05:40", "08:40"),
               wholesale=True),
    "M2": dict(name="Chawkbazar", date=date(2026, 3, 4), mult=1.07,
               session=("07:00", "11:30"), cons=("07:15", "11:15"),
               wholesale=False),
    "M3": dict(name="Kazir Dewri", date=date(2026, 3, 5), mult=1.08,
               session=("07:30", "12:00"), cons=("07:45", "11:45"),
               wholesale=False),
    "M4": dict(name="Karnaphuli Complex", date=date(2026, 3, 6), mult=1.05,
               session=("06:30", "10:30"), cons=("06:45", "10:15"),
               wholesale=False),
    "M5": dict(name="Bahaddarhat", date=date(2026, 3, 7), mult=1.10,
               session=("07:00", "11:30"), cons=("07:15", "11:15"),
               wholesale=False),
    "M6": dict(name="Patenga", date=date(2026, 3, 3), mult=1.02,
               session=("09:45", "13:30"), cons=("10:00", "13:15"),
               wholesale=True),
}
MKT_ORDER = ["M1", "M2", "M3", "M4", "M5", "M6"]
LANDING_MARKETS = ("M1", "M6")

SPECIES = {
    "S01": dict(local="Ilish", base=1120, avail=0.85),   # lean-season 2026
    "S02": dict(local="Rupchanda", base=1150, avail=0.75),
    "S03": dict(local="Lakkha", base=750, avail=0.55),
    "S04": dict(local="Koral", base=650, avail=0.50),
    "S05": dict(local="Surma", base=420, avail=0.80),
    "S06": dict(local="Churi", base=320, avail=0.85),
    "S07": dict(local="Poa", base=380, avail=0.70),
    "S08": dict(local="Kankoita", base=240, avail=0.55),  # was 0.35
    "S09": dict(local="Loitta", base=190, avail=0.80),
    "S10": dict(local="Harina", base=160, avail=0.65),    # was 0.50
}
SP_ORDER = list(SPECIES.keys())

EDU_WEIGHTS = [("Illiterate", 0.12), ("Primary", 0.33), ("Secondary", 0.42),
               ("Higher_Secondary", 0.13)]

PROBLEM_POOL = [
    "High ice price", "Rising toll and lease burden", "Unsold fish spoilage loss",
    "Day-to-day price volatility", "Irregular electricity and load-shedding",
    "Transport cost increase", "Delayed credit recovery", "Supply syndicate control",
    "Low landings in lean season", "Waterlogging during monsoon",
    "Competition from frozen imported fish", "Rising cost of ice and salt",
]

OTHER_COST_POOL = [
    ("Market committee toll", 800, 4000), ("Union levy", 500, 2500),
    ("Weighing scale repair", 400, 1500), ("Auction hall cleaning fee", 300, 1200),
    ("Ice block purchase", 1000, 5000),
]

SOURCE_POOL_LOCAL = ["Fishery Ghat landing", "Karnaphuli river ghat"]
SOURCE_POOL_COAST = ["Cox's Bazar landing", "Kutubdia", "Moheshkhali", "Teknaf",
                     "Bhola charter landing", "Kuakata"]

TAG_EXTRA_FISH = [
    ("Bagda chingri", 800, 1300), ("Chatka chingri", 300, 500),
    ("Kakra (crab)", 400, 700), ("Faisya", 250, 400),
    ("Lobster (local)", 2200, 3500), ("Moid", 150, 250),
    ("Datina", 300, 500), ("Khoira", 200, 350),
]

# consumer demand weights (wanted-species probability)
BUY_PROBS = [("S01", 0.50), ("S02", 0.32), ("S03", 0.15), ("S04", 0.15),
             ("S05", 0.50), ("S06", 0.70), ("S07", 0.30), ("S08", 0.20),
             ("S09", 0.58), ("S10", 0.30)]

# buy-price multiplier by declared source (per-kg, relative to wholesale
# anchor W of that market-day)
BEPARI_BUY_MULT = {
    "Fisherman": (0.955, 0.985),   # direct from boats / fishermen
    "Aratdar":   (0.995, 1.020),   # commission agent's sell price
    "Faria":     (1.000, 1.050),   # small intermediary markup
    "Other":     (0.990, 1.030),
}
RETAILER_BUY_MULT = {
    "Fisherman": (0.960, 0.990),   # only at landing markets
    "Aratdar":   (1.000, 1.020),
    "Faria":     (1.040, 1.100),
    "Other":     (1.080, 1.150),   # bepari / Khatunganj wholesale hauls
}

MIN_CONS_GUARD = 3      # bought-today consumer rows per species
MIN_LANDING = 2         # landing aratdar buy+sell quotes per species
MIN_PO_ROWS = 20        # total PO rows per species
MIN_RETAIL_MKTS = 3     # markets with retailer sell quotes per species
MAX_PO = 500            # template prefilled Obs_ID limit

# ----------------------------------------------------------------------------
# 2. HELPERS
# ----------------------------------------------------------------------------
def wchoice(pairs):
    r = rng.random()
    acc = 0.0
    for val, p in pairs:
        acc += p
        if r <= acc:
            return val
    return pairs[-1][0]


def round_price_kg(x):
    """Round a BDT/kg price to a natural-looking integer quote."""
    return int(round(x / 5.0) * 5)


def round_maund_quote(per_kg):
    """Round per-maund quote (per_kg * 37.32) to a natural taka figure."""
    raw = per_kg * 37.32
    if raw >= 10000:
        step = 250
    elif raw >= 3000:
        step = 100
    else:
        step = 50
    return int(round(raw / step) * step)


def put(ws, row, col, value):
    ws.cell(row=row, column=col).value = value


def pick_problems(n=3):
    return rng.sample(PROBLEM_POOL, n)


def t_min(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def rand_time(mk):
    lo, hi = (t_min(x) for x in MARKETS[mk]["cons"])
    t = rng.randint(lo, hi)
    return f"{t // 60:02d}:{t % 60:02d}"


def species_availability(market, actor):
    """Availability probability of each species for a trader at a market."""
    probs = {}
    low_tier = {"S08", "S09", "S10"}
    for sp, cfg in SPECIES.items():
        p = cfg["avail"]
        if not MARKETS[market]["wholesale"] and sp in low_tier:
            p *= 0.55          # retail neighbourhoods carry fewer low-tier species
        if MARKETS[market]["wholesale"] and sp in low_tier:
            p *= 1.25          # landing markets move volume of everything
        if actor == "Bepari_Faria":
            p *= 0.92
        probs[sp] = min(p, 0.93)
    return probs


def pick_active(market, actor, cap=5):
    """UNBIASED random sample of species handled by this trader today."""
    probs = species_availability(market, actor)
    avail = [sp for sp in SP_ORDER if rng.random() < probs[sp]]
    if len(avail) < 4:
        avail = rng.sample(SP_ORDER, 4)
    rng.shuffle(avail)
    return avail[:cap]


def mk_consumer_purchase(mk, sp):
    paid = RC[mk][sp] * rng.uniform(0.99, 1.03)
    return dict(sp=sp, bought=True, price=round_price_kg(paid),
                qty=rng.choice([0.5, 0.75, 1.0, 1.0, 1.25, 1.5, 2.0, 2.5]),
                frm=wchoice([("Retailer", 0.85), ("Hawker", 0.15)]))


# ----------------------------------------------------------------------------
# 3. LOAD WORKBOOK
# ----------------------------------------------------------------------------
wb = openpyxl.load_workbook(SRC)  # formulas preserved
wb.properties.creator = "Z.ai"


def quota_rows(ws, market, actor, serial_max=5):
    """Excel rows holding the quota respondents (serials 01..05)."""
    rows = []
    prefix = f"{market}-{actor}-"
    for r in range(5, ws.max_row + 1):
        rid = ws.cell(row=r, column=2).value
        if isinstance(rid, str) and rid.startswith(prefix):
            try:
                serial = int(rid.split("-")[2])
            except (IndexError, ValueError):
                continue
            if serial <= serial_max:
                rows.append((r, rid))
    return rows


# ----------------------------------------------------------------------------
# 4. MARKET-DAY PRICE ANCHORS (law of one price within a market-day)
# ----------------------------------------------------------------------------
W = {}    # wholesale anchor per market x species (BDT/kg)
RC = {}   # retail anchor per market x species (BDT/kg)
for mk in MKT_ORDER:
    mult = MARKETS[mk]["mult"]
    W[mk] = {}
    RC[mk] = {}
    for sp in SP_ORDER:
        w = SPECIES[sp]["base"] * mult * rng.uniform(0.96, 1.04)
        W[mk][sp] = w
        RC[mk][sp] = w * rng.uniform(1.27, 1.35)

# ----------------------------------------------------------------------------
# 5. RESPONDENT DATA MODEL
# ----------------------------------------------------------------------------
traders = []    # each: dict(id, market, actor, sheet_row, ...) with price quotes
consumers = []  # each: dict(id, market, row, purchases=[...], other_fish=[...])

for mk in MKT_ORDER:
    # ---- Aratdars (Form A) ----
    for row, rid in quota_rows(wb["Form_A_Aratdar"], mk, "A"):
        age = rng.randint(28, 62)
        edu = wchoice(EDU_WEIGHTS)
        years = min(age - 16, rng.randint(5, 40))
        cap_raw = rng.randint(8, 35)
        active = pick_active(mk, "Aratdar")
        quotes = {}
        for sp in active:
            w = W[mk][sp]
            quotes[sp] = dict(buy_kg=w * rng.uniform(0.955, 0.975),   # fisherman receives
                              sell_kg=w * rng.uniform(1.000, 1.015))  # bepari pays
        traders.append(dict(
            id=rid, market=mk, actor="Aratdar", sheet_row=row, sheet="Form_A_Aratdar",
            age=age, edu=edu, years=years, cap_raw=cap_raw, cap_unit="Maund",
            active=active, quotes=quotes, k_species=[], d_flags={},
        ))

    # ---- Bepari / Faria (Form B) ----
    for row, rid in quota_rows(wb["Form_B_Bepari_Faria"], mk, "B"):
        subtype = wchoice([("Bepari", 0.62), ("Faria", 0.38)])
        pattern = wchoice([("Year_round", 0.70), ("Seasonal", 0.30)])
        age = rng.randint(22, 58)
        edu = wchoice(EDU_WEIGHTS)
        years = min(age - 16, rng.randint(3, 35))
        cap_raw = rng.randint(4, 12) if subtype == "Bepari" else round(rng.uniform(1.0, 4.0), 1)
        active = pick_active(mk, "Bepari_Faria")
        buy_source = wchoice([("Fisherman", 0.50), ("Aratdar", 0.30),
                             ("Faria", 0.15), ("Other", 0.05)])
        quotes = {}
        for sp in active:
            w = W[mk][sp]
            lo, hi = BEPARI_BUY_MULT[buy_source]
            quotes[sp] = dict(buy_kg=w * rng.uniform(lo, hi),
                              sell_kg=w * rng.uniform(1.10, 1.17))
        if mk in LANDING_MARKETS:
            source = rng.choice(SOURCE_POOL_LOCAL)
            fare = rng.randint(300, 1200)
        else:
            source = rng.choice(SOURCE_POOL_LOCAL + SOURCE_POOL_COAST)
            fare = rng.randint(500, 3500) if source in SOURCE_POOL_COAST else rng.randint(400, 1500)
        traders.append(dict(
            id=rid, market=mk, actor="Bepari_Faria", sheet_row=row, sheet="Form_B_Bepari_Faria",
            age=age, edu=edu, years=years, cap_raw=cap_raw, cap_unit="Maund",
            active=active, quotes=quotes, k_species=[], d_flags={},
            subtype=subtype, pattern=pattern, source=source, buy_source=buy_source,
        ))

    # ---- Khuchra retailers (Form R) ----
    for row, rid in quota_rows(wb["Form_R_Khuchra"], mk, "R"):
        age = rng.randint(20, 55)
        edu = wchoice(EDU_WEIGHTS)
        years = min(age - 16, rng.randint(2, 32))
        use_kg = rng.random() < 0.85
        cap_raw = rng.randint(40, 150) if use_kg else round(rng.uniform(1.0, 3.0), 1)
        active = pick_active(mk, "Khuchra")
        # source: no direct fisherman purchases at inland retail markets
        if mk in LANDING_MARKETS:
            buy_source = wchoice([("Fisherman", 0.35), ("Aratdar", 0.40),
                                  ("Faria", 0.20), ("Other", 0.05)])
        else:
            buy_source = wchoice([("Aratdar", 0.50), ("Faria", 0.25),
                                  ("Other", 0.25)])
        quotes = {}
        for sp in active:
            w = W[mk][sp]
            lo, hi = RETAILER_BUY_MULT[buy_source]
            quotes[sp] = dict(buy_kg=w * rng.uniform(lo, hi),
                              sell_kg=RC[mk][sp] * rng.uniform(1.00, 1.05))
        traders.append(dict(
            id=rid, market=mk, actor="Khuchra", sheet_row=row, sheet="Form_R_Khuchra",
            age=age, edu=edu, years=years, cap_raw=cap_raw,
            cap_unit="Kg" if use_kg else "Maund",
            active=active, quotes=quotes, k_species=[], d_flags={},
            buy_source=buy_source,
        ))

    # ---- Consumers (Form C) ----
    for row, rid in quota_rows(wb["Form_C_Consumer"], mk, "C"):
        freq = wchoice([("Daily", 0.35), ("Weekly", 0.65)])
        interval = rng.randint(1, 2) if freq == "Daily" else rng.randint(4, 7)
        wanted = [sp for sp, p in BUY_PROBS if rng.random() < p]
        if not wanted:
            wanted = [rng.choice(["S01", "S06", "S09"])]
        bought = rng.sample(wanted, min(len(wanted), rng.randint(1, 3)))
        rest = [sp for sp, p in BUY_PROBS if sp not in bought and rng.random() < p * 0.35]
        not_today = rng.sample(rest, min(len(rest), rng.randint(0, 2)))
        purchases = [mk_consumer_purchase(mk, sp) for sp in bought]
        for sp in not_today:
            purchases.append(dict(sp=sp, bought=False, price="K", qty=None, frm=""))
        consumers.append(dict(
            id=rid, market=mk, row=row, time=rand_time(mk),
            freq=freq, interval=interval,
            pay=wchoice([("Cash", 0.50), ("bKash", 0.28), ("Nagad_app", 0.12), ("Credit", 0.10)]),
            reason=wchoice([("Proximity", 0.25), ("Purity", 0.25), ("Price", 0.20),
                            ("Familiar_shop", 0.15), ("Variety", 0.10), ("Other", 0.05)]),
            purchases=purchases, other_fish=[],
        ))

# ----------------------------------------------------------------------------
# 6. K ROWS + D FLAGS (assigned BEFORE pairs so pairs can be protected)
# ----------------------------------------------------------------------------
for t in traders:
    rest = [sp for sp in SP_ORDER if sp not in t["active"]]
    if rng.random() < 0.35 and rest:
        t["k_species"] = rng.sample(rest, min(len(rest), rng.randint(1, 2)))
    for sp in t["active"]:
        r = rng.random()
        if r < 0.035:
            t["d_flags"][sp] = "sell"
        elif r < 0.055:
            t["d_flags"][sp] = "buy"

# ----------------------------------------------------------------------------
# 7. PAIR LINKAGE (Methodology 3.3.4)
# ----------------------------------------------------------------------------
pairs = []
for mk in MKT_ORDER:
    arat = [t for t in traders if t["market"] == mk and t["actor"] == "Aratdar"]
    retail = [t for t in traders if t["market"] == mk and t["actor"] == "Khuchra"]
    n_pairs = rng.randint(2, 3)
    sellers = rng.sample(arat, min(n_pairs, len(arat)))
    buyers = rng.sample(retail, min(n_pairs, len(retail)))
    for i, (seller, buyer) in enumerate(zip(sellers, buyers), 1):
        both = [sp for sp in seller["active"] if sp in buyer["active"]]
        if not both:
            continue
        sp = rng.choice(both)
        # transaction price: retailer buys at the aratdar's sell price
        sell_kg = seller["quotes"][sp]["sell_kg"]
        buyer["quotes"][sp]["buy_kg"] = sell_kg * rng.uniform(0.999, 1.001)
        buyer["buy_source"] = "Aratdar"          # declared source consistent
        pair_id = f"PAIR-{mk}-{i:02d}"
        seller["pair"] = (pair_id, sp)
        buyer["pair"] = (pair_id, sp)
        pairs.append(dict(pair_id=pair_id, market=mk, seller_id=seller["id"],
                          buyer_id=buyer["id"], species=sp))

# protect pair species from K/D / not-yet-sold on BOTH sides
for t in traders:
    if "pair" in t:
        sp = t["pair"][1]
        t["k_species"] = [s2 for s2 in t["k_species"] if s2 != sp]
        t["d_flags"].pop(sp, None)

# ----------------------------------------------------------------------------
# 8. COVERAGE GUARDS (all-ten-species reporting)
# ----------------------------------------------------------------------------
def landing_quotes(sp):
    n = 0
    for t in traders:
        if t["actor"] == "Aratdar" and t["market"] in LANDING_MARKETS:
            if sp in t["active"] and sp not in t["d_flags"] and sp not in t["k_species"]:
                n += 1
    return n


def add_species_to_trader(t, sp):
    """Force sp into trader's active list with anchor-derived quotes."""
    if sp in t["active"]:
        return
    if len(t["active"]) >= 5:
        # drop a species that has the most coverage overall
        counts = {}
        for t2 in traders:
            if t2["actor"] == t["actor"]:
                for s2 in t2["active"]:
                    counts[s2] = counts.get(s2, 0) + 1
        drop = max(t["active"], key=lambda s2: counts.get(s2, 0))
        t["active"] = [s2 for s2 in t["active"] if s2 != drop]
        t["quotes"].pop(drop, None)
        t["k_species"] = [s2 for s2 in t["k_species"] if s2 != sp]
    t["active"].append(sp)
    t["k_species"] = [s2 for s2 in t["k_species"] if s2 != sp]
    t["d_flags"].pop(sp, None)
    w = W[t["market"]][sp]
    if t["actor"] == "Aratdar":
        t["quotes"][sp] = dict(buy_kg=w * rng.uniform(0.955, 0.975),
                               sell_kg=w * rng.uniform(1.000, 1.015))
    elif t["actor"] == "Bepari_Faria":
        lo, hi = BEPARI_BUY_MULT[t["buy_source"]]
        t["quotes"][sp] = dict(buy_kg=w * rng.uniform(lo, hi),
                                sell_kg=w * rng.uniform(1.10, 1.17))
    else:
        lo, hi = RETAILER_BUY_MULT[t["buy_source"]]
        t["quotes"][sp] = dict(buy_kg=w * rng.uniform(lo, hi),
                               sell_kg=RC[t["market"]][sp] * rng.uniform(1.00, 1.05))


# guard 1: landing aratdar buy+sell quotes (producer price availability)
for sp in SP_ORDER:
    for mk in LANDING_MARKETS:
        tries = 0
        while landing_quotes(sp) < MIN_LANDING and tries < 20:
            tries += 1
            cands = [t for t in traders if t["market"] == mk and t["actor"] == "Aratdar"
                     and sp not in t["active"]]
            if not cands:
                break
            add_species_to_trader(rng.choice(cands), sp)

# guard 2: retailer sell quotes in >= MIN_RETAIL_MKTS markets
for sp in SP_ORDER:
    def retail_mkts_with_sell():
        mkts = set()
        for t in traders:
            if (t["actor"] == "Khuchra" and sp in t["active"]
                    and sp not in t["d_flags"] and sp not in t["k_species"]):
                mkts.add(t["market"])
        return mkts
    tries = 0
    while len(retail_mkts_with_sell()) < MIN_RETAIL_MKTS and tries < 30:
        tries += 1
        have = retail_mkts_with_sell()
        need = [m for m in MKT_ORDER if m not in have]
        mk = rng.choice(need)
        cands = [t for t in traders if t["market"] == mk and t["actor"] == "Khuchra"
                 and sp not in t["active"] and "pair" not in t]
        if not cands:
            continue
        add_species_to_trader(rng.choice(cands), sp)

# guard 3: bought-today consumer rows >= MIN_CONS_GUARD per species
def bought_count(sp):
    return sum(1 for c in consumers for p in c["purchases"]
               if p["bought"] and p["sp"] == sp)


for sp in SP_ORDER:
    tries = 0
    while bought_count(sp) < MIN_CONS_GUARD and tries < 40:
        tries += 1
        cands = [c for c in consumers
                 if all(p["sp"] != sp for p in c["purchases"])]
        if not cands:
            break
        c = min(cands, key=lambda x: sum(1 for p in x["purchases"] if p["bought"]))
        nt = next((p for p in c["purchases"] if not p["bought"]), None)
        if nt is not None:
            new = mk_consumer_purchase(c["market"], sp)
            nt.clear()
            nt.update(new)
        elif sum(1 for p in c["purchases"] if p["bought"]) < 3:
            c["purchases"].append(mk_consumer_purchase(c["market"], sp))
        # else: consumer already at 3 bought rows; loop picks another candidate

# ----------------------------------------------------------------------------
# 9. WRITE FORM SHEETS
# ----------------------------------------------------------------------------
wsA = wb["Form_A_Aratdar"]
for t in [x for x in traders if x["actor"] == "Aratdar"]:
    r = t["sheet_row"]
    put(wsA, r, 4, MARKETS[t["market"]]["date"])          # D Interview_Date
    put(wsA, r, 5, t["age"])                               # E Age
    put(wsA, r, 6, t["edu"])                               # F Education
    put(wsA, r, 7, t["years"])                             # G Years
    put(wsA, r, 8, t["cap_raw"])                           # H capacity raw
    put(wsA, r, 9, "Maund")                                # I unit
    put(wsA, r, 11, rng.randint(3, 9))                     # K family
    # rent / lease
    if rng.random() < 0.85:
        put(wsA, r, 12, "Pay")
        if rng.random() < 0.75:
            amt = {"M1": rng.randint(30, 84), "M6": rng.randint(16, 40)
                   }.get(t["market"], rng.randint(12, 50)) * 5000
            put(wsA, r, 13, amt); put(wsA, r, 14, "Yearly")
        else:
            put(wsA, r, 13, rng.randint(8, 30) * 1000); put(wsA, r, 14, "Monthly")
    else:
        put(wsA, r, 12, "Receive")
        put(wsA, r, 13, rng.randint(2, 8) * 500); put(wsA, r, 14, "Monthly")
    # commission
    basis = wchoice([("Percent", 0.70), ("Lot", 0.20), ("Kg", 0.10)])
    put(wsA, r, 15, basis)
    if basis == "Percent":
        put(wsA, r, 16, rng.choice([2.0, 2.5, 3.0, 3.5, 4.0, 5.0]))
    elif basis == "Lot":
        put(wsA, r, 16, rng.choice([500, 800, 1000, 1500, 2000, 2500]))
    else:
        put(wsA, r, 16, rng.choice([1, 1.5, 2, 2.5, 3]))
    # electricity
    put(wsA, r, 17, rng.randint(25, 140) * 100)
    put(wsA, r, 18, "Monthly" if rng.random() < 0.9 else "Yearly")
    # workers
    put(wsA, r, 19, rng.randint(2, 9))
    put(wsA, r, 20, rng.choice([500, 550, 600, 650, 700, 750, 800]))
    # equipment / cooler maintenance
    put(wsA, r, 21, rng.randint(3, 24) * 500)
    put(wsA, r, 22, "Yearly" if rng.random() < 0.6 else "Monthly")
    # other cost
    desc, lo, hi = rng.choice(OTHER_COST_POOL)
    put(wsA, r, 23, desc)
    put(wsA, r, 24, round(rng.randint(lo, hi) / 50.0) * 50)
    # payment mix (must sum to 100)
    cash = rng.randint(55, 80)
    mfs = rng.randint(5, min(25, 100 - cash - 5))
    put(wsA, r, 25, cash); put(wsA, r, 26, mfs); put(wsA, r, 27, 100 - cash - mfs)
    put(wsA, r, 28, wchoice([("Regular", 0.40), ("Occasional", 0.45), ("Never", 0.15)]))
    p1, p2, p3 = pick_problems()
    put(wsA, r, 29, p1); put(wsA, r, 30, p2); put(wsA, r, 31, p3)
    if "pair" in t:
        put(wsA, r, 32, t["pair"][0])
    if rng.random() < 0.12:
        put(wsA, r, 33, rng.choice([
            "Interviewed between two auction sessions",
            "Handles consignments for Dhaka buyers as well",
            "Second-generation arat business",
            "Also supplies ice to stall vendors",
        ]))

wsB = wb["Form_B_Bepari_Faria"]
for t in [x for x in traders if x["actor"] == "Bepari_Faria"]:
    r = t["sheet_row"]
    put(wsB, r, 4, MARKETS[t["market"]]["date"])
    put(wsB, r, 5, t["subtype"])
    put(wsB, r, 6, t["pattern"])
    put(wsB, r, 7, t["age"])
    put(wsB, r, 8, t["edu"])
    put(wsB, r, 9, t["years"])
    put(wsB, r, 10, t["cap_raw"])
    put(wsB, r, 11, "Maund")
    put(wsB, r, 13, rng.randint(2, 8))
    put(wsB, r, 14, t["source"])
    put(wsB, r, 15, t["buy_source"])
    fare = rng.randint(8, 70) * 50
    put(wsB, r, 16, fare)
    put(wsB, r, 17, rng.randint(1, 3))                     # per N days
    put(wsB, r, 18, rng.randint(1, 3))                     # M trips
    put(wsB, r, 19, rng.randint(2, 10) * 50)               # loading/unloading per trip
    ice_kg = rng.randint(30, 120)
    put(wsB, r, 20, ice_kg)
    put(wsB, r, 21, round(ice_kg * rng.uniform(2.5, 4.0) / 10.0) * 10)
    if rng.random() < 0.8:
        put(wsB, r, 22, rng.choice([2.0, 2.5, 3.0, 3.5, 4.0, 5.0])); put(wsB, r, 23, "Percent_of_lot")
    else:
        put(wsB, r, 22, rng.choice([300, 500, 800, 1000, 1500])); put(wsB, r, 23, "BDT_per_lot")
    put(wsB, r, 24, rng.randint(2, 8))                     # transit damage %
    cash = rng.randint(50, 80)
    mfs = rng.randint(5, min(30, 100 - cash - 5))
    put(wsB, r, 25, cash); put(wsB, r, 26, mfs); put(wsB, r, 27, 100 - cash - mfs)
    put(wsB, r, 28, wchoice([("Regular", 0.35), ("Occasional", 0.50), ("Never", 0.15)]))
    put(wsB, r, 29, wchoice([("Almost_all", 0.10), ("Some", 0.55), ("None", 0.35)]))
    p1, p2, p3 = pick_problems()
    put(wsB, r, 30, p1); put(wsB, r, 31, p2); put(wsB, r, 32, p3)
    if rng.random() < 0.10:
        put(wsB, r, 34, rng.choice([
            "Carries fish for two other traders on same pickup",
            "Uses rented pickup van for long routes",
            "Seasonal supplier during ilish closure for other species",
        ]))

wsR = wb["Form_R_Khuchra"]
for t in [x for x in traders if x["actor"] == "Khuchra"]:
    r = t["sheet_row"]
    put(wsR, r, 4, MARKETS[t["market"]]["date"])
    put(wsR, r, 5, t["age"])
    put(wsR, r, 6, t["edu"])
    put(wsR, r, 7, t["years"])
    put(wsR, r, 8, t["cap_raw"])
    put(wsR, r, 9, t["cap_unit"])
    put(wsR, r, 11, rng.randint(2, 8))
    put(wsR, r, 12, rng.randint(12, 70) * 5)               # shop/van rent per day
    put(wsR, r, 13, rng.randint(16, 50) * 5)               # ice per day
    put(wsR, r, 14, rng.randint(6, 30) * 5)                # wash/water/other per day
    put(wsR, r, 15, rng.randint(2, 8))                     # spoilage %
    put(wsR, r, 16, t["buy_source"])
    put(wsR, r, 17, wchoice([("Household", 0.60), ("Hawker", 0.15), ("Hotel", 0.15),
                             ("Institutional", 0.05), ("Other", 0.05)]))
    cash = rng.randint(40, 70)
    mfs = rng.randint(15, min(45, 100 - cash - 5))
    put(wsR, r, 18, cash); put(wsR, r, 19, mfs); put(wsR, r, 20, 100 - cash - mfs)
    put(wsR, r, 21, wchoice([("Regular", 0.45), ("Occasional", 0.40), ("Never", 0.15)]))
    put(wsR, r, 22, wchoice([("Some", 0.60), ("Almost_all", 0.10), ("No", 0.30)]))
    p1, p2, p3 = pick_problems()
    put(wsR, r, 23, p1); put(wsR, r, 24, p2); put(wsR, r, 25, p3)
    if "pair" in t:
        put(wsR, r, 26, t["pair"][0])
    if rng.random() < 0.10:
        put(wsR, r, 27, rng.choice([
            "Van-based vendor, moves with morning footfall",
            "Keeps display on crushed ice slabs",
            "Supplies two nearby restaurants on order",
        ]))

wsC = wb["Form_C_Consumer"]
for c in consumers:
    r = c["row"]
    put(wsC, r, 4, MARKETS[c["market"]]["date"])
    put(wsC, r, 5, c["time"])
    put(wsC, r, 6, "Yes")                                  # consent
    put(wsC, r, 7, c["freq"])
    put(wsC, r, 8, c["interval"])
    put(wsC, r, 9, c["pay"])
    put(wsC, r, 10, c["reason"])
    if rng.random() < 0.08:
        put(wsC, r, 12, rng.choice([
            "Accompanied by spouse, joint purchase decision",
            "Asked for gutting before packing",
            "Complained about recent price rise",
        ]))

# ----------------------------------------------------------------------------
# 10. PRICE OBSERVATIONS (core long-format sheet, rows 5.., prefilled Obs_ID)
# ----------------------------------------------------------------------------
wsP = wb["Price_Observations"]
po_row = 5
po_count = 0


def po_next():
    global po_row, po_count
    r = po_row
    po_row += 1
    po_count += 1
    return r


def split_qty(cap, n, unit):
    weights = [rng.uniform(0.6, 1.4) for _ in range(n)]
    total = sum(weights)
    out = []
    for wgt in weights:
        q = cap * wgt / total * rng.uniform(0.85, 1.0)
        out.append(round(q, 1) if unit == "Maund" else max(5, int(round(q / 5.0) * 5)))
    return out


for t in traders:
    if po_count >= MAX_PO:
        break
    actor = t["actor"]
    unit = "Kg" if actor == "Khuchra" and t["cap_unit"] == "Kg" else "Maund"
    cap = t["cap_raw"]
    qtys = split_qty(cap, len(t["active"]), unit)
    for idx, sp in enumerate(t["active"]):
        if po_count >= MAX_PO:
            break
        q = t["quotes"][sp]
        r = po_next()
        put(wsP, r, 3, t["id"])                              # C Respondent_ID
        put(wsP, r, 4, t["market"])                          # D Market
        put(wsP, r, 5, actor)                                # E Actor_type
        put(wsP, r, 6, sp)                                   # F Species_code
        buy_raw = "D" if t["d_flags"].get(sp) == "buy" else None
        sell_raw = "D" if t["d_flags"].get(sp) == "sell" else None
        if actor == "Khuchra" and t["cap_unit"] == "Kg":
            buy_val = round_price_kg(q["buy_kg"])
            sell_val = round_price_kg(q["sell_kg"])
        else:
            buy_val = round_maund_quote(q["buy_kg"])
            sell_val = round_maund_quote(q["sell_kg"])
        # retailers occasionally have not-yet-sold stock -> sell = K
        # (never on the pair species: the pair transaction completed today)
        if (actor == "Khuchra" and sell_raw is None and rng.random() < 0.08
                and not ("pair" in t and t["pair"][1] == sp)):
            sell_raw = "K"
        put(wsP, r, 7, buy_raw if buy_raw else buy_val)      # G buy price raw
        put(wsP, r, 8, sell_raw if sell_raw else sell_val)   # H sell price raw
        put(wsP, r, 9, unit)                                 # I unit
        put(wsP, r, 12, qtys[idx])                           # L quantity raw
        put(wsP, r, 13, unit)                                # M quantity unit
        if "pair" in t and t["pair"][1] == sp:
            put(wsP, r, 15, t["pair"][0])                    # O Pair_ID
        if buy_raw or sell_raw:
            note = []
            if buy_raw == "D":
                note.append("Buy price declined")
            if sell_raw == "K":
                note.append("Bought but no sale yet today")
            if sell_raw == "D":
                note.append("Sell price declined")
            put(wsP, r, 16, "; ".join(note))
    # K-flag rows: species grid marked K (not handled today)
    for sp in t["k_species"]:
        if po_count >= MAX_PO:
            break
        r = po_next()
        put(wsP, r, 3, t["id"])
        put(wsP, r, 4, t["market"])
        put(wsP, r, 5, actor)
        put(wsP, r, 6, sp)
        put(wsP, r, 7, "K")
        put(wsP, r, 8, "K")
        put(wsP, r, 16, "Species not handled today")

# ----------------------------------------------------------------------------
# 11. CONSUMER PURCHASE SHEETS
# ----------------------------------------------------------------------------
wsF = wb["Consumer_Purchases_Focal"]
frow = 5
for c in consumers:
    for p in c["purchases"]:
        put(wsF, frow, 2, c["id"])                           # B Respondent_ID
        put(wsF, frow, 3, c["market"])                       # C Market
        put(wsF, frow, 4, p["sp"])                           # D Species_code
        put(wsF, frow, 5, "Yes" if p["bought"] else "No")    # E Purchased_today
        if p["bought"]:
            put(wsF, frow, 6, p["frm"])                      # F Bought_from
            put(wsF, frow, 7, p["price"])                    # G price raw (BDT/kg)
            put(wsF, frow, 8, "Kg")                          # H unit
            put(wsF, frow, 10, p["qty"])                     # J quantity raw
            put(wsF, frow, 11, "Kg")                         # K quantity unit
        else:
            put(wsF, frow, 7, "K")                           # not bought today
        frow += 1

wsO = wb["Consumer_Other_Fish"]
orow = 5
for c in consumers:
    if rng.random() < 0.40:
        n = rng.randint(1, 2)
        chosen = rng.sample(TAG_EXTRA_FISH, n)
        for name, lo, hi in chosen:
            price = round_price_kg(rng.uniform(lo, hi))
            qty = rng.choice([0.25, 0.5, 0.5, 0.75, 1.0, 1.5])
            loc = wchoice([("Same market", 0.75), ("Khatunganj wholesale", 0.10),
                           ("Neighbourhood van", 0.15)])
            put(wsO, orow, 2, c["id"])
            put(wsO, orow, 3, c["market"])
            put(wsO, orow, 4, name)
            put(wsO, orow, 5, price)
            put(wsO, orow, 6, "Kg")
            put(wsO, orow, 8, qty)
            put(wsO, orow, 9, "Kg")
            put(wsO, orow, 11, loc)
            c["other_fish"].append(name)
            orow += 1

# ----------------------------------------------------------------------------
# 12. FORM M - MARKET OBSERVATION CHECKLIST (one row per market)
# ----------------------------------------------------------------------------
wsM = wb["Form_M_Market_Observation"]
FORM_M = {
    "M1": dict(mtype="Mixed", hours="03:30-13:00", stalls=210, transport="Good",
               platform="Medium", roofing="Partial", drainage="Medium", elec="Irregular",
               ice="Available", ice_note="On-site ice factory, approx 150 m",
               sani="Poor", water="Irregular", fee="Aratdar",
               fee_note="2.5-5% commission per lot; daily stall fee BDT 30-60",
               gps="22.3370, 91.8312", photos="IMG_M1_01 to IMG_M1_04",
               evidence="Direct observation; verbal confirmation from committee office"),
    "M2": dict(mtype="Retail", hours="06:00-20:00", stalls=160, transport="Good",
               platform="Good", roofing="Complete", drainage="Medium", elec="Regular",
               ice="Available", ice_note="Two private ice suppliers at gate",
               sani="Medium", water="Regular", fee="Committee",
               fee_note="Daily toll BDT 50 per stall; monthly cleaning levy",
               gps="22.3392, 91.8366", photos="IMG_M2_01 to IMG_M2_04",
               evidence="Direct observation; stall-count estimated with market supervisor"),
    "M3": dict(mtype="Retail", hours="06:30-19:30", stalls=85, transport="Medium",
               platform="Medium", roofing="Partial", drainage="Poor", elec="Regular",
               ice="Available", ice_note="Ice cart delivery from Bahaddarhat, 1.5 km",
               sani="Medium", water="Regular", fee="Committee",
               fee_note="Daily toll BDT 40 per stall",
               gps="22.3415, 91.8301", photos="IMG_M3_01 to IMG_M3_03",
               evidence="Direct observation; verbal confirmation from stall holders"),
    "M4": dict(mtype="Retail", hours="06:00-20:00", stalls=120, transport="Good",
               platform="Good", roofing="Complete", drainage="Good", elec="Regular",
               ice="Available", ice_note="Ice plant within market compound",
               sani="Good", water="Regular", fee="Committee",
               fee_note="Daily toll BDT 60; covered modern shed",
               gps="22.3318, 91.8178", photos="IMG_M4_01 to IMG_M4_04",
               evidence="Direct observation; office register consulted"),
    "M5": dict(mtype="Retail", hours="06:30-20:00", stalls=110, transport="Medium",
               platform="Good", roofing="Complete", drainage="Medium", elec="Regular",
               ice="Available", ice_note="Adjacent ice factory, approx 300 m",
               sani="Medium", water="Regular", fee="Mixed",
               fee_note="Committee toll plus informal entry charge for vans",
               gps="22.3611, 91.8230", photos="IMG_M5_01 to IMG_M5_03",
               evidence="Direct observation; verbal confirmation from committee member"),
    "M6": dict(mtype="Mixed", hours="04:00-12:30", stalls=65, transport="Medium",
               platform="Poor", roofing="Partial", drainage="Poor", elec="Irregular",
               ice="Available", ice_note="Private ice factory adjacent to landing",
               sani="Poor", water="Irregular", fee="Committee",
               fee_note="Landing-side fee per basket; BDT 20-40 per maund handled",
               gps="22.2786, 91.7991", photos="IMG_M6_01 to IMG_M6_03",
               evidence="Direct observation; verbal confirmation from landing agents"),
}
for r in range(5, 11):
    mk = wsM.cell(row=r, column=2).value          # B prefilled market code
    info = FORM_M[mk]
    put(wsM, r, 4, MARKETS[mk]["date"])           # D Obs_Date
    put(wsM, r, 5, info["mtype"])
    put(wsM, r, 6, info["hours"])
    put(wsM, r, 7, info["stalls"])
    put(wsM, r, 8, info["transport"])
    put(wsM, r, 9, info["platform"])
    put(wsM, r, 10, info["roofing"])
    put(wsM, r, 11, info["drainage"])
    put(wsM, r, 12, info["elec"])
    put(wsM, r, 13, info["ice"])
    put(wsM, r, 14, info["ice_note"])
    put(wsM, r, 15, info["sani"])
    put(wsM, r, 16, info["water"])
    put(wsM, r, 17, info["fee"])
    put(wsM, r, 18, info["fee_note"])
    put(wsM, r, 19, info["gps"])
    put(wsM, r, 20, info["photos"])
    put(wsM, r, 21, info["evidence"])

# ----------------------------------------------------------------------------
# 13. TAG PRICE SHEET (optional displayed-price log)
# ----------------------------------------------------------------------------
wsT = wb["Tag_Price_Sheet"]
trow = 5
COLLECTOR = "RS"
for mk in MKT_ORDER:
    minfo = MARKETS[mk]
    n_vendors = rng.randint(8, 12)
    vendor_ids = [f"V-{i:02d}" for i in range(1, n_vendors + 1)]
    for v_id in vendor_ids:
        # 1-3 displayed items per vendor, priced off the SAME retail anchor
        items = []
        focal = [sp for sp in SP_ORDER if rng.random() < 0.30]
        if not focal:
            focal = [rng.choice(SP_ORDER)]
        for sp in focal[:2]:
            disp = RC[mk][sp] * rng.uniform(0.99, 1.07)
            items.append((SPECIES[sp]["local"], round_price_kg(disp)))
        if rng.random() < 0.45:
            name, lo, hi = rng.choice(TAG_EXTRA_FISH)
            items.append((name, round_price_kg(rng.uniform(lo, hi))))
        for name, price in items:
            put(wsT, trow, 2, minfo["date"])                  # B Date
            put(wsT, trow, 3, mk)                              # C Market
            put(wsT, trow, 4, v_id)                            # D vendor
            put(wsT, trow, 5, COLLECTOR)                      # E initials
            put(wsT, trow, 6, name)                           # F fish name
            put(wsT, trow, 7, price)                           # G price raw
            put(wsT, trow, 8, "Kg")                           # H unit
            if rng.random() < 0.10:
                put(wsT, trow, 10, rng.choice([
                    "Gutting on request", "Displayed on crushed ice",
                    "Live tank display", "Negotiable, quote is asking price",
                ]))
            trow += 1

# ----------------------------------------------------------------------------
# 14. DATA COLLECTION LOG (one row per field visit)
# ----------------------------------------------------------------------------
wsL = wb["Data_Collection_Log"]
LOG = [
    (date(2026, 3, 2), "M1", "Researcher", "05:30", "09:00", "No", 4, 1,
     "Light fog, calm sea",
     "Pilot day: 5 test interviews (one per stratum incl. one consumer); forms "
     "discarded after wording fixes; species list unchanged"),
    (date(2026, 3, 3), "M1", "Researcher", "04:30", "09:00", "No", 15, 5,
     "Fair, moderate NE wind", "Main round opening; all quota rows completed"),
    (date(2026, 3, 3), "M6", "Researcher", "09:45", "13:30", "No", 15, 5,
     "Sunny, rising swell by noon", "Landing-side buy prices recorded at ice jetty"),
    (date(2026, 3, 4), "M2", "Researcher", "07:00", "11:30", "No", 15, 5,
     "Sunny and humid", ""),
    (date(2026, 3, 5), "M3", "Researcher", "07:30", "12:00", "No", 15, 5,
     "Overcast, brief drizzle at 10:30", "Roofing check completed between showers"),
    (date(2026, 3, 6), "M4", "Researcher", "06:30", "10:30", "Yes", 15, 5,
     "Hot, 33 degree C",
     "Friday (Jummah) morning session; some traders left early for prayer; "
     "two bepari quotes taken from Thursday reference session"),
    (date(2026, 3, 7), "M5", "Researcher", "07:00", "11:30", "No", 15, 5,
     "Fair", "Reserve day kept unused; entry and verification began 08/03"),
]
for i, (dt, mk, coll, t1, t2, ref, ntr, nco, weather, note) in enumerate(LOG):
    r = 5 + i
    put(wsL, r, 2, dt)
    put(wsL, r, 4, mk)
    put(wsL, r, 5, coll)
    put(wsL, r, 6, t1)
    put(wsL, r, 7, t2)
    put(wsL, r, 8, ref)
    put(wsL, r, 9, ntr)
    put(wsL, r, 10, nco)
    put(wsL, r, 11, weather)
    put(wsL, r, 12, note)

# ----------------------------------------------------------------------------
# 15. SELF-CHECK BEFORE SAVE (fail loudly on any logical violation)
# ----------------------------------------------------------------------------
errors = []

# quota counts (from the model)
n_a = sum(1 for t in traders if t["actor"] == "Aratdar")
n_b = sum(1 for t in traders if t["actor"] == "Bepari_Faria")
n_r = sum(1 for t in traders if t["actor"] == "Khuchra")
if (n_a, n_b, n_r, len(consumers)) != (30, 30, 30, 30):
    errors.append(f"quota mismatch: A={n_a} B={n_b} R={n_r} C={len(consumers)}")

# PO row limit
if po_count > MAX_PO:
    errors.append(f"PO rows {po_count} exceed template limit {MAX_PO}")

# consumer time windows
for c in consumers:
    lo, hi = (t_min(x) for x in MARKETS[c["market"]]["cons"])
    tt = t_min(c["time"])
    if not (lo <= tt <= hi):
        errors.append(f"time window violation {c['id']} {c['time']}")

# per-species coverage
from collections import Counter
po_rows_species = Counter()
retail_mkts = {}
for t in traders:
    for sp in t["active"]:
        po_rows_species[sp] += 1
        if t["actor"] == "Khuchra" and sp not in t["d_flags"] and sp not in t["k_species"]:
            retail_mkts.setdefault(sp, set()).add(t["market"])
    for sp in t["k_species"]:
        po_rows_species[sp] += 1
for sp in SP_ORDER:
    if bought_count(sp) < MIN_CONS_GUARD:
        errors.append(f"{sp}: consumer bought-today = {bought_count(sp)} < {MIN_CONS_GUARD}")
    if landing_quotes(sp) < MIN_LANDING:
        errors.append(f"{sp}: landing aratdar quotes = {landing_quotes(sp)} < {MIN_LANDING}")
    if po_rows_species[sp] < MIN_PO_ROWS:
        errors.append(f"{sp}: PO rows = {po_rows_species[sp]} < {MIN_PO_ROWS}")
    if len(retail_mkts.get(sp, set())) < MIN_RETAIL_MKTS:
        errors.append(f"{sp}: retail markets = {sorted(retail_mkts.get(sp, set()))}")

# pair completeness: seller sell numeric & buyer buy numeric for every pair
by_id = {t["id"]: t for t in traders}
for p in pairs:
    s, b = by_id[p["seller_id"]], by_id[p["buyer_id"]]
    sp = p["species"]
    if sp in s["d_flags"] or sp in b["d_flags"]:
        errors.append(f"{p['pair_id']}: D-flag on pair species")
    if sp in s["k_species"] or sp in b["k_species"]:
        errors.append(f"{p['pair_id']}: K-species overlaps pair")

# payment sums already enforced by construction (100 - cash - mfs)

if errors:
    print("SELF-CHECK FAILED -- fix before saving:")
    for e in errors:
        print("  !!", e)
    raise SystemExit(1)

# ----------------------------------------------------------------------------
# 16. SAVE + SUMMARY (simulated → archive/ only; never touches REAL field data)
# ----------------------------------------------------------------------------
import os as _os
_os.makedirs(_os.path.dirname(OUT), exist_ok=True)
real_candidates = [
    _os.path.join(ROOT, "04_data_filled", "Marine_Fish_Marketing_Data_Entry_Chattogram_REAL_FILLED.xlsx"),
    _os.path.join(ROOT, "04_data_filled", "Marine_Fish_Marketing_Data_Entry_Chattogram_REAL.xlsx"),
]
for rc in real_candidates:
    if _os.path.exists(rc):
        print(f"[NOTE] REAL field data detected: {rc}")
        print("  Simulated output stays in archive/ and will NOT touch it.")
        break

wb.save(OUT)

print("=" * 64)
print("SAVED:", OUT)
print("=" * 64)
print(f"Respondents entered : {n_a} aratdar + {n_b} bepari/faria + {n_r} retailers"
      f" + {len(consumers)} consumers = {n_a + n_b + n_r + len(consumers)}")
print(f"Price_Observations  : {po_count} rows (limit {MAX_PO})")
print(f"Focal purchases     : {frow - 5} rows")
print(f"Other fish          : {orow - 5} rows")
print(f"Tag price rows      : {trow - 5}")
print(f"Form M markets      : 6")
print(f"Log visits          : {len(LOG)}")
print(f"Matched pairs       : {len(pairs)}")
for p in pairs:
    print(f"  {p['pair_id']}: {p['seller_id']} -> {p['buyer_id']} ({p['species']})")
print("\nPer-species coverage self-check:")
for sp in SP_ORDER:
    print(f"  {sp}: PO rows={po_rows_species[sp]:3d}  bought-today={bought_count(sp)}"
          f"  landing-aratdar={landing_quotes(sp)}"
          f"  retail-markets={len(retail_mkts.get(sp, set()))}")
