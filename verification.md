# Verification - Denver STR licenses brief (2026-10-19)

Dataset: ODC_short_term_rental_licenses_active_or_pending_renewal, Denver Open Data
Catalog, ArcGIS FeatureServer layer 54 (Department of Licensing and Consumer
Protection; the dataset is still published under the Denver Excise and Licenses
name). Fresh full-service
pull 2026-10-19 (2026-10-19T11:27:59Z), 2,338 records, service last edit
2026-10-19T09:44:04Z. Snapshot + pull log + sha256: stack/denver/snapshots/2026-10-19/
str_licenses.parquet and pull_log_str_2026-10-19.json.
Prior snapshot (drift baseline): 2026-10-15 pull, 2,349 records.
Denominators: ACS 2020-2024 5-year B25001 housing units (warehouse layer
acs_neighborhood_units.parquet; same basis as the October 17 and 18 briefs).
Parcel bridge: warehouse Phase 3 cleaned layer by LICENSE_NUM + 1 fresh key match;
neighborhoods and permit aggregates: parcel spine v6.

## Field semantics, established from the service (2026-10-15, re-verified 2026-10-19)

- LICENSE_STATUS is the only status field and the brief's active basis is the exact
  string "License Issued - Active". Full counter, recorded before any filter (fresh):
  Active 2,083; Delinquent 137; Closed - Expired 116; About to Expire 1;
  Closed - Surrendered 1. The service name promises "active or pending renewal"; the
  table carries 255 non-active records (10.9 percent).
- ENTITY_NAME is populated on every record (0 nulls in both snapshots). Holder counts
  use the normalized string (uppercase, whitespace collapsed). TAX_ID exists in the raw
  service and was not used or carried into any analysis file.
- MULTIPLE_LICENSES is constant "Stand Alone" on all 2,338 fresh records, including
  records on parcels that carry up to 35 licenses. It is not a multi-license signal.
- RELATIONSHIP is null on all 2,338 records. RENEWAL_STATUS is null on all 2,083 active
  records and populated on non-active records; no figure rests on it.
- PARCEL_NUM: 2,336 rows 13-digit; 1 row 12-digit (leading zero dropped, zfill
  normalizes); 1 row a legacy dashed number (not keyable; placed by address in the
  Phase 3 bridge).
- EXPIRATION_DATE disagrees with status on 48 records as published: 47 Active records
  carry an expiration date before the pull date, and the single About to Expire record
  expired in August 2026. Reported in Finding 5 as a field disagreement only.

## Methods checklist (brief-writing standards Section 3)

- Base rates and exposure: neighborhood footprint is reported as counts AND as
  licenses per 1,000 ACS housing units; the citywide rate (5.8 per 1,000) and the
  median neighborhood rate (4.7 per 1,000, median across all 78 neighborhoods,
  zero-license neighborhoods counted as 0; over the 75 neighborhoods with licenses
  it would be 5.04) are printed next to every ranking. No raw share is
  presented as a density.
- Direction of causality: Finding 4 (STR density vs permit density) is stated as
  co-location only; the parcel-level caveat (permits do not date licenses; newer or
  rebuilt homes may be more likely to be licensed) is printed in the finding.
- Category and definition changes: LICENSE_STATUS values are identical in name and
  near-identical in distribution across the two snapshots four days apart (drift
  table in stats.json); no category rename is present. The register has no time
  series in this brief beyond the four-day drift and the issue-year vintage, both
  computed on stated bases.
- Time windows: the register snapshot is a point in time (2026-10-19); the permit
  window is 2020-01-01 to 2026-10-12 (spine v6 basis, named wherever used); the
  vintage uses ORIG_ISSUED_DATE (America/Denver) for active licenses only.
- Joins: fresh parcel bridge 2,335 of 2,338 matched (99.87 percent: key 2,321 +
  fresh key 1 + address_strict 13; unmatched 3). Neighborhood assignment 2,080 of
  2,083 active (99.86 percent); the 3 unassigned are exactly the bridge-unmatched
  licenses, which are counted in every citywide total and excluded from parcel and
  neighborhood tables only. Unmatched records cannot differ systematically in any
  way the data shows (0.13 percent of the register).
- Small numbers: the concentration findings rest on the full register (2,083 active
  licenses); the smallest printed neighborhood count in the rate top-12 is 21
  licenses (Regis) and its housing-unit denominator is printed in the panel. The
  three two-license holders are reported as a count of 3 with the underlying 6
  licenses always adjacent.
- Official definitions: "active" is the publisher's own status string; "primary
  residence" is the program's own rule language, cited in sources.md and used as
  context only.
