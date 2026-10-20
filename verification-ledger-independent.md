# Independent Verification Ledger — Denver STR Licenses Brief (2026-10-19)

Verifier: independent subagent pass, brief-writing standards §11.1 step 3 / §11.2 (method diversity).
Method: figures recomputed from the RAW warehouse snapshots with the verifier's own
implementation (script preserved at /tmp/verify_str.py in the verifier session; logic
written independently of code/build_stats.py — builder code was read only for the
claims list via stats.json / brief-draft.md). No licensee names or street addresses
appear in this ledger; name-field results are reported as patterns and counts only.

Sources of truth used:
- Fresh snapshot: stack/denver/snapshots/2026-10-19/str_licenses.parquet
- Prior snapshot: stack/denver/snapshots/2026-10-15/str_licenses.parquet
- Cleaned bridge layer: stack/denver/layers/str_licenses_clean.parquet (schednum by LICENSE_NUM)
- Parcel spine: stack/denver/joins/parcel_spine_v6.parquet (neighborhood, TOT_UNITS, permit counts)
- ACS: stack/denver/layers/acs_neighborhood_units.parquet
- Package panel: data/neighborhood_panel.csv (for the Spearman cross-check pair)
- Package working copy data/str_licenses_raw_2026-10-19.parquet: 2,338 rows, LICENSE_NUM set identical to the warehouse fresh snapshot.

Environment note: the specified venv (~/workspace/denver-housing-permits/.venv) had
pandas 3.0.6 but no pyarrow in this session; pyarrow 26.0.0 was installed to a
throwaway /tmp target and layered via PYTHONPATH. The builder's environment and
files were not modified.

## Ledger

