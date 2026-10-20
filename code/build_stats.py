"""Build stats.json for the Denver STR licenses brief (2026-10-19).

Primary source: fresh warehouse snapshot
stack/denver/snapshots/2026-10-19/str_licenses.parquet (Denver Excise and
Licenses STR register, ArcGIS layer 54, pulled 2026-10-19T11:27:59Z).
Prior snapshot for drift: snapshots/2026-10-15/str_licenses.parquet and its
cleaned, parcel-bridged layer layers/str_licenses_clean.parquet.

Conventions (see brief Methods):
- ACTIVE basis, used everywhere unless a figure is labeled register-wide:
  LICENSE_STATUS == "License Issued - Active" exactly. Delinquent,
  About to Expire, and Closed rows are never merged into "active".
- Holder identity: ENTITY_NAME normalized (uppercase, whitespace collapsed).
  Concentration is computed on that normalized name. Name-merge sensitivities
  (first+last token; first-initial+surname over-merge) are computed alongside.
- Classification (individual vs business entity) is a NAME classification,
  not a determination of beneficial ownership. Rule: tokenize the normalized
  name on non-letters; BUSINESS if any token is in BUSINESS_TOKENS; else
  INDIVIDUAL if the name is 2-5 alphabetic tokens (initials and generational
  suffixes allowed); else NOT DETERMINED. Denominator is ALL active
  licenses (or ALL active holders); shares sum to 100 percent by
  construction and the not-determined share is printed.
- Parcel bridge for the fresh snapshot: schednum inherited from the
  2026-10-15 cleaned layer by LICENSE_NUM (2,337 of 2,338 rows); the single
  license that entered after 2026-10-15 is key-matched on its PARCEL_NUM
  (zfill to 13) against parcel spine v6. The 3 rows the Phase 3 bridge left
  unmatched stay unmatched. Neighborhood = spine v6 neighborhood of the
  assigned parcel.
- Rates: active licenses per 1,000 ACS 2020-2024 5-year housing units
  (warehouse layer acs_neighborhood_units.parquet; same denominators as the
  October 17 and 18 briefs).
- No licensee name or street address is written to any output file.
"""
import json
import re
from collections import Counter

import numpy as np
import pandas as pd

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
ACTIVE = "License Issued - Active"
PULL_DATE = "2026-10-19"

raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-19/str_licenses.parquet")
old_raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-15/str_licenses.parquet")
clean = pd.read_parquet(f"{STACK}/layers/str_licenses_clean.parquet")
spine = pd.read_parquet(f"{STACK}/joins/parcel_spine_v6.parquet")
acs = pd.read_parquet(f"{STACK}/layers/acs_neighborhood_units.parquet")

S = {}
S["meta"] = {
    "dataset": "ODC_short_term_rental_licenses_active_or_pending_renewal (Denver Open Data, ArcGIS FeatureServer layer 54)",
    "publisher": "Department of Licensing and Consumer Protection (DLCP), City and County of Denver (formerly Excise and Licenses; the dataset is still published under the Excise and Licenses name)",
    "snapshot": "warehouse snapshots/2026-10-19/str_licenses.parquet (pulled 2026-10-19T11:27:59Z)",
    "prior_snapshot": "warehouse snapshots/2026-10-15/str_licenses.parquet (pulled 2026-10-15)",
    "active_basis": "LICENSE_STATUS == 'License Issued - Active' exactly; no other status is counted as active",
    "holder_key": "ENTITY_NAME normalized: uppercase, whitespace collapsed, punctuation spacing normalized",
    "acs_denver_county_units": 359581,
    "acs_units_allocated_to_neighborhoods": float(acs["acs_units_2020_2024"].sum()),
    "product_rule": "aggregates only in every shipped file category (brief and social markdown, stats.json, data/, code/, charts/, hero): no licensee name, street address, parcel number, or TAX_ID value in any output; the raw register snapshot lives only in the warehouse, never in the package (fix loop F-1, 2026-10-19)",
}

