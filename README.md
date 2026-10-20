# Denver STR licenses brief - package README

Topic (Alex's pick, 2026-10-19, arrived the morning of brief day): who holds Denver's
STR licenses and how concentrated are they - licensee concentration, neighborhood
footprint, and how the licensed footprint sits against the permit and housing layers in
the warehouse. Dataset: short-term rental license register of the Department of
Licensing and Consumer Protection (DLCP) (ODC_short_term_rental_licenses_active_or_
pending_renewal, layer 54; the dataset is still published under the Denver Excise and
Licenses name), fresh pull 2026-10-19. Mirrors the published Nashville STR brief
(2026-10-14) in the second locality of the stack.

Status: PUBLISHED 2026-10-20 to https://github.com/adowlen/denver-str-licenses-data-brief under Alex's 2026-10-20 standing rule (GitHub publication pre-authorized when QA and the audit gates pass; LinkedIn stays Friday-only and nothing was posted). The Section 11 independent verifier and adversarial passes are complete and the adjudicated fix loop was applied on 2026-10-19 (dispositions in verification.md, "Fix loop" section). The three items left open there (F-14, F-15 in part, F-17) plus N-2 were resolved in the conservative direction on 2026-10-20 before publication (verification.md, "Pre-publication conservative resolutions"): Finding 3 now carries the tenure-mix disclosure and the ranking-stability sentence in the finding itself, Data notes now state that property-ownership concentration was not tested, and the X thread was removed from social-drafts.md (X retired 2026-10-19). No figure changed in those resolutions.

## Headline result

2,083 active licenses under 2,080 licensee names: 2,077 licensees hold one license,
3 hold two, none holds more; 99.7 percent of active licenses are their holder's only
license; 0 active licenses are filed under a business-entity name. Concentration sits
on parcels (12 parcels, 84 licenses, all distinct holders) and in neighborhoods
(Whittier 27.1 licenses per 1,000 housing units; citywide 5.8).

## Contents
- brief-draft.md - the brief (publishable text)
- stats.json - every figure used in the brief and social copy, produced by code/build_stats.py
- verification.md - Section 10 pre-flight audit output, methods checklist, controls, warehouse deposit record
- reviewer-notes.md - claims most likely challenged, Section 11.3 flags, open items
- sources.md - dataset citations, field semantics, access notes
- social-drafts.md - LinkedIn page post and personal repost comment (drafts only; the X thread drafted with the package was removed at publication, per Alex's 2026-10-19 X-retirement rule)
- substack-draft.md - Substack cross-post draft
- hero.png - hero graphic (generated illustration + composited verified figure; code/hero_composite.py)
- charts/ - chart_bands.png, chart_neighborhood_rates.png, chart_vintage.png
- data/ - neighborhood_panel.csv (aggregate neighborhood panel), audit_output.txt
  (Section 10 audit output). No raw register file ships in the package: the raw
  snapshot lives only in the warehouse (fix loop F-1)
- code/ - pull_data.py, build_stats.py, audit_section10.py, leakage_scan.py,
  charts.py, hero_composite.py, deposit_warehouse.py
- hero_source/ - the raw generated illustration before compositing

## Dependencies (match code imports)
python 3.12; pandas, numpy, pyarrow (parquet), matplotlib, Pillow (hero composite).
No other third-party imports (Spearman correlations are computed on pandas ranks in
build_stats.py). Working venv: the crime brief package's ./.venv
(denver-crime-brief-2026-10-17/.venv).

## Rebuild order
1. code/pull_data.py (fresh register pull to the warehouse snapshot 2026-10-19 only;
   refuses to overwrite an existing snapshot; never writes a copy into the package)
2. code/build_stats.py (writes stats.json + data/neighborhood_panel.csv)
3. code/audit_section10.py (Section 10 gates; output to data/audit_output.txt)
4. code/deposit_warehouse.py (manifest registration + stack verification entry;
   idempotent)
5. code/charts.py, code/hero_composite.py
6. code/leakage_scan.py (F-1 gate: scans every package file for register values;
   must pass before the package is presented as ready)

## Data provenance
STR register: warehouse stack/denver/snapshots/2026-10-19/str_licenses.parquet
(fresh pull, 2,338 rows; pull log pull_log_str_2026-10-19.json beside it).
Drift baseline: snapshots/2026-10-15/str_licenses.parquet (2,349 rows) and its cleaned
layer layers/str_licenses_clean.parquet (the parcel bridge). Neighborhoods and permit
aggregates: joins/parcel_spine_v6.parquet. Denominators: ACS 2024 5-year B25001 via
layers/acs_neighborhood_units.parquet (same basis as the crime and traffic briefs).
Warehouse deposit from this study: the 2026-10-19 snapshot registered in the manifest
(denver_str_licenses) with a study-deposit entry in stack/denver/verification.md.

## Product rules applied
Aggregates only, in every shipped file category: no licensee name, street address,
parcel number, or TAX_ID value appears in the brief, the substack or social drafts,
stats.json, the data/ files (aggregate neighborhood panel and audit output only),
the code/ files, the charts, or the hero. The raw register snapshot is archived
only in the warehouse and is never copied into the package. Fix loop F-1
(2026-10-19): the adversarial review found a raw working copy of the snapshot in
data/ (2,338 rows with names, addresses, parcel numbers, and TAX_IDs); it was
deleted, code/pull_data.py no longer writes one, and code/leakage_scan.py scans
every package file for register values (output recorded in verification.md).
Licensee names are used transiently inside code to compute concentration; the
audit prints anonymized evidence only.
