# Reviewer notes - Denver STR licenses brief (2026-10-19)

## Claims most likely to be challenged, and where the defense lives

1. "99.7 percent of active licenses are their holder's only license" (headline, hero,
   social). Basis: normalized ENTITY_NAME on the fresh 2026-10-19 snapshot, 2,077 of
   2,083 active licenses (stats.json concentration_active). The defense is the three-way
   re-derivation in verification.md: exact names, first-and-last-token merge (identical
   result), and the deliberate first-initial-and-surname over-merge (max group 4; 92
   licenses, 4.4 percent, in groups of 2+, printed in Finding 1 as an upper bound on
   splitting by middle names and initials only, not a measurement; it cannot bound
   splitting across a changed surname, a name-order swap, or a suffix keyed as the
   surname token, per fix loop F-9). The honest limit is also printed: the register cannot see common
   control exercised through different people's names, and the brief says so in Finding
   1, the Data notes, and "What this might mean."

2. "No active license is held under a business-entity name" (Finding 1). This is the
   claim with the largest semantic risk in the package. It is a classification of the
   ENTITY_NAME string by a documented 60-token rule, not a determination of ownership:
   a sole proprietor, a host whose property sits in an LLC but who licensed personally,
   or a manager filing for clients under personal names would all read as individual
   names. The brief states that scope in the finding itself ("a classification of the
   name as filed, not of beneficial ownership"). The 0.0 percent business share and the
   0.0 percent not-determined share are printed with their counts (0 and 0 of 2,083) so
   a challenger can see exactly what was counted. If Alex wants this claim softened
   further, the fallback sentence is already in the brief: "no active Denver STR license
   is held in the name of a company, trust, or partnership that the register can see."

3. "Licenses stack on parcels" (Finding 2). The 32-license parcel could be misread as
   one operator with 32 licenses; the brief's own check (all 84 multi-parcel licenses
   under distinct holder names; the largest parcel's assessor record carries 579
   units) is printed in the finding. Addresses and the parcel key are deliberately NOT
   printed: the largest parcel is identified only as "one parcel in the Union Station
   neighborhood," per the product rule against publishing individual licensee addresses.
   The neighborhood attribution comes from the spine record for that parcel.
   Fix loop F-4 (2026-10-19): the adversarial reviewer correctly noted that parcels
   are not buildings (condo units are individual parcels). Finding 2 now also prints
   a proper base-address rollup (unit designators stripped systematically): 39
   multi-license base addresses holding 159 licenses, maximum 17, 27 spanning more
   than one parcel, every license again under a distinct holder name. The one parcel
   carrying 4 licenses against a TOT_UNITS of 1 is explained in the finding from its
   own record: a RESIDENTIAL-CONDOMINIUM master parcel (126,465 sq ft condo structure,
   built 2018), not a single-unit house.

4. Fusion rho 0.64 (Finding 4). A correlation across 75 neighborhoods on rates that
   share one denominator. The brief prints the two sensitivities next to it (raw-count
   rho 0.62; including DIA, 0.60) and labels the claim geographic, not causal, with the
   direction-of-causality caveat in the finding. The permit basis is the spine v6
   surviving-parcel aggregate (2020-01-01 to 2026-10-12), not a fresh permit pull; if a
   challenger asks, the window and basis are in Methods.

5. The 47 status/expiration disagreements (Finding 5). Printed as a disagreement
   between the register's own fields, with an explicit no-conclusion sentence. A
   challenger from the licensing office could explain these as renewal-grace records;
   the brief pre-answers by claiming nothing about any license's standing and routing
   the question to the office in the Who can act item. Fix loop F-6 (2026-10-19):
   Finding 5 now prints the cross-tab (29 of the 47 were most recently issued in
   2025-2026; expiration lag median 230 days, maximum 1,374 days, 20 over one year;
   4 were re-issued after their printed expiration date), and the Who can act item
   now asks the office to publish which field is authoritative when status and
   expiration disagree, with success measured by that documentation existing, not by
   a zero count.

## Checks that could not be completed

- Platform-side activity (nights rented, listing presence) is not observable from any
  warehouse layer; the brief never claims it. The unlicensed segment is likewise
  unmeasurable from the register and is framed as a data gap, not a finding.
- The independent verifier and adversarial reviewer passes have now run (ledgers in
  this package); the fix loop was applied 2026-10-19 and every disposition is
  recorded in verification.md. Two items remain open as flags for Alex: F-14
  (renter-share sensitivity on the ACS denominator, not run) and F-17 (the in-stack
  assessor-owner layer, neither run nor, until this note, disclosed as untested;
  see the Section 11.3 flags).
- The denvergov.org dataset landing page could not be text-fetched during the build
  (the page returned no extractable content); the landing URL is cited from the
  warehouse manifest, which recorded it at the Phase 3 build, and the live ArcGIS
  service itself was queried directly for every figure.

## Surprises

- The headline is an absence: measured holder concentration in the licensed register
  is zero in every band above 2, and there are no business names at all. The fix loop
  (F-2) reframed the claim to what the data earn: licenses are filed one per person
  under personal names, the shape the primary-residence intake rules require, and the
  register has no field that could reveal common ownership behind those names. The
  Nashville STR brief (2026-10-14) found a visible investor segment; Denver's
  register shows the opposite shape. The brief reports this as a measured pattern,
  not as proof of compliance.