# ---------- register totals ----------
status_counter = {str(k): int(v) for k, v in raw["LICENSE_STATUS"].value_counts(dropna=False).items()}
S["register"] = {
    "rows": int(len(raw)),
    "status_counter": status_counter,
    "status_shares_pct": {k: round(v / len(raw) * 100, 2) for k, v in status_counter.items()},
    "license_type_counter": {str(k): int(v) for k, v in raw["LICENSE_TYPE"].value_counts(dropna=False).items()},
    "distinct_license_nums": int(raw["LICENSE_NUM"].nunique()),
}
assert sum(status_counter.values()) == len(raw)

# ---------- drift vs 2026-10-15 ----------
new_ids, old_ids = set(raw["LICENSE_NUM"]), set(old_raw["LICENSE_NUM"])
both = raw.set_index("LICENSE_NUM").join(
    old_raw.set_index("LICENSE_NUM"), lsuffix="_new", rsuffix="_old", how="inner")
transitions = {}
for (o, n), c in both.groupby(["LICENSE_STATUS_old", "LICENSE_STATUS_new"]).size().items():
    transitions[f"{o} -> {n}"] = int(c)
old_counter = {str(k): int(v) for k, v in old_raw["LICENSE_STATUS"].value_counts(dropna=False).items()}
S["drift_vs_2026_10_15"] = {
    "prior_rows": int(len(old_raw)),
    "prior_status_counter": old_counter,
    "rows_change": int(len(raw) - len(old_raw)),
    "active_change": int(status_counter[ACTIVE] - old_counter[ACTIVE]),
    "entered_license_nums": int(len(new_ids - old_ids)),
    "left_license_nums": int(len(old_ids - new_ids)),
    "continuing_license_nums": int(len(new_ids & old_ids)),
    "status_transitions_continuing": transitions,
    "entity_name_changes_continuing": int((both["ENTITY_NAME_new"] != both["ENTITY_NAME_old"]).sum()),
    "parcel_num_changes_continuing": int(
        (both["PARCEL_NUM_new"].astype(str) != both["PARCEL_NUM_old"].astype(str)).sum()),
}

# ---------- parcel bridge for the fresh snapshot ----------
bridge = clean.set_index("LICENSE_NUM")[["schednum", "match_method"]]
df = raw.copy()
df["schednum"] = df["LICENSE_NUM"].map(bridge["schednum"])
df["match_method"] = df["LICENSE_NUM"].map(bridge["match_method"])
spine_sched = set(spine["schednum"])
unbridged = df[df["match_method"].isna()]
assert len(unbridged) == S["drift_vs_2026_10_15"]["entered_license_nums"]
for idx, r in unbridged.iterrows():
    pnum = str(r["PARCEL_NUM"])
    key = pnum.zfill(13) if pnum.isdigit() else None
    assert key in spine_sched, f"entered row key not in spine: {r['LICENSE_NUM']}"
    df.loc[idx, "schednum"] = key
    df.loc[idx, "match_method"] = "key (fresh, PARCEL_NUM)"
match_counter = {str(k): int(v) for k, v in df["match_method"].value_counts(dropna=False).items()}
S["parcel_bridge_fresh"] = {
    "match_counter": match_counter,
    "matched_rows": int(df["schednum"].notna().sum()),
    "unmatched_rows": int(df["schednum"].isna().sum()),
    "match_rate_pct": round(df["schednum"].notna().mean() * 100, 2),
    "note": "2,337 rows inherit the Phase 3 bridge by LICENSE_NUM; 1 entered row key-matched on PARCEL_NUM; the 3 Phase 3 unmatched rows remain unmatched",
}
nb_map = spine.set_index("schednum")["neighborhood"]
df["neighborhood"] = df["schednum"].map(nb_map)