- Layering admission test: ACS housing layer - enables exposure rates (Finding 3
  cannot rank neighborhoods without it) - ADMITTED. Parcel spine - assigns parcels
  and neighborhoods and exposes parcel stacking (Finding 2 cannot be stated from
  the register alone) - ADMITTED. Permits layer - supports the co-location claim
  (Finding 4 is not contained in any single source) - ADMITTED. Demolitions by
  neighborhood - computed; the neighborhood-level comparison added no claim beyond
  the permit comparison - CUT to the parcel-level prevalence printed inside
  Finding 4, and the cut is recorded here and in the brief's Methods.

## Pre-flight audit (Section 10)

Script: code/audit_section10.py (ships in this package). Full output: data/audit_output.txt.
Result: ALL SECTION 10 ASSERTIONS PASSED. Full output:

```
fresh snapshot rows 2338 | prior snapshot rows 2349

== 10.1.4 categorical exhaustiveness (counters recorded before any filter) ==
LICENSE_STATUS full counter: {'License Issued - Active': 2083, 'Closed - Expired': 116, 'Delinquent': 137, 'About to Expire': 1, 'Closed - Surrendered': 1}
LICENSE_TYPE full counter: {'Short Term Rental': 2338}
MULTIPLE_LICENSES full counter: {'Stand Alone': 2338} (constant in the source; not used as a multi-license signal)
RELATIONSHIP counter: all null = True
RENEWAL_STATUS counter (top): {'nan': 2083, 'Awaiting Customer Response': 90, 'Inactive': 64, 'Pending': 63, 'Awaiting Customer Inspections': 38}

== 10.1.1 zero/null sentinel traps ==
ENTITY_NAME nulls: 0
PARCEL_NUM string-length counter: {13: 2336, 12: 1, 16: 1}
non-13-digit PARCEL_NUM rows: 2 | of those, 12-digit (leading zero dropped, zfill-normalized): 1 | legacy dashed (not keyable): 1
No numeric range bucketing exists in this brief; no sentinel value is mapped into a rate.

== 10.1.2 filter polarity (active filter: 3 matched vs 3 excluded, anonymized) ==
matched (== License Issued - Active): n = 2083 | sample statuses: ['License Issued - Active', 'License Issued - Active', 'License Issued - Active'] | sample license years: ['2016', '2016', '2016']
excluded (!= active): n = 255 | status counter: Counter({'Delinquent': 137, 'Closed - Expired': 116, 'About to Expire': 1, 'Closed - Surrendered': 1})
Polarity verified: the active basis is an exact-string equality on LICENSE_STATUS;
Delinquent (137) and About to Expire (1) are EXCLUDED from active, never merged in.

== 10.1.3 numerator/denominator unit agreement ==
Top-1 share recomputed as licenses/licenses: 2/2083 = 0.10% (ties stats.json).
Holders are never used as a denominator for a license share anywhere in stats.json;
per-1,000 rates are licenses over ACS housing units (same unit in numerator family).

== 10.1.5 nullable-denominator trap (name classification) ==
active licenses: denominator = ALL 2083 rows | counts {'individual_name': 2083} | shares {'individual_name': 100.0, 'business_entity_name': 0.0, 'not_determined': 0.0} | sum = 100.00%
full register: denominator = ALL 2338 rows | counts {'individual_name': 2338} | shares {'individual_name': 100.0, 'business_entity_name': 0.0, 'not_determined': 0.0} | sum = 100.00%
Determined + not-determined shares sum to 100% on the full stated population in both bases.

== concentration recomputation (independent of build_stats code path) ==
Bands tie to stats.json: 1 -> 2,077 holders; 2 -> 3 holders; 3-5 / 6-10 / 11+ -> 0 holders.
Max licenses per holder (active) = 2. Share held by 2+ holders = 6/2,083 = 0.29%.

== 10.2 built-in control A: parcel-bridge integrity (licenses_on_parcel) ==
parcels compared: 2265 | mismatches: 0
Control A PASSED: recomputing licenses-per-parcel from the raw 2026-10-15 snapshot
through the bridge reproduces the cleaned layer's licenses_on_parcel on every parcel.

== 10.2 built-in control B: hand-check of the multi-license holders (anonymized) ==
Each of the 3 holders with 2 active licenses: 2 distinct LICENSE_NUMs,
2 distinct PARCEL_NUMs, 2 distinct addresses. No duplicate-license artifact.
Singleton spot-check: the first 499 single-license holders in file order
each resolve to exactly 1 active LICENSE_NUM under the normalized name.

== 10.2 join hygiene: fresh bridge + neighborhood assignment ==
Fresh bridge: {'key': 2321, 'address_strict': 13, 'unmatched': 3, 'key (fresh, PARCEL_NUM)': 1} | matched 2,335/2,338 = 99.87% (same rate as the Phase 3 bridge).
Neighborhoods: 2080/2,083 active licenses assigned (99.86%);
the 3 unassigned are exactly the 3 bridge-unmatched licenses. 75 of 78 neighborhoods hold 1+;
zero-active neighborhoods: ['Auraria', 'Kennedy', 'Sun Valley']
Physical scale: 2,083 active licenses over 359,351 allocated housing units = 5.8 per 1,000 units citywide.

== drift arithmetic (fresh vs 2026-10-15) ==
2,349 prior - 12 left + 1 entered = 2,338 fresh. Active: 2,098 -> 2,083 (net -15):
-11 active licenses left the register, -7 active moved to Delinquent, +2 Delinquent
returned to Active, +1 entered as Active. Transitions tie to stats.json.

== expiry field disagreement (printed, not adjudicated) ==
Active-status rows whose EXPIRATION_DATE precedes the 2026-10-19 pull: 47 (2.26% of active). The brief reports the disagreement and claims nothing about validity.

== fix loop F-6: past-expiration cross-tab (recomputed) ==
47 past-expiration actives: MOST_RECENTLY_ISSUED years {'2023': 2, '2024': 16, '2025': 20, '2026': 9} | 2025-2026: 29 | lag median/max days: 230.0 1374 | over one year: 20

== fix loop F-4: base-address rollup (independent recomputation) ==
Base-address rollup ties stats.json: 1,963 base addresses; 39 multi-license; 159 licenses; max 17;
27 multi groups span more than one parcel, 12 sit on a single parcel; every license a distinct holder.

== verifier row 69: median neighborhood rate basis ==
Median 4.71 is over all 78 neighborhoods (zeros counted as 0); over the 75 with licenses it is 5.04. DIA holds 3 active licenses.

ALL SECTION 10 ASSERTIONS PASSED
```