- The source's own MULTIPLE_LICENSES field reads "Stand Alone" on all 2,338 records
  while 13 parcels carry multiple licenses. Anyone quoting that field would report
  zero multi-license parcels.
- The register moved measurably in four days (active minus 15 on a 2,098 base), which
  is why the brief dates every count.

## Section 11 pipeline record

- Builder: package assembled 2026-10-19 morning (brief-day build; the pick arrived
  05:25 MDT). Fresh pull taken the same morning; Section 10 audit passed before
  drafting (data/audit_output.txt).
- Independent verifier: COMPLETE. Ledger in this package
  (verification-ledger-independent.md): 89 figures checked, 88 reproduced, 1
  caveated (row 69, the median neighborhood rate's basis; the basis is now stated
  wherever the median is printed).
- Adversarial reviewer: COMPLETE. Report in this package (adversarial-review.md):
  findings F-1 to F-19 (1 BLOCKING, 8 SHOULD-FIX, 10 FLAG-FOR-ALEX). Fix loop
  applied 2026-10-19; every disposition is recorded in verification.md.
- Product rules, corrected in the fix loop: the original claim in this section
  enumerated only the prose artifacts and was WRONG about the package as shipped:
  a raw working copy of the snapshot sat in data/ with every licensee name, street
  address, parcel number, and TAX_ID (finding F-1, BLOCKING). Found and fixed
  2026-10-19, never omitted from this record: the file was deleted (the archived
  snapshot remains in the warehouse), pull_data.py no longer writes a package
  copy, and code/leakage_scan.py now scans every file in the package (brief,
  substack and social drafts, stats.json, data/, code/, charts/, hero, and all
  markdown) for register values; its post-fix output is recorded in
  verification.md. Aggregates only, in every shipped file category.

## Section 11.3 flags for Alex

- F-1 (found and FIXED in the fix loop, recorded here so it is never omitted): the
  package as built shipped a raw working copy of the register in data/ containing
  every licensee name, street address, parcel number, and TAX_ID. The file was
  deleted 2026-10-19, the warehouse snapshot remains the only raw copy, and a
  leakage scan over the whole package passes (verification.md). Blocking at review;
  closed on evidence.
- F-5: three names hold two active licenses each on distinct parcels, in tension
  with the one-primary-residence rule the brief cites. Finding 1 now prints the
  pattern with the innocent mechanisms (mid-term move, overlapping renewal) and
  draws no conclusion. Flagged so Alex sees the tension was printed, not buried.
- F-7: the administering department's current name is the Department of Licensing
  and Consumer Protection (DLCP); the package originally used the retired Excise
  and Licenses name throughout, including in Who can act. Fixed: DLCP is used
  wherever the brief addresses the department, with one parenthetical noting the
  dataset is still published under the Excise and Licenses name.
- F-17 (OPEN for Alex): an in-stack assessor-owner layer exists (the warehouse
  parcels layer carries assessor owner names as lineage), and a
  licenses-per-assessor-owner count is the closest available test of
  property-level concentration behind the personal licensee names. Disclosed here
  as untested scope: property-ownership concentration was NOT tested in this
  brief, and the owner layer was not run. Alex's call whether to run it or ship
  with the licensee-scope claims as reframed.
- Naming an agency: the Who can act section names the Department of Licensing and
  Consumer Protection (DLCP) with two register-hygiene items (publish a holder
  summary; publish which field is authoritative when status and expiration
  disagree). This is the standing agency flag.
- First use: the STR register is the primary dataset of a brief for the first time
  (warehouse layer since 2026-10-15; previously a readout section only). The service
  name misdescribes its contents (10.9 percent non-active records) - flagged in the
  brief's Data notes.
- Surprising result: zero measured holder concentration and a 0.0 percent
  business-entity share (claim 2 above). Verified three ways before printing.
- Definition issue for your call: whether "Delinquent" licenses (137) should ever be
  described as part of the operating footprint in social copy. The package's line is
  strict: active means the exact Active status, everywhere, and delinquent counts are
  printed only as register composition. If you want the delinquent bucket treated
  differently at QA, Finding 5 and the Methods are where it would change.
- Repo name follows the series pattern (adowlen/denver-str-licenses-data-brief);
  nothing has been created, pushed, posted, or sent.

## Publication-day resolutions (2026-10-20)

Under Alex's 2026-10-20 standing rule (GitHub publication pre-authorized
on QA and audit gates), the three items left open above were resolved in
the conservative direction before publication; full record in
verification.md, "Pre-publication conservative resolutions (2026-10-20)":
F-14 resolved by strengthening the tenure disclosure in Finding 3 (the
per-renter-occupied sensitivity was not run); F-15 resolved by adding
the ranking-stability sentence to Finding 3 (median basis was already
stated); F-17 resolved by adding a Data-notes sentence stating that
property-ownership concentration was not tested and the assessor-owner
layer was not run. N-2 was resolved by removing the X thread from
social-drafts.md (X retired 2026-10-19). No figure changed.