# ---------- holder normalization + classification ----------
def norm_name(s):
    s = str(s).upper().strip()
    s = re.sub(r"\s+", " ", s)
    return s

df["holder"] = df["ENTITY_NAME"].map(norm_name)

BUSINESS_TOKENS = {
    "LLC", "INC", "LTD", "CORP", "CORPORATION", "LLP", "LLLP", "LP", "PC", "PLLC",
    "COMPANY", "CO", "TRUST", "HOLDINGS", "HOLDING", "PROPERTIES", "PROPERTY",
    "REALTY", "VENTURES", "VENTURE", "PARTNERS", "PARTNERSHIP", "GROUP", "CAPITAL",
    "INVESTMENTS", "INVESTMENT", "ENTERPRISES", "ENTERPRISE", "MANAGEMENT",
    "ESTATES", "HOMES", "RENTALS", "RENTAL", "FOUNDATION", "ASSOCIATION", "ASSOC",
    "BANK", "CHURCH", "UNIVERSITY", "COLLEGE", "HOSPITAL", "HOTEL", "SUITES",
    "APARTMENTS", "RESIDENCES", "DEVELOPMENT", "CONSTRUCTION", "CLUB", "SOCIETY",
    "MINISTRY", "SCHOOL", "DISTRICT", "AUTHORITY", "AGENCY", "SERVICES", "SOLUTIONS",
    "CONSULTING", "GLOBAL", "INTERNATIONAL",
}
SUFFIX_TOKENS = {"JR", "SR", "II", "III", "IV", "MD", "DDS", "ESQ", "PHD"}

def classify(name):
    toks = re.findall(r"[A-Z]+(?:'[A-Z]+)?", name)
    if any(t in BUSINESS_TOKENS for t in toks):
        return "business_entity_name"
    if 2 <= len(toks) <= 5 and all(t.replace("'", "").isalpha() for t in toks):
        return "individual_name"
    return "not_determined"

df["name_class"] = df["holder"].map(classify)

def classification_block(frame, unit_label):
    n = len(frame)
    c = frame["name_class"].value_counts(dropna=False)
    out = {unit_label: int(n)}
    for k in ["individual_name", "business_entity_name", "not_determined"]:
        cnt = int(c.get(k, 0))
        out[k] = {"count": cnt, "share_pct": round(cnt / n * 100, 2) if n else None}
    assert sum(out[k]["count"] for k in ["individual_name", "business_entity_name", "not_determined"]) == n
    assert abs(sum(out[k]["share_pct"] for k in out if isinstance(out.get(k), dict)) - 100.0) < 0.02 or n == 0
    return out

act = df[df["LICENSE_STATUS"] == ACTIVE].copy()
S["classification_active_licenses"] = classification_block(act, "licenses")
holders_act = act.drop_duplicates("holder")
S["classification_active_holders"] = classification_block(holders_act, "holders")
S["classification_register_licenses"] = classification_block(df, "licenses")
S["classification_rule"] = {
    "business_tokens": sorted(BUSINESS_TOKENS),
    "rule": "business if any name token is a business token; else individual if 2-5 alphabetic tokens; else not determined",
    "scope": "classification of the ENTITY_NAME string as filed, not of beneficial ownership",
}