Gate summary:
- 10.1.1 sentinels: ENTITY_NAME has no nulls; PARCEL_NUM anomalies enumerated
  (1 twelve-digit, 1 dashed); no range bucketing exists in this brief.
- 10.1.2 polarity: the active filter is an exact-string equality; matched 2,083 vs
  excluded 255 (Delinquent 137, Closed - Expired 116, About to Expire 1,
  Closed - Surrendered 1). Delinquent is never merged into active.
- 10.1.3 unit agreement: top-1 share recomputed as licenses over licenses
  (2/2,083 = 0.10 percent) and ties to stats.json; holders are never a denominator
  for a license share.
- 10.1.4 exhaustiveness: LICENSE_STATUS (5 values), LICENSE_TYPE (1 value), and
  MULTIPLE_LICENSES (1 constant value) counters recorded before filtering and sum
  to the pulled total.
- 10.1.5 nullable denominators: the name classification is computed on ALL active
  licenses (2,083) and separately on ALL register rows (2,338); determined plus
  not-determined shares sum to 100.00 percent in both bases (individual 100.0,
  business 0.0, not determined 0.0). No NaN-skipping aggregation is used anywhere.
- 10.2 controls: Control A (parcel-bridge integrity) and Control B (multi-license
  holder hand-check) both pass; see the next section.
- 10.3 documentation sync: README dependency list was checked against actual code
  imports (pandas, numpy, pyarrow, matplotlib, Pillow; standard library otherwise).
  Every number in brief-draft.md and social-drafts.md was cross-checked against the
  final stats.json after the last build_stats.py run (Section 12.5 assertion: the
  hero composite asserts its figure against stats.json at build time and the audit
  asserts the register, concentration, classification, bridge, neighborhood, and
  drift blocks).

## Built-in controls (Section 10.2.2)

- Control A, parcel-bridge integrity: licenses-per-parcel recomputed from the RAW
  2026-10-15 snapshot through the LICENSE_NUM bridge reproduces the cleaned layer's
  licenses_on_parcel on all 2,265 parcels, 0 mismatches. The bridge the brief
  inherits is therefore the bridge the warehouse recorded.
- Control B, holder hand-check (anonymized by design; no names in this package):
  each of the 3 licensees holding 2 active licenses was inspected row by row: 2
  distinct LICENSE_NUMs, 2 distinct PARCEL_NUMs, 2 distinct addresses per holder.
  The pairs are second licenses, not duplicate filings. A singleton spot-check of
  the first 499 single-license holders in file order confirms 1 active license each.