| # | Figure | Claimed | Recomputed | Verdict |
|---|--------|---------|------------|---------|
| 1 | Fresh register rows | 2,338 | 2,338 | reproduced |
| 2 | Active ("License Issued - Active") | 2,083 | 2,083 | reproduced |
| 3 | Delinquent | 137 | 137 | reproduced |
| 4 | Closed - Expired | 116 | 116 | reproduced |
| 5 | About to Expire | 1 | 1 | reproduced |
| 6 | Closed - Surrendered | 1 | 1 | reproduced |
| 7 | Status counter sums to total | 2,338 | 2,338 (5 statuses, exhaustive) | reproduced |
| 8 | Distinct LICENSE_NUM, fresh | 2,338 | 2,338 | reproduced |
| 9 | LICENSE_TYPE all "Short Term Rental" | 2,338 | 2,338 | reproduced |
| 10 | ENTITY_NAME nulls, fresh | 0 | 0 | reproduced |
| 11 | PARCEL_NUM length mix | 2,336×13-digit, 1×12-digit, 1 dashed | 13: 2,336; 12: 1; 16: 1 | reproduced |
| 12 | Prior rows 2026-10-15 | 2,349 | 2,349 | reproduced |
| 13 | Prior active | 2,098 | 2,098 | reproduced |
| 14 | Prior Delinquent | 133 | 133 | reproduced |
| 15 | Drift: license numbers left | 12 | 12 | reproduced |
| 16 | Drift: license numbers entered | 1 | 1 | reproduced |
| 17 | Drift: continuing | 2,337 | 2,337 | reproduced |
| 18 | Transition Active→Delinquent | 7 | 7 | reproduced |
| 19 | Transition Delinquent→Active | 2 | 2 | reproduced |
| 20 | Transition Delinquent→Closed-Expired | 1 | 1 | reproduced |
| 21 | Transition Active→Active | 2,080 | 2,080 | reproduced |
| 22 | All other transition cells (A→A-exp 1, CE→CE 115, CS→CS 1, D→D 130) | as stats.json | identical, all 8 cells | reproduced |
| 23 | ENTITY_NAME changes among continuing | 0 | 0 | reproduced |
| 24 | PARCEL_NUM changes among continuing | 0 | 0 | reproduced |
| 25 | Finding 5 drift decomposition (11 active left, 7 A→D, 2 D→A, 1 entered as Active; entered row's status = Active; of 12 left, 11 were Active, 1 Closed-Expired) | as brief | exact match on every component | reproduced |
| 26 | Active distinct holders | 2,080 | 2,080 | reproduced |
| 27 | Active holders by band (1 / 2 / 3-5 / 6-10 / 11+) | 2,077 / 3 / 0 / 0 / 0 | 2,077 / 3 / 0 / 0 / 0 | reproduced |
| 28 | Max licenses per holder (active) | 2 | 2 | reproduced |
| 29 | Top-1 share of active licenses | 0.10% (2) | 0.10% (2) | reproduced |
| 30 | Top-5 share | 0.38% (8) | 0.38% (8) | reproduced |
| 31 | Top-10 share | 0.62% (13) | 0.62% (13) | reproduced |
| 32 | Top-25 share | 1.34% (28) | 1.34% (28) | reproduced |
| 33 | Share of licenses that are holder's only license | 99.71% (2,077) | 99.71% (2,077) | reproduced |
| 34 | Share held by holders with 2+ | 0.29% | 0.29% (6 licenses) | reproduced |
| 35 | Register-wide distinct holders | 2,333 | 2,333 | reproduced |
| 36 | Register-wide max per holder / bands | 2; 2,328 with 1, 5 with 2 | 2; 2,328 / 5 | reproduced |
| 37 | Business-entity names, active licenses (builder rule) | 0 (0.0%) | 0 under verifier's own rule (see §Classification) | reproduced |
| 38 | Business-entity names, active holders | 0 (0.0%) | 0 | reproduced |
| 39 | Business-entity names, full register | 0 (0.0%) | 0 | reproduced |
| 40 | Not-determined, all bases | 0 (0.0%) | 0 — every active name is 2–5 alphabetic tokens (histogram: 2:1,969; 3:103; 4:10; 5:1) | reproduced |
| 41 | First+last-token merge: groups / max | 2,080 / 2 | 2,080 / 2 (same 3 pairs, 6 licenses) | reproduced |
| 42 | Over-merge (first initial + surname): groups | 2,034 | 2,034 | reproduced |
| 43 | Over-merge: max per group | 4 | 4 | reproduced |
| 44 | Over-merge: licenses in groups of 2+ | 92 (4.4%) | 92 (4.42%); distribution 1:1,991 / 2:39 / 3:2 / 4:2 | reproduced |
| 45 | Distinct address strings, active / max per string / strings with 2+ | 2,082 / 2 / 1 | 2,082 / 2 / 1 | reproduced |
| 46 | Active licenses with parcel | 2,080 (3 without) | 2,080 (3 without) | reproduced |
| 47 | Active distinct parcels | 2,008 | 2,008 | reproduced |
| 48 | Parcels with 2+ active licenses | 12 | 12 | reproduced |
| 49 | Licenses on multi-license parcels | 84 | 84 | reproduced |
| 50 | Max active licenses on one parcel | 32 | 32 | reproduced |
| 51 | Parcel size distribution (parcels by license count) | 1:1,996; 2:3; 3:4; 4:1; 6:2; 18:1; 32:1 | identical | reproduced |
| 52 | Multi-license parcels where every license has a distinct holder | 12 of 12 (84 licenses, 84 holders) | 12 of 12 | reproduced |
| 53 | Largest parcel: neighborhood / units on record | Union Station / 579 | Union Station / 579.0 (spine TOT_UNITS) | reproduced |
| 54 | Register parcels: distinct / 2+ / max / licenses on multi | 2,255 / 13 / 35 / 93 | 2,255 / 13 / 35 / 93 | reproduced |
| 55 | Register licenses with parcel | 2,335 | 2,335 | reproduced |
| 56 | Active licenses with neighborhood | 2,080 / 2,083 = 99.9% | 2,080 (99.86%) | reproduced |
| 57 | Neighborhoods with 1+ active, of 78 | 75 | 75 | reproduced |
| 58 | Zero-license neighborhoods | Auraria, Kennedy, Sun Valley | Auraria, Kennedy, Sun Valley (exact set) | reproduced |
| 59 | Top counts: Five Points / Highland / West Colfax / Berkeley / Sunnyside | 151 / 112 / 105 / 88 / 88 | 151 / 112 / 105 / 88 / 88 | reproduced |
| 60 | Top-5 neighborhoods' share of active | 26.1% (544) | 26.12% (544) | reproduced |
| 61 | Top-10 share | 41.5% | 41.53% | reproduced |
| 62 | Whittier rate per 1,000 | 27.1 (61 licenses) | 27.10 (61; ACS 2,251.0) | reproduced |
| 63 | Cole rate | 24.8 (stats 24.75) | 24.75 (50 licenses) | reproduced |
| 64 | Skyland rate | 19.7 (stats 19.73) | 19.73 (35) | reproduced |
| 65 | Clayton rate | 19.1 (stats 19.12) | 19.12 (35) | reproduced |
| 66 | Berkeley rate | 18.4 (stats 18.38) | 18.38 (88) | reproduced |
| 67 | Citywide rate per 1,000 | 5.8 | 5.797 on builder basis (2,083 / 359,351.5 allocated units); 5.788 on assigned-only numerator — both round to 5.8 | reproduced |
| 68 | ACS allocated units total | 359,351 (county 359,581) | 359,351.5 allocated across 78 neighborhoods | reproduced |
| 69 | Median neighborhood rate | 4.7 per 1,000 (stats 4.71) | 4.71 computed over ALL 78 neighborhoods (zero-license counted as 0). Over the 75 with licenses only it would be 5.04. The brief does not state the basis. | caveated (value correct on all-78 basis; basis unstated in brief) |
| 70 | Whittier = 4.7× citywide | 4.7× | 4.68× | reproduced |
| 71 | Vintage by ORIG_ISSUED year (America/Denver), active | 2016:31; 2017:73; 2018:65; 2019:129; 2020:88; 2021:179; 2022:247; 2023:258; 2024:247; 2025:401; 2026:365 | identical, all 11 years | reproduced |
| 72 | Share issued 2023+ | 61.0% | 61.02% | reproduced |
| 73 | Share issued 2025–2026 | 36.8% | 36.77% | reproduced |
| 74 | Active licenses with expiration before pull date | 47 (2.26%; brief 2.3%) | 47 (2.26%) | reproduced |
| 75 | About to Expire record's expiration | August 2026, already past | 8/28/2026 | reproduced |
| 76 | Spearman rho, STR rate vs new-building permit rate (75 hoods, ≥1,000 units, DIA excluded) | 0.64 (stats 0.643) | 0.643 from package panel CSV; 0.643 from verifier's own warehouse computation (own STR counts × spine permit sums) | reproduced |
| 77 | Spearman rho on raw counts | 0.62 (stats 0.622) | 0.622 both ways | reproduced |
| 78 | Spearman rho including DIA | 0.60 | 0.600 from panel | reproduced |
| 79 | Top-10 rate overlap (STR vs permits) | Berkeley, Sunnyside, West Colfax | Berkeley, Sunnyside, West Colfax | reproduced |
| 80 | Panel integrity: panel active counts vs verifier neighborhood counts; panel ACS vs ACS layer; panel permits vs spine sums | — (control) | 0 mismatches on all 78 neighborhoods, all three comparisons; spine plain new_building_permit_count sums match the panel exactly (successor-inclusive sums differ and give rho 0.649, so the builder's stated surviving-parcel basis is the one that ties) | reproduced |
| 81 | STR parcels with a 2020–2026 new-building permit | 10.6% of 2,008 | 10.61% | reproduced |
| 82 | Residential parcels with a new-building permit | 3.6% of 209,805 | 3.63%; denominator reproduced exactly: spine parcels with a characteristics record = 209,805 | reproduced |
| 83 | STR parcels with a demolition | 4.8% | 4.78% | reproduced |
| 84 | Residential parcels with a demolition | 1.3% | 1.31% | reproduced |
| 85 | Prose spot-check: hero "2,083 licenses / 2,080 holders" | as headline | exact | reproduced |
| 86 | Prose spot-check: "Five Points alone holds 7.2%" | 7.2% | 7.25% (151/2,083) | reproduced |
| 87 | Prose spot-check: "84 licenses = 4.0% of active" | 4.0% | 4.03% | reproduced |
| 88 | Prose spot-check: "no status filter overstates active by 255; 10.9% Delinquent or Closed" | 255; 10.9% | 255; 255/2,338 = 10.91% | reproduced |
| 89 | Prose spot-check: fresh bridge match rate | 99.87% (2,335/2,338) | 2,335/2,338 = 99.87% on fresh register basis | reproduced |

Totals: 89 figures checked — 88 reproduced, 1 caveated (row 69, median-rate basis),
0 corrected, 0 refuted.

## Classification deep-dive (task item 4)

Verifier's own rule, written independently: tokenize the normalized name on
non-letters; BUSINESS if any token is in the verifier's token set. The set was
deliberately broader than the builder's in three places (TRUSTEE, ESTATE singular,
and REAL/ESTATE as standalone tokens were added). Result on all three bases —
active licenses, active holders, full register: **0 business-entity names**.
The builder's 0.0% claim HOLDS under an independent, slightly more aggressive rule.

Eyeball checks for misclassification risk (patterns/counts only, no names printed):
- Token-count histogram (active): 2 tokens: 1,969; 3: 103; 4: 10; 5: 1; single-token: 0; 6+: 0.
  Every name sits inside the builder's 2–5-token "individual" window, so the
  0 not-determined result is structural, not a rule artifact.
- No name contains a digit or an ampersand; one name contains a period, in the
  pattern single-letter initial + period (a personal-name initial, not an entity marker).
- Substring scans over the full name strings (catches tokenization misses):
  LLC 0, CORP 0, TRUST 0, COMPAN- 0, PROPERT- 0, HOLDING 0, REALTY 0, PARTNER 0,
  ENTERPRIS- 0, VENTURE 0, CAPITAL 0, MANAG- 0, FOUNDATION 0, HOTEL 0, RENTAL 0,
  SUITE 0, ASSOC 0, UNIVERSIT- 0, MINISTR- 0, SOCIETY 0, HOSPITAL- 0, ESTATE 0,
  AIRBNB 0, VRBO 0, VACATION 0, HOSPITALITY 0, MGMT 0, HOMES 0.
- Nonzero substring hits are all letter sequences INSIDE longer personal-name
  tokens, never standalone tokens: "INC" in 7 names (inside 6–9-letter tokens,
  interior or prefix position); "INN" in 5 (inside 4–9-letter tokens);
  "BANK" in 1 (prefix of a 5-letter token); "HOST" in 1 (prefix of a 9-letter token).
  Exact standalone-token counts for INN, HOST, CO are all 0. A token-based rule —
  the builder's or mine — is not missing hidden entity suffixes.
- Generational/particle tokens present are personal-name forms (JR ×3, III ×3,
  DE ×3, LA ×3 — counts of names containing the token), consistent with person names.

Conclusion on classification: the register genuinely contains no entity-style
name strings on the active basis; the 0.0% is a property of the data, not of
either rule. (As the brief itself states, this classifies the name as filed,
not beneficial ownership.)

## Scope caveats (not discrepancies)

1. Parcel and neighborhood figures (rows 46–68) are conditional on the Phase 3
   parcel bridge. The verifier rebuilt the assignment independently in form
   (inherit schednum by LICENSE_NUM from the cleaned layer; key-match the one
   entered license on its own PARCEL_NUM against the spine) and reproduced every
   figure. However, a purely raw PARCEL_NUM key match against spine v6 reaches
   only 2,069 of 2,083 active licenses (2,322 of 2,338 register-wide); the
   remaining placements come from the bridge's address-based matching, which the
   verifier did not re-derive from raw addresses. The bridge's own integrity is
   supported by the builder's Control A (recorded in verification.md); this pass
   verifies everything downstream of the bridge, and the bridge's match outcomes
   themselves only via the inherited layer.
2. Median neighborhood rate (row 69): correct on an all-78 basis; the brief
   prints 4.7 without naming the basis. Minor documentation gap, no numeric error.
3. Spearman verification is genuinely two-path: (a) from the package's
   neighborhood_panel.csv, and (b) from the verifier's own joins of the raw
   register + spine + ACS layers. Both give 0.643 / 0.622. Path (b) does not
   depend on the package panel at all; the panel was separately shown to match
   the warehouse layers on all 78 neighborhoods.

## Disposition

No figure in stats.json or brief-draft.md requires correction. The package's
decisive claims — holder concentration (2,080 holders, max 2, 99.71% singletons),
0.0% business-entity names, parcel stacking (12 parcels / 84 licenses / all
distinct holders), neighborhood footprint and rates, four-day drift, and the
0.64 co-location correlation — all reproduce from the raw snapshots under an
independent implementation.

## Re-verification pass (fix loop) — 2026-10-19

Verifier: independent re-verification subagent pass, after the fix loop. Scope was
limited to the five items below (F-4 base-address rollup, F-6 cross-tab, the
corrected non-active count, the row-69 median basis, and headline sanity). Every
figure was recomputed from the RAW warehouse snapshots with the verifier's own
implementation, written from the task specification; package code
(code/build_stats.py, code/audit_section10.py) was NOT reused or executed.
Parcel assignment was rebuilt independently in form (schednum inherited by
LICENSE_NUM from the cleaned layer; the 1 entered license key-matched on its
PARCEL_NUM, zfill to 13, against spine v6; result 2,335 of 2,338 matched, 3
unmatched — the same bridge outcomes the package records). No licensee name,
street address, or parcel number appears in this section; results are counts
and patterns only.

Environment note: the specified venv (~/workspace/denver-housing-permits/.venv)
again had pandas but no pyarrow; pyarrow 26.0.0 was installed to a throwaway
/tmp target and layered via PYTHONPATH. No package or warehouse file was
modified by the recomputation.

### Item 1 — F-4 base-address rollup (active licenses, status exactly "License Issued - Active")

Verifier normalization, implemented from the specification: uppercase; "."
and "," treated as separators; trailing "#"+identifier stripped; trailing
named designator (UNIT/APT/APARTMENT/STE/SUITE/BLDG/BUILDING/FL/FLOOR/RM/ROOM)
plus its identifier stripped (identifier may contain a hyphen); bare trailing
unit token (digits, digits+letter, or single letter) following a street-suffix
token stripped, directional tokens (N/S/E/W) never stripped.

| Figure | Claimed | Recomputed | Verdict |
|---|---|---|---|
| Distinct base addresses (active) | 1,963 | 1,963 | reproduced |
| Multi-license base addresses | 39 | 39 | reproduced |
| Licenses on multi-license base addresses | 159 | 159 | reproduced |
| Share of active licenses | 7.63% | 7.6332% → 7.63% (brief prints 7.6% at 1 dp) | reproduced |
| Max licenses at one base address | 17 | 17 | reproduced |
| Multi groups spanning >1 parcel | 27 | 27 | reproduced |
| Multi groups on a single parcel | 12 | 12 | reproduced |
| Every license in every multi group under a distinct holder | true | true (licenses == distinct holders in all 39 groups) | reproduced |
| Size distribution (licenses per group: # groups) | 2:21, 3:9, 4:1, 6:1, 7:1, 8:1, 9:2, 13:1, 17:2 | identical, all nine cells | reproduced |
| Finding 2 printed figures vs stats.json vs recomputation | 1,963 / 39 / 159 / 7.6% / 17 / 27 / 12 | all three agree (7.6% is the 1-dp rounding of 7.63%) | reproduced |

Supporting checks: no multi-license group contains one of the 3
parcel-unmatched licenses, so the 27 / 12 parcel split is not distorted by
missing parcels. Sensitivity (not a discrepancy): under a deliberately more
aggressive reading that also destroys hyphens inside identifiers, the rollup
reads 1,964 distinct / 38 multi / 157 licenses / max 17 — exactly one
2-license group, whose two filings carry hyphenated APT identifiers, fails to
merge under that reading. The claimed figures hold under the documented rule
(identifiers may contain hyphens, per the brief Methods and the task
specification); the maximum (17) and every structural conclusion are unchanged
under either reading.

### Item 2 — F-6 cross-tab (active records with expiration before the 2026-10-19 pull date)

Dates parsed independently: EXPIRATION_DATE from its string form;
MOST_RECENTLY_ISSUED_DATE as epoch-milliseconds UTC converted to
America/Denver for the year; lag = pull date (2026-10-19) minus expiration.

| Figure | Claimed | Recomputed | Verdict |
|---|---|---|---|
| Past-expiration active records | 47 | 47 (2.26% of active) | reproduced |
| Most-recently-issued year 2023 | 2 | 2 | reproduced |
| Most-recently-issued year 2024 | 16 | 16 | reproduced |
| Most-recently-issued year 2025 | 20 | 20 | reproduced |
| Most-recently-issued year 2026 | 9 | 9 | reproduced |
| Most recently issued in 2025–2026 | 29 | 29 | reproduced |
| Expiration lag, median days | 230 | 230.0 | reproduced |
| Expiration lag, max days | 1,374 | 1,374 | reproduced |
| Lag over one year | 20 | 20 (identical under >365 and ≥365) | reproduced |
| Most-recent issue date AFTER printed expiration date | 4 | 4 (identical under instant compare and Denver date-only compare; year distribution also identical on UTC years) | reproduced |

### Item 3 — Non-active record count (corrected figure: 255)

| Figure | Claimed | Recomputed | Verdict |
|---|---|---|---|
| Delinquent | 137 | 137 | reproduced |
| Closed - Expired | 116 | 116 | reproduced |
| About to Expire | 1 | 1 | reproduced |
| Closed - Surrendered | 1 | 1 | reproduced |
| Non-active total | 255 | 255 (137+116+1+1; also 2,338 − 2,083) | reproduced |
| Brief / verification print 255 consistently | yes | yes: brief-draft.md (Finding 5 and Data notes), substack-draft.md (same two places), and verification.md (field semantics, audit output, gate summary, F-8 disposition) all print 255; stats.json status counter sums to the same 255; no competing non-active total appears in the brief, substack draft, social drafts, or verification | reproduced |

Scope note on the two residual "253" strings in the package: (a)
verification.md's F-8 disposition quotes the erroneous fix instruction
("said 253 non-active records") in the same sentence that corrects it to 255 —
a correction record, not a competing figure; (b) adversarial-review.md, the
pre-fix reviewer artifact, still states 253 in its F-8 finding text. That file
is the historical review record and sits outside the brief/verification scope
of this check; the fix loop's disposition in verification.md is the
package's current word on the number.

### Item 4 — Row-69 median basis (Finding 3 / Methods)

Medians recomputed independently from the raw register through the rebuilt
bridge and spine neighborhoods against the ACS layer (359,351.5 allocated
units over 78 neighborhoods; verifier neighborhood counts match
data/neighborhood_panel.csv on all 78 neighborhoods, 0 mismatches).

| Figure | Claimed | Recomputed | Verdict |
|---|---|---|---|
| Median rate, all 78 neighborhoods (zeros counted as 0) | 4.71 (brief prints 4.7) | 4.7138 on unrounded rates → 4.71 | reproduced |
| Median rate, 75 neighborhoods with licenses only | 5.04 | 5.0401 on unrounded rates → 5.04 | reproduced |
| Basis sentence in brief Finding 3 | present | present verbatim: "median across all 78 neighborhoods, zero-license neighborhoods counted as 0; over the 75 neighborhoods with licenses it would be 5.04" | reproduced |
| Basis sentence in brief Methods | present | basis clause present verbatim ("The median neighborhood rate is computed across all 78 neighborhoods, zero-license neighborhoods counted as 0"); the 5.04 alternate figure is not repeated in brief Methods — it appears in Finding 3, stats.json, and the verification.md methods checklist | reproduced (with this precision note) |
| Basis counts | 78 total / 75 with licenses / 3 zero | 78 / 75 / 3; zero set Auraria, Kennedy, Sun Valley; DIA holds 3 active licenses | reproduced |

Rounding note: averaging the two middle rounded panel rates gives 4.715,
while the median of unrounded rates is 4.7138; both round to the claimed
4.71, so the printed figure is correct on either computation path.

### Item 5 — Headline sanity after the fix loop

Holder key: ENTITY_NAME normalized (uppercase, whitespace collapsed),
computed on active licenses only.

| Figure | Claimed | Recomputed | Verdict |
|---|---|---|---|
| Active licenses | 2,083 | 2,083 | reproduced |
| Distinct holders | 2,080 | 2,080 | reproduced |
| Sole-license share | 99.71% | 99.7120% → 99.71% (2,077 of 2,083 licenses; 2,077 holders with 1, 3 holders with 2, max 2) | reproduced |
| Top-1 share | 0.10% | 0.0960% (2 licenses) → 0.10% | reproduced |
| Top-5 share | 0.38% | 0.3841% (8 licenses) → 0.38% | reproduced |
| Top-10 share | 0.62% | 0.6241% (13 licenses) → 0.62% | reproduced |
| Top-25 share | 1.34% | 1.3442% (28 licenses) → 1.34% | reproduced |

### Re-verification disposition

All five items reproduced; 0 corrected, 0 refuted. Two precision notes are
recorded above and neither changes a printed figure: (1) the F-4 rollup's
exact counts depend on treating hyphenated unit identifiers as single
identifiers (the documented rule); under a hyphen-destroying variant one
2-license group splits and the rollup reads 1,964 / 38 / 157 with the same
maximum of 17. (2) brief-draft.md Methods states the median basis but does
not repeat the 5.04 over-75 figure, which is printed in Finding 3, stats.json,
and verification.md. Nothing was published, pushed, posted, or sent in this
pass.