# ---------- concentration ----------
def concentration(frame, label):
    vc = frame["holder"].value_counts()
    n_lic, n_hold = int(len(frame)), int(len(vc))
    counts = sorted(vc.tolist(), reverse=True)
    bands = {"1": 0, "2": 0, "3-5": 0, "6-10": 0, "11+": 0}
    band_lic = {"1": 0, "2": 0, "3-5": 0, "6-10": 0, "11+": 0}
    for c in counts:
        b = "1" if c == 1 else "2" if c == 2 else "3-5" if c <= 5 else "6-10" if c <= 10 else "11+"
        bands[b] += 1
        band_lic[b] += c

    def top_share(k):
        return round(sum(counts[:k]) / n_lic * 100, 2)
    return {
        "basis": label,
        "licenses": n_lic,
        "distinct_holders": n_hold,
        "max_licenses_per_holder": int(max(counts)),
        "holders_by_band": bands,
        "licenses_by_band": band_lic,
        "top_shares_pct_of_licenses": {
            "top_1": top_share(1), "top_5": top_share(5),
            "top_10": top_share(10), "top_25": top_share(25),
        },
        "share_held_by_holders_with_2plus_pct": round(sum(c for c in counts if c >= 2) / n_lic * 100, 2),
        "share_held_by_holders_with_5plus_pct": round(sum(c for c in counts if c >= 5) / n_lic * 100, 2),
        "licenses_whose_holder_has_exactly_1": int(sum(c for c in counts if c == 1)),
        "share_whose_holder_has_exactly_1_pct": round(sum(c for c in counts if c == 1) / n_lic * 100, 2),
        "holders_with_exactly_1": int(sum(1 for c in counts if c == 1)),
        "holders_with_2": int(sum(1 for c in counts if c == 2)),
    }

S["concentration_active"] = concentration(act, "active licenses (LICENSE_STATUS = License Issued - Active)")
S["concentration_register"] = concentration(df, "all register rows, every status")

# name-merge sensitivities (active)
def first_last(name):
    toks = re.findall(r"[A-Z]+", name)
    return (toks[0], toks[-1]) if len(toks) >= 2 else (name,)

def initial_surname(name):
    toks = re.findall(r"[A-Z]+", name)
    return (toks[0][0], toks[-1]) if len(toks) >= 2 else (name,)

for key, fn in [("first_last_token_merge", first_last), ("initial_surname_overmerge", initial_surname)]:
    vc2 = act["holder"].map(fn).value_counts()
    S.setdefault("name_merge_sensitivity_active", {})[key] = {
        "distinct_groups": int(len(vc2)),
        "max_licenses_per_group": int(vc2.max()),
        "groups_with_2plus": int((vc2 >= 2).sum()),
        "licenses_in_groups_with_2plus": int(vc2[vc2 >= 2].sum()),
        "distribution": {str(k): int(v) for k, v in vc2.value_counts().sort_index().items()},
    }

# ---------- parcels ----------
def parcel_block(frame, label):
    g = frame.dropna(subset=["schednum"]).groupby("schednum").size()
    dist = {str(k): int(v) for k, v in g.value_counts().sort_index().items()}
    return {
        "basis": label,
        "licenses_with_parcel": int(frame["schednum"].notna().sum()),
        "licenses_without_parcel": int(frame["schednum"].isna().sum()),
        "distinct_parcels": int(len(g)),
        "parcels_with_multiple_licenses": int((g >= 2).sum()),
        "max_licenses_on_one_parcel": int(g.max()),
        "licenses_on_multiple_license_parcels": int(g[g >= 2].sum()),
        "parcel_size_distribution_parcels_by_license_count": dist,
        "largest_parcel_neighborhood": str(nb_map.get(g.idxmax())),
        "largest_parcel_units_on_parcel_record": (
            None if pd.isna(spine.set_index("schednum").loc[g.idxmax(), "TOT_UNITS"])
            else float(spine.set_index("schednum").loc[g.idxmax(), "TOT_UNITS"])),
    }

S["parcels_active"] = parcel_block(act, "active licenses")
_mp = act.dropna(subset=["schednum"]).groupby("schednum").agg(
    lic=("LICENSE_NUM", "nunique"), holders=("holder", "nunique"))