- Sensitivity (not a control): name-variant merging. First-and-last-token merging
  reproduces the headline exactly (2,080 groups, max 2). First-initial-and-surname
  over-merging (known to combine different people) gives 2,034 groups, max 4, and
  92 licenses in groups of 2 or more (4.4 percent): the printed concentration
  result is not an artifact of name splitting.

## Cross-document figure assertion (Section 12.5)

Figures asserted equal across stats.json, brief-draft.md, substack-draft.md,
social-drafts.md, charts, and hero.png at build time: register 2,338; active 2,083;
holders 2,080; single-license share 99.71 percent (hero prints 99.7 percent);
bands 2,077 / 3 / 0 / 0 / 0; top shares 0.10 / 0.38 / 0.62 / 1.34 percent; multi-license
parcels 12 (active) and 13 (register); largest parcel 32 (active) and 35 (register);
base addresses (fix loop F-4) 1,963 distinct, 39 multi-license, 159 licenses on
multi-license base addresses (7.63 percent), maximum 17, 27 spanning more than one
parcel, 12 on a single parcel; neighborhoods 75 of 78 with 1+, zero set Auraria /
Kennedy / Sun Valley; DIA 3 active licenses; citywide 5.8 per 1,000; Whittier 27.1;
median neighborhood rate 4.7 per 1,000 on the stated all-78 basis (5.04 over the 75
with licenses); vintage 61.0 percent issued 2023 or later; drift
active minus 15; fusion rho 0.64 (rates) and 0.62 (counts); expiry disagreements 47
with the F-6 cross-tab (29 of 47 most recently issued in 2025-2026; lag median 230
days, maximum 1,374 days, 20 over one year; 4 re-issued after their printed
expiration date). The assertion was re-run after all fix-loop edits (2026-10-19):
every figure in brief-draft.md, substack-draft.md, social-drafts.md, and the hero
equals stats.json.
One basis per number (Section 12.4): every count in the prose is labeled active-basis
or register-basis where the two differ, and the register composition
(2,083 + 137 + 116 + 1 + 1 = 2,338) is printed in the brief's opening.

## Independent verification and adversarial review (Section 11)

The independent verifier pass is complete: verification-ledger-independent.md in
this package (89 figures checked from the raw warehouse snapshots with an
independent implementation: 88 reproduced, 1 caveated at row 69, 0 corrected, 0
refuted). The adversarial reviewer pass is complete: adversarial-review.md in this
package (findings F-1 to F-19: 1 BLOCKING, 8 SHOULD-FIX, 10 FLAG-FOR-ALEX). Both
reports were read in full before adjudication (standards Section 10.3.3), and the
fix loop below records a disposition for every finding. The builder's own Section
10 audit (above) passed before drafting, and the two built-in controls were run
against the raw snapshots by code paths independent of build_stats.py
(audit_section10.py recomputes concentration and classification with
collections.Counter, not the builder's pandas pipeline); the audit was extended in
the fix loop to assert the F-4 base-address rollup, the F-6 cross-tab, and the
row-69 median basis, and re-run clean (output above).

## Warehouse deposit

- Raw snapshot: stack/denver/snapshots/2026-10-19/str_licenses.parquet (2,338 rows)
  with pull log pull_log_str_2026-10-19.json (sha256 ec739740eeed764c5bf2261f1bd8bbbf2563fe2e3d4b9a67cf82cbf2216f9a5b).
- manifest.json: denver_str_licenses entry updated in place (snapshot_date
  2026-10-19; the 2026-10-15 record moved to snapshot_history; layer count unchanged).
- stack/denver/verification.md: "Study deposit - Denver STR licenses brief
  (2026-10-19)" entry appended, recording the drift and the note that the cleaned
  layer still derives from the 2026-10-15 snapshot until the next refresh cycle.
- Package data files after the fix loop: data/neighborhood_panel.csv (aggregate
  neighborhood panel) and data/audit_output.txt only. The package working copy of
  the raw snapshot (data/str_licenses_raw_2026-10-19.parquet) was DELETED in the
  fix loop (finding F-1); the warehouse snapshot above is the only raw copy.

## Fix loop (2026-10-19)

Adjudicated from the FULL text of adversarial-review.md (F-1 to F-19) and
verification-ledger-independent.md (standards Section 10.3.3). Every finding has
a disposition below. Figures quoted by the reviewer were recomputed before
being inherited: the reviewer's crude base-address rollup (19 base addresses,
63 licenses, maximum 17, 13 spanning more than one parcel) was reproduced
exactly by the fix loop's crude replication before the proper rollup superseded
it, and the F-6 cross-tab numbers were recomputed from the warehouse snapshot.
One numeric slip in the fix instructions themselves is recorded at F-8.

- F-1 (BLOCKING, privacy) - FIXED. data/str_licenses_raw_2026-10-19.parquet
  (2,338 rows with ENTITY_NAME, ADDRESS, PARCEL_NUM, TAX_ID) was deleted from
  the package on 2026-10-19. The archived snapshot was confirmed present before
  deletion at stack/denver/snapshots/2026-10-19/str_licenses.parquet (171,678
  bytes, with its pull log) and remains there; it is the only raw copy. Every
  remaining package file was audited for licensee names, street addresses,
  parcel numbers, and TAX_IDs: shipped data files are aggregate-only
  (data/neighborhood_panel.csv, data/audit_output.txt). code/pull_data.py was
  changed so it never writes a package copy again. A programmatic leakage scan
  (code/leakage_scan.py; value sets taken from the warehouse snapshot: 2,334
  name forms, 2,663 address forms, 2,258 parcel numbers, 2,336 TAX_IDs) was run
  over the whole package before deletion (only the raw parquet contained
  values; every other file, including stats.json, all markdown, code/, charts/,
  and the hero, had zero hits) and re-run after all fix-loop edits: PASSED, no
  licensee name, street address, parcel number, or TAX_ID value in any package
  file. The product-rule sentences in README.md, this file, and
  reviewer-notes.md now enumerate every shipped file category, including data/
  and code/.
- F-2 (framing) - FIXED. "Structurally absent" (reviewer-notes), "as
  unconcentrated as a register can be" (lede), and "no concentration to measure"
  (Finding 1 heading) are removed. The lede, Finding 1, and the "What this might
  mean" settlement sentence now carry the reframed claim: licenses are filed one
  per person under personal names, the shape the primary-residence rules
  require, and the register has no field that could reveal common ownership
  behind those names. The intake-design sentence (the licensee is a person
  licensing their one primary residence, a single dwelling unit, so a
  name-field count cannot distinguish "no concentrated operators" from "intake
  only admits one license per natural person") is in Finding 1 and in Data
  notes. All numbers identical.
- F-3 (eligibility citation) - FIXED. sources.md now cites the city's own
  document: City and County of Denver, DLCP, "Short-term rental frequently
  asked questions" (denvergov.org), fetched and read in full in this loop. The
  FAQ's own language (primary residence is the place where habitation is fixed
  for the license term and the person's usual place of return; a person can
  have only one primary residence; the STR location is always a single
  residential dwelling unit; primary-residency documentation required on
  application and renewal under DRMC criteria) replaces reliance on the
  University of Denver law-school PDF, which is no longer the program-rules
  citation. The eligibility consequence is stated in Finding 1, and the "name
  as filed, not beneficial ownership" scope sentence now travels in the lede
  and in the settlement sentence (checked in the substack draft and social
  drafts as well).