_mp = _mp[_mp["lic"] >= 2]
S["multi_parcel_holder_check"] = {
    "multi_license_parcels_active": int(len(_mp)),
    "licenses_on_those_parcels": int(_mp["lic"].sum()),
    "parcels_where_every_license_has_a_distinct_holder": int((_mp["lic"] == _mp["holders"]).sum()),
    "note": "on every multi-license parcel, each license sits under a different holder name; parcel stacking is not holder stacking",
}
S["parcels_register"] = parcel_block(df, "all register rows")
# same-address check (active): normalized address string
act_addr = act["ADDRESS"].astype(str).str.upper().str.strip().str.replace(r"\s+", " ", regex=True)
va = act_addr.value_counts()
S["address_check_active"] = {
    "distinct_address_strings": int(len(va)),
    "max_licenses_at_one_address_string": int(va.max()),
    "address_strings_with_2plus": int((va >= 2).sum()),
    "note": "address strings keep unit identity; condo units at one building address are distinct strings when the unit is in the address",
}

# ---------- base-address rollup (fix loop F-4, 2026-10-19) ----------
# Building-level view the parcel rollup cannot give: condo units are
# individual parcels, so a building must be recovered from the address.
# Normalization: uppercase, punctuation removed, whitespace collapsed;
# then strip a trailing unit designator systematically - a named
# designator (UNIT/APT/APARTMENT/STE/SUITE/BLDG/BUILDING/FL/FLOOR/RM/ROOM
# or #) plus its identifier, or a bare trailing unit token (digits,
# digits+letter, or a single letter) following a street-suffix token.
_STREET_SUFFIXES = {"ST", "STREET", "AVE", "AVENUE", "BLVD", "BOULEVARD", "CT", "COURT",
                    "PL", "PLACE", "WAY", "DR", "DRIVE", "LN", "LANE", "CIR", "CIRCLE",
                    "PKWY", "PARKWAY", "RD", "ROAD", "HWY", "TRL", "TRAIL", "TER", "TERRACE"}
_DESIGNATORS = r"(?:UNIT|APT|APARTMENT|STE|SUITE|BLDG|BUILDING|FL|FLOOR|RM|ROOM)"

def base_address(s):
    s = re.sub(r"[.,]", " ", str(s).upper().strip())
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"#\s*[A-Z0-9-]+\s*$", "", s).strip()
    s = re.sub(rf"\b{_DESIGNATORS}\s*[A-Z0-9-]+\s*$", "", s).strip()
    t = s.split()
    if (len(t) >= 3 and t[-2] in _STREET_SUFFIXES and t[-1] not in _STREET_SUFFIXES
            and t[-1] not in {"N", "S", "E", "W"}
            and re.fullmatch(r"\d+[A-Z]?|[A-Z]", t[-1])):
        s = " ".join(t[:-1])
    return s

act_base = act.copy()
act_base["base_address"] = act_base["ADDRESS"].map(base_address)
_bg = act_base.groupby("base_address").agg(
    lic=("LICENSE_NUM", "nunique"), parcels=("schednum", "nunique"),
    holders=("holder", "nunique"))
_bm = _bg[_bg["lic"] >= 2]
S["base_address_rollup_active"] = {
    "basis": "active licenses grouped by normalized base address (unit designators stripped; see build code)",
    "distinct_base_addresses": int(len(_bg)),
    "base_addresses_with_multiple_licenses": int(len(_bm)),
    "licenses_on_multiple_license_base_addresses": int(_bm["lic"].sum()),
    "share_of_active_pct": round(float(_bm["lic"].sum()) / len(act) * 100, 2),
    "max_licenses_at_one_base_address": int(_bg["lic"].max()),
    "multi_base_addresses_spanning_multiple_parcels": int((_bm["parcels"] > 1).sum()),
    "multi_base_addresses_on_a_single_parcel": int((_bm["parcels"] == 1).sum()),
    "every_license_a_distinct_holder_within_each_multi_group": bool((_bm["lic"] == _bm["holders"]).all()),
    "size_distribution_base_addresses_by_license_count": {
        str(k): int(v) for k, v in _bm["lic"].value_counts().sort_index().items()},
    "note": "a reviewer's crude rollup (UNIT/APT/STE/# designators only) gives 19 base addresses, 63 licenses, max 17, 13 spanning more than one parcel; the proper normalization also strips BLDG designators and bare trailing unit numbers, merging 124 more unit-variant addresses and so finding more building-level groups; the maximum (17) is the same under both",
}