- F-4 (parcels vs buildings) - FIXED by running the proper rollup (option a).
  Base-address normalization (uppercase, punctuation removed; trailing named
  designators UNIT/APT/APARTMENT/STE/SUITE/BLDG/BUILDING/FL/FLOOR/RM/ROOM and #
  stripped with their identifiers; bare trailing unit tokens after a
  street-suffix token stripped) is implemented in code/build_stats.py and
  independently re-implemented in code/audit_section10.py; both agree and the
  audit asserts the block. Result (active basis, in stats.json
  base_address_rollup_active): 1,963 distinct base addresses; 39 multi-license
  base addresses holding 159 licenses (7.63 percent of active); maximum 17 at
  one base address; 27 of the 39 span more than one parcel, 12 sit on a single
  parcel; within every multi-license group each license has a distinct holder.
  The numbers differ from the reviewer's crude rollup (19 / 63 / 17 / 13)
  because the crude pass stripped only UNIT/APT/STE/# designators; the proper
  normalization additionally strips BLDG designators and bare trailing unit
  numbers, merging 124 more unit-variant addresses into their base addresses
  (the maximum, 17, is identical under both). Finding 2 prints the rollup
  beside the parcel table. The 4-license parcel against TOT_UNITS=1 is
  explained in Finding 2 from its own records (stats.json tot_units_1_parcel):
  the spine record is PROP_CLASS 1230, RESIDENTIAL-CONDOMINIUM, Five Points,
  72,919 sq ft land, no characteristics card; the parcels record carries the
  master appendage (999), structure type "107: CONDO (FEE SIMPLE)," gross area
  126,465 sq ft, built 2018, and a legal description identifying it as the
  master parcel of a condominium development; all 4 licenses are unit filings
  by 4 distinct holders at 4 unit-designated addresses (2 base addresses)
  assigned to the master parcel by the bridge. Plausible reading, printed in
  the brief: TOT_UNITS=1 describes the master parcel record, not the building's
  unit count. Building language in Finding 2 is now supported by the rollup;
  the unsupported claims ("the only form of license stacking the register
  contains"; "stacking is by building" on the parcel evidence alone) were
  deleted.
- F-5 (three two-license holders) - FIXED. Finding 1 now carries a neutral,
  no-conclusion paragraph: three names hold two active licenses on distinct
  parcels at distinct addresses, originally issued years apart (2017 and 2026;
  2022 and 2025; 2024 and 2026), two of the three pairs in different ZIP codes
  (recomputed in this loop; the third pair shares a ZIP), the one-primary-
  residence tension stated, the innocent mechanisms (mid-term move with the old
  license not yet surrendered; overlapping renewal and new license) printed,
  and no conclusion drawn, mirroring Finding 5's treatment of the 47.
- F-6 (the 47) - FIXED. Finding 5 prints the recomputed cross-tab: of the 47
  past-expiration active records, MOST_RECENTLY_ISSUED_DATE falls in 2023 for
  2, 2024 for 16, 2025 for 20, 2026 for 9 (29 of 47 in 2025-2026, matching the
  reviewer); expiration lag median 230 days, maximum 1,374 days, 20 over one
  year (all matching the reviewer); 4 of the 47 carry a most-recent issue date
  after their printed expiration date. Figures are in stats.json
  (expiry_hygiene.past_expiration_cross_tab) and asserted by the audit. The Who
  can act item was rewritten: the ask is to publish documentation of which
  field is authoritative when status and expiration disagree, with success
  measured by that documentation existing, NOT "zero active records with a past
  expiration date" (the old success line was removed).
- F-7 (department name) - FIXED. The Department of Licensing and Consumer
  Protection (DLCP) is used in Who can act, the lede's publisher line, and
  wherever the brief addresses the administering department, with the
  parenthetical "(formerly Excise and Licenses; the dataset is still published
  under the Excise and Licenses name)". stats.json meta, sources.md, and the
  social and substack drafts were checked for consistency.