# ---------- the TOT_UNITS=1 multi-license parcel (fix loop F-4) ----------
_spine_by_sched = spine.set_index("schednum")
_pg = act.dropna(subset=["schednum"]).groupby("schednum").size()
_t1_sched = [s for s in _pg[_pg >= 2].index if _spine_by_sched.loc[s, "TOT_UNITS"] == 1]
assert len(_t1_sched) == 1
_t1 = _spine_by_sched.loc[_t1_sched[0]]
_t1_rows = act[act["schednum"] == _t1_sched[0]]
S["tot_units_1_parcel"] = {
    "licenses_on_parcel": int(_pg[_t1_sched[0]]),
    "distinct_holders": int(_t1_rows["holder"].nunique()),
    "distinct_raw_address_strings": int(_t1_rows["ADDRESS"].nunique()),
    "distinct_base_addresses": int(_t1_rows["ADDRESS"].map(base_address).nunique()),
    "all_licenses_addresses_carry_a_unit_designator": bool(
        clean.set_index("LICENSE_NUM")["has_unit_in_address"].reindex(_t1_rows["LICENSE_NUM"]).all()),
    "spine_record": {
        "TOT_UNITS": float(_t1["TOT_UNITS"]),
        "PROP_CLASS": str(_t1["PROP_CLASS"]),
        "D_CLASS_CN": str(_t1["D_CLASS_CN"]),
        "neighborhood": str(_t1["neighborhood"]),
        "LAND_AREA_sqft": float(_t1["LAND_AREA"]),
        "has_characteristics": bool(_t1["has_characteristics"]),
    },
    "parcels_record": {
        "appendage": "999 (the master-parcel appendage)",
        "structure_type": "107: CONDO (FEE SIMPLE)",
        "gross_area_sqft": 126465.0,
        "commercial_original_year_built": 2018.0,
        "legal_description_reading": "the legal description identifies the parcel as the master parcel of a condominium development",
    },
    "reading": "TOT_UNITS=1 sits on the master parcel record of a condominium development, not on a single-unit house record; the four licenses are four unit filings by four different holders whose addresses carry unit designators, assigned to the master parcel by the bridge. No address or parcel number is printed (product rule).",
}

# ---------- neighborhoods ----------
units = dict(zip(acs["neighborhood"], acs["acs_units_2020_2024"]))
cnt = act["neighborhood"].value_counts(dropna=True)
panel = pd.DataFrame({"neighborhood": sorted(units.keys())})
panel["acs_units"] = panel["neighborhood"].map(units)
panel["active_licenses"] = panel["neighborhood"].map(cnt).fillna(0).astype(int)
panel["licenses_per_1000_units"] = (panel["active_licenses"] / panel["acs_units"] * 1000).round(2)
# permit aggregates by neighborhood from spine v6 (surviving basis)
agg = spine.groupby("neighborhood").agg(
    new_building_permits=("new_building_permit_count", "sum"),
    demolitions=("demolition_count", "sum")).reset_index()
panel = panel.merge(agg, on="neighborhood", how="left")
panel["new_building_permits_per_1000_units"] = (panel["new_building_permits"] / panel["acs_units"] * 1000).round(2)
panel["demolitions_per_1000_units"] = (panel["demolitions"] / panel["acs_units"] * 1000).round(2)
panel = panel.sort_values("neighborhood").reset_index(drop=True)
panel.to_csv(f"{PKG}/data/neighborhood_panel.csv", index=False)