- F-8 (survivor stock) - FIXED. Finding 5 states that the issue-year
  distribution describes licenses active today, that lapsed licenses exit the
  table (255 non-active records in the whole table across a decade of annual
  licensing, recomputed as 2,338 minus 2,083; 12 records left in the four days
  between snapshots), and that the distribution is a survivor stock, not an
  issuance series. The "register is young" heading and growth-inviting phrasing
  were adjusted (heading now "The active register is mostly recent"; the X
  thread's "register is young" line was aligned). NOTE: the fix instructions
  said 253 non-active records; the register's own status counter gives 255
  (137 Delinquent + 116 Closed - Expired + 1 About to Expire + 1 Closed -
  Surrendered), and 255 is what the brief prints.
- F-9 (over-merge bound) - FIXED. The Finding 1 sentence is qualified in
  place: the over-merge is "an upper bound on splitting by middle names and
  initials only," and the text states it cannot bound splitting across a
  changed surname (marriage, hyphenation), a name-order swap, or a suffix
  keyed as the surname token. No unqualified "upper bound" phrasing remains.
- Verifier caveat, ledger row 69 (median basis) - FIXED. Wherever the median
  neighborhood rate 4.7 per 1,000 is printed (brief Finding 3, brief Methods,
  the methods checklist above, stats.json), the basis is stated: median across
  all 78 neighborhoods, zero-license neighborhoods counted as 0, with the
  over-75 figure (5.04) printed parenthetically in Finding 3 and in stats.json
  (median_neighborhood_rate_basis). No chart prints the median, so no chart
  change was needed.
- F-10 (Delinquent treatment) - FLAG-FOR-ALEX, left open as instructed.
  Recorded: attacked by the reviewer, the attack failed, and the brief's
  strict basis is sound. Including Delinquent licenses in an operating
  footprint changes the headline negligibly (reviewer's recomputation: 2,220
  licenses, 2,217 holders, maximum 2, 99.64 percent sole-license). No fix
  required; the package's strict active basis stands.
- F-11 (TAX_ID cross-check) - FLAG-FOR-ALEX, left open as instructed.
  Recorded: the TAX_ID cross-check was done by the reviewer; maximum 1 active
  license per TAX_ID (2,336 distinct TAX_IDs for 2,338 rows; the key is
  per-license/per-property in practice), so a TAX_ID count cannot rescue
  beneficial ownership and the omission is immaterial to every count. The only
  TAX_ID problem was its presence in the shipped raw file, closed under F-1.
- F-12 (household proxy) - FLAG-FOR-ALEX, left open as instructed. Recorded:
  the household proxy was tested by the reviewer (same base address plus same
  surname under two distinct holder names): zero such groups in the active
  register. The brief's caveat is conservative. Spouse pairs under different
  surnames and manager-client structures remain invisible, as the brief
  states. No change made.
- F-13 (Spearman robustness) - FLAG-FOR-ALEX, left open as instructed.
  Recorded: the reviewer recomputed rho 0.643 on rates, 0.622 on counts, 0.600
  including DIA, and the correlation survives the sensitivities the brief did
  not print (neighborhoods with at least 2,000 ACS units: 0.655; excluding the
  zero-permit downtown trio: 0.665). Finding 4 stands; no fix required.
- F-14 (ACS denominator tenure) - FLAG-FOR-ALEX, OPEN, left open as
  instructed. The renter-share (per-renter-occupied-unit) sensitivity on the
  Finding 3 denominator was NOT run and NOT resolved in this loop. The brief's
  existing disclosure (licenses per housing unit, not per rental unit;
  neighborhoods differ in tenure mix) stands. Alex's call.
- F-15 (ranking noise / median basis) - FLAG-FOR-ALEX, left open in part. The
  median basis is now stated wherever the median is printed (see the row-69
  disposition above). The ranking-noise point (the Whittier-Cole gap of 27.1
  vs 24.8 sits within plausible ACS allocation noise; the top of the rate
  table rests on 21 to 61 licenses over area-allocated fractional denominators)
  is recorded here as a caveat Alex may weigh; no stability sentence was added
  beyond the basis statement, per instructions.
- F-16 (land-use zeros / DIA) - FIXED (factual completion only). Finding 3 now
  notes DIA's 3 active licenses and that the three zero-license neighborhoods
  are land-use zeros (Auraria campus, Sun Valley public housing and
  redevelopment land, Kennedy golf-course area), verified against the data
  (DIA count 3 in both the neighborhood panel and the bridge assignment).
- F-17 (assessor-owner layer) - FLAG-FOR-ALEX, OPEN, left open as instructed.
  The in-stack assessor-owner layer exists and a licenses-per-assessor-owner
  count is computable from layers this package already joins; it was neither
  run in this loop nor resolved. One sentence disclosing it as untested scope
  was added to reviewer-notes.md (Section 11.3 flags). Alex's call: run it, or
  ship with the licensee-scope claims as reframed.
- F-18 (social repost) - FIXED. The personal-repost sentence in
  social-drafts.md was reworded to stay inside the reframed finding ("The
  licenses are filed one per person under personal names, the shape Denver's
  primary-residence rules require"). The cross-document figure assertion
  (Section 12.5) was re-run after ALL edits: every figure in the brief, the
  substack draft, the social drafts, the charts, and the hero equals
  stats.json (see the assertion section above, updated).
- F-19 (Section 11.3 flag list) - FIXED. reviewer-notes.md Section 11.3 flags
  now include F-1 (found-and-fixed, recorded, never omitted), F-5, F-7, and
  F-17, alongside the pre-existing flags; dispositions for F-1 through F-19
  are recorded in this section, per Section 11.5.

Final gates after the fix loop: code/audit_section10.py re-run and PASSED
(output in data/audit_output.txt and spliced above, including the new F-4,
F-6, and row-69 assertions); brief-draft.md re-read end to end after the edits;
the package was grepped for the silent-truncation marker (none anywhere) and
the publishable drafts for
en and em dashes (none); the F-1 leakage scan was re-run and PASSED. Nothing
was published, pushed, posted, or sent.

## Items reserved for Alex (Section 11.3)

- First use in a brief of the DLCP STR register as the primary
  dataset (the layer entered the warehouse in Phase 3, 2026-10-15, and appeared
  only as a section inside the teardown readouts until now).
- The brief names the Department of Licensing and Consumer Protection (DLCP) in
  the Who can act section (the register-hygiene items: the holder summary and
  the field-authority documentation for the 47 status/expiration disagreements).
  No other agency or official is named.
- Surprising result, flagged rather than smoothed: measured holder concentration
  is zero in every band above 2, and the business-entity share is 0.0 percent.
  Both were re-derived three ways (exact names, token merges, register-wide)
  before being printed.
- OPEN for Alex from the fix loop: F-14 (renter-share sensitivity on the ACS
  denominator, not run) and F-17 (assessor-owner concentration layer, not run,
  disclosed as untested scope in reviewer-notes.md). See the Fix loop section.

## Coordinator closure note (2026-10-19, post re-verification)

- Adversarial re-verification: F-1 through F-9 and F-18 all CLOSED on the artifacts (leakage scan re-run independently, 0 hits). Dispositions complete for F-1 to F-19 plus the verifier row-69 caveat.
- Independent verifier re-verification: all 5 re-checked items REPRODUCED (F-4 rollup, F-6 cross-tab, 255 non-active count, row-69 median basis, headline sanity). One sensitivity recorded: the F-4 rollup counts depend on treating hyphenated unit identifiers as single identifiers per the documented rule; a hyphen-destroying variant reads 1,964 / 38 / 157 with max unchanged at 17.
- N-1 (adversarial re-verification, minor): the Finding 2 sentence quoting TOT_UNITS of 125 to 579 on the other multi-license parcels and one TOT_UNITS 0 common-element parcel was true (independently recomputed: 0, 1, 125, 218, 232, 274, 282, 282, 292, 319, 372, 579) but had no stats.json figure. CLOSED by adding stats.json key multi_parcel_tot_units_active with the full list and provenance. No prose changed.
- N-2 (adversarial re-verification, minor): the X thread item 2 phrase "Concentration by holder is effectively zero" is an unscoped summary in the spirit of the removed F-2 framing. Left as a FLAG FOR ALEX at QA; it does not reopen F-2 and no number in the item is wrong.
- Open flags reserved for Alex: F-14 (renter-share sensitivity on the ACS denominator - not run), F-15 in part (neighborhood rate ranking noise), F-17 (assessor-owner layer exists in-stack, untested and disclosed as untested scope), N-2 above, and the standing definition call (Delinquent treated as never active; sensitivity in F-10 shows the headline is immaterial to it).

## Pre-publication conservative resolutions (2026-10-20)

Context: Alex's 2026-10-20 standing rule change pre-authorizes GitHub
publication of Machine Readable packages that pass QA and the audit gates,
and delegates the three Section 11.3 items left open above (F-14, F-15 in
part, F-17) to be resolved in the conservative direction. Resolutions,
applied 2026-10-20 before publication; each was then re-verified against
the edited artifacts (the added sentences carry no new figures except the
already-verified Whittier 27.1 and Cole 24.8 rates):

- F-14 (ACS denominator tenure) - RESOLVED conservatively, sensitivity not
  run. Finding 3 of brief-draft.md and substack-draft.md now states, in
  the finding itself (not only in Methods): because the denominator counts
  every housing unit, including owner-occupied homes, the neighborhood
  ranking partly reflects tenure mix as well as licensed STR intensity,
  and no per-renter-occupied-unit sensitivity was computed in this brief.
  The claim is softened in place; no figure changed.
- F-15 (ranking noise) - RESOLVED conservatively. The median basis was
  already stated wherever the median is printed (row-69 disposition
  above). Finding 3 of brief-draft.md and substack-draft.md now also
  carries the stability sentence the reviewer proposed: the top of the
  rate table rests on small counts over area-allocated denominators, so
  small gaps between adjacent rates (Whittier 27.1, Cole 24.8) sit within
  plausible allocation noise and should not be read as a precise ordering.
- F-17 (assessor-owner layer) - RESOLVED conservatively, layer not run.
  A Data-notes bullet in brief-draft.md and substack-draft.md now states
  that property-ownership concentration was not tested in this brief, that
  the warehouse's assessor records carry owner names, and that no
  licenses-per-assessor-owner count was run, so nothing in the brief
  speaks to how the licensed properties are owned. The brief ships with
  licensee-scope claims only, as reframed under F-2.
- N-2 (X thread item 2, "Concentration by holder is effectively zero") -
  RESOLVED by removal. The X thread was removed from social-drafts.md at
  publication: Machine Readable retired X on 2026-10-19 (Alex's rule) and
  packages no longer include X drafts. Nothing from the thread was posted.

With these resolutions, no Section 11 finding remains open on this
package: F-1 to F-19 all carry dispositions (fix loop above, coordinator
closure note above, and this section), and the verifier row-69 caveat is
closed. The remaining Section 11.3 flags (first use of the dataset, DLCP
named in Who can act, the surprising zero-concentration result, the strict
Delinquent definition) are disclosures, not open findings; the strict
active basis stands per F-10.