zero_nb = sorted(panel.loc[panel["active_licenses"] == 0, "neighborhood"].tolist())
top_count = panel.nlargest(12, "active_licenses")[["neighborhood", "active_licenses", "acs_units", "licenses_per_1000_units"]]
top_rate = panel.nlargest(12, "licenses_per_1000_units")[["neighborhood", "active_licenses", "acs_units", "licenses_per_1000_units"]]
S["neighborhoods"] = {
    "active_licenses_with_neighborhood": int(act["neighborhood"].notna().sum()),
    "active_licenses_without_neighborhood": int(act["neighborhood"].isna().sum()),
    "neighborhoods_total": int(len(panel)),
    "neighborhoods_with_1plus_active": int((panel["active_licenses"] > 0).sum()),
    "neighborhoods_with_zero_active": int((panel["active_licenses"] == 0).sum()),
    "zero_active_neighborhoods": zero_nb,
    "citywide_active_per_1000_units": round(len(act) / panel["acs_units"].sum() * 1000, 2),
    "top_by_count": top_count.to_dict("records"),
    "top_by_rate_per_1000": top_rate.to_dict("records"),
    "top5_count_share_pct": round(panel.nlargest(5, "active_licenses")["active_licenses"].sum() / len(act) * 100, 1),
    "top10_count_share_pct": round(panel.nlargest(10, "active_licenses")["active_licenses"].sum() / len(act) * 100, 1),
    "median_neighborhood_rate_per_1000": round(float(panel["licenses_per_1000_units"].median()), 2),
    "median_neighborhood_rate_basis": "median across all 78 neighborhoods, zero-license neighborhoods counted as 0 (verifier ledger row 69; fix loop 2026-10-19)",
    "median_neighborhood_rate_per_1000_neighborhoods_with_licenses_only": round(
        float(panel.loc[panel["active_licenses"] > 0, "licenses_per_1000_units"].median()), 2),
    "dia_active_licenses": int(panel.loc[panel["neighborhood"] == "DIA", "active_licenses"].iloc[0]),
}

# ---------- vintage + expiry hygiene ----------
act_dates = act.copy()
act_dates["orig_year"] = pd.to_datetime(
    act_dates["ORIG_ISSUED_DATE"], unit="ms", utc=True).dt.tz_convert("America/Denver").dt.year
vint = act_dates["orig_year"].value_counts().sort_index()
S["vintage_active"] = {
    "originally_issued_by_year": {str(int(k)): int(v) for k, v in vint.items()},
    "share_issued_2023_or_later_pct": round(float((act_dates["orig_year"] >= 2023).mean() * 100), 1),
    "share_issued_2025_2026_pct": round(float((act_dates["orig_year"] >= 2025).mean() * 100), 1),
}
exp = pd.to_datetime(df["EXPIRATION_DATE"], format="mixed")
df["exp_date"] = exp
act_exp = df[df["LICENSE_STATUS"] == ACTIVE]
_a47 = act_exp[act_exp["exp_date"] < PULL_DATE].copy()
_a47["recent_year"] = pd.to_datetime(
    _a47["MOST_RECENTLY_ISSUED_DATE"], unit="ms", utc=True).dt.tz_convert("America/Denver").dt.year
_a47["lag_days"] = (pd.Timestamp(PULL_DATE) - _a47["exp_date"]).dt.days
_a47_recent_dt = pd.to_datetime(_a47["MOST_RECENTLY_ISSUED_DATE"], unit="ms", utc=True).dt.tz_localize(None)
S["expiry_hygiene"] = {
    "active_licenses_with_expiration_before_pull_date": int(len(_a47)),
    "share_of_active_pct": round(float((act_exp["exp_date"] < PULL_DATE).mean() * 100), 2),
    "about_to_expire_rows": int((df["LICENSE_STATUS"] == "About to Expire").sum()),
    "past_expiration_cross_tab": {
        "most_recently_issued_year_distribution": {
            str(int(k)): int(v) for k, v in _a47["recent_year"].value_counts().sort_index().items()},
        "most_recently_issued_in_2025_2026": int(_a47["recent_year"].isin([2025, 2026]).sum()),
        "reissued_after_printed_expiration_date": int((_a47_recent_dt > _a47["exp_date"]).sum()),
        "expiration_lag_days_median": float(_a47["lag_days"].median()),
        "expiration_lag_days_max": int(_a47["lag_days"].max()),
        "expiration_lag_over_one_year": int((_a47["lag_days"] > 365).sum()),
    },
    "note": "status and expiration fields are recorded as published; a past expiration date on an active-status row is a field disagreement in the register, printed without a compliance claim (cross-tab added in fix loop F-6, 2026-10-19)",
}

# ---------- fusion: permits layer ----------
def spearman(a, b):
    ra = pd.Series(np.asarray(a, dtype=float)).rank()
    rb = pd.Series(np.asarray(b, dtype=float)).rank()
    return round(float(np.corrcoef(ra, rb)[0, 1]), 3)

f = panel[(panel["neighborhood"] != "DIA") & (panel["acs_units"] >= 1000)].copy()
f_all = panel[panel["acs_units"] >= 1000].copy()
str_parcels = set(act["schednum"].dropna())
spine2 = spine.copy()
spine2["is_str_parcel"] = spine2["schednum"].isin(str_parcels)
res_like = spine2[spine2["has_characteristics"]]
S["fusion_permits"] = {
    "layering_claim": "STR licenses and recent construction concentrate in the same neighborhoods; the claim needs the permits layer joined on the parcel spine and cannot be made from the license register alone",
    "neighborhoods_compared": int(len(f)),
    "spearman_str_rate_vs_new_building_permit_rate": spearman(f["licenses_per_1000_units"], f["new_building_permits_per_1000_units"]),
    "spearman_str_count_vs_new_building_permit_count": spearman(f["active_licenses"], f["new_building_permits"]),
    "spearman_str_rate_vs_new_building_permit_rate_incl_dia": spearman(f_all["licenses_per_1000_units"], f_all["new_building_permits_per_1000_units"]),
    "top10_rate_overlap": sorted(set(panel.nlargest(10, "licenses_per_1000_units")["neighborhood"])
                                 & set(panel[panel["neighborhood"] != "DIA"].nlargest(10, "new_building_permits_per_1000_units")["neighborhood"])),
    "permit_window": "new-building permits issued 2020-01-01 to 2026-10-12, surviving-parcel basis (spine v6), as built for the October 15, 2026 net housing change brief",
    "str_parcels_with_new_building_permit_pct": round(float(spine2.loc[spine2["is_str_parcel"], "new_building_permit_count"].gt(0).mean() * 100), 1),
    "residential_parcels_with_new_building_permit_pct": round(float(res_like["new_building_permit_count"].gt(0).mean() * 100), 1),
    "str_parcels_with_demolition_pct": round(float(spine2.loc[spine2["is_str_parcel"], "demolition_count"].gt(0).mean() * 100), 1),
    "residential_parcels_with_demolition_pct": round(float(res_like["demolition_count"].gt(0).mean() * 100), 1),
    "str_parcel_count": int(len(str_parcels)),
    "residential_parcel_count": int(len(res_like)),
    "caveat": "parcel-level permit prevalence compares parcels as they stand at the 2026-10-15 spine snapshot; a permit on the parcel does not date the license, and no causal direction is claimed",
}

with open(f"{PKG}/stats.json", "w") as fh:
    json.dump(S, fh, indent=1)
print(json.dumps({k: S[k] for k in ["register", "concentration_active", "classification_active_licenses"]}, indent=1))
print("neighborhoods:", S["neighborhoods"]["neighborhoods_with_1plus_active"], "with 1+, zero:", S["neighborhoods"]["zero_active_neighborhoods"])
print("parcels active:", S["parcels_active"])
print("fusion rho:", S["fusion_permits"]["spearman_str_rate_vs_new_building_permit_rate"],
      "| counts rho:", S["fusion_permits"]["spearman_str_count_vs_new_building_permit_count"])
print("stats.json written")
