# Sources - Denver STR licenses brief (2026-10-19)

## Primary dataset
- Denver Open Data Catalog, ODC_short_term_rental_licenses_active_or_pending_renewal
  (short-term rental licenses), ArcGIS FeatureServer layer 54:
  https://services1.arcgis.com/zdB7qR0BtYrg0Xpl/ArcGIS/rest/services/ODC_short_term_rental_licenses_active_or_pending_renewal/FeatureServer/54
  Publisher: Department of Licensing and Consumer Protection (DLCP); the dataset is
  still published under the Denver Excise and Licenses name. Dataset landing page (per the warehouse manifest):
  https://denvergov.org/opendata/dataset/city-and-county-of-denver-short-term-rental-licenses
  Fresh snapshot: full-service pull 2026-10-19 (2026-10-19T11:27:59Z), 2,338 records;
  service last edit 2026-10-19T09:44:04Z (editingInfo at pull time). Archived at warehouse
  stack/denver/snapshots/2026-10-19/str_licenses.parquet (sha256 in the pull log next to it
  and in the manifest).
  Prior snapshot (drift baseline and bridge source): 2026-10-15 pull, 2,349 records,
  stack/denver/snapshots/2026-10-15/str_licenses.parquet.

## Field semantics (established from the service itself, 2026-10-15 and 2026-10-19)
- LICENSE_STATUS: five values, counted exhaustively before any filter on both snapshots.
  Fresh: License Issued - Active 2,083; Delinquent 137; Closed - Expired 116;
  About to Expire 1; Closed - Surrendered 1. Despite the service name ("active or pending
  renewal"), the table carries delinquent and closed records: any "active" figure must
  filter on status. This brief's active basis is the exact string
  "License Issued - Active" and nothing else.
- LICENSE_TYPE: "Short Term Rental" on every record in both snapshots.
- ENTITY_NAME: the licensee name as filed; the holder key for this brief after
  normalization (uppercase, whitespace collapsed). It is lineage in the warehouse cleaned
  layer and an analysis field here only in aggregate (counts, shares, bands). No licensee
  name appears in any published artifact of this package.
- PARCEL_NUM: the assessor schedule number. Fresh snapshot: 2,336 rows carry a 13-digit
  value; 1 row carries a 12-digit value (leading zero dropped; zfill-normalizes to a
  spine key); 1 row carries a legacy dashed number (not keyable; recovered by address in
  the Phase 3 bridge). TAX_ID is present in the raw service and was NOT carried into any
  analysis file (warehouse data-minimization rule, Phase 3).
- MULTIPLE_LICENSES: constant "Stand Alone" on all 2,338 fresh records, including records
  on multi-license parcels. Not a usable signal; multi-license parcels in this brief are
  computed from the parcel bridge, never from this field.
- RELATIONSHIP: null on all records. RENEWAL_STATUS: populated on non-active records
  only in the fresh pull (top values Awaiting Customer Response 90, Inactive 64,
  Pending 63); no figure in this brief rests on it.
- EXPIRATION_DATE: a text date in the raw service. 47 active-status records carry an
  expiration date before the 2026-10-19 pull date; the disagreement is reported in
  Finding 5 without a compliance claim.
- ORIG_ISSUED_DATE / MOST_RECENTLY_ISSUED_DATE: epoch-millisecond timestamps; vintage in
  Finding 5 uses ORIG_ISSUED_DATE converted to America/Denver.

## Parcel bridge and neighborhood assignment
- Warehouse cleaned layer layers/str_licenses_clean.parquet (built 2026-10-15, Phase 3):
  the parcel bridge for 2,337 of the 2,338 fresh records, inherited by LICENSE_NUM
  (key 2,321; address_strict 13; unmatched 3). The one license that entered after
  2026-10-15 was key-matched on PARCEL_NUM against parcel spine v6. Fresh match outcome:
  2,335 of 2,338 matched (99.87 percent), the same rate as the Phase 3 bridge.
- Neighborhood: parcel spine v6 (stack/denver/joins/parcel_spine_v6.parquet, built
  2026-10-15) neighborhood of the assigned parcel (the city's 78 statistical
  neighborhoods, official ODC boundaries). 2,080 of 2,083 active licenses carry a
  neighborhood; the 3 without are exactly the 3 bridge-unmatched licenses.
- Parcel unit count for the largest multi-license parcel (579 units) is TOT_UNITS on the
  spine record for that parcel (assessor parcels layer, 2026-10-15 snapshot), reported
  as the parcel record's figure, not as a count of licensed units.

## Comparison and denominator layers (warehouse)
- Permits: spine v6 new_building_permit_count aggregates (new-building permits issued
  2020-01-01 to 2026-10-12, surviving-parcel basis, from layers/permits_clean.parquet,
  79,757 records as snapshotted 2026-10-15). The same permit basis as the October 15,
  2026 net housing change brief.
- Denominators: US Census Bureau, American Community Survey 2020-2024 5-year estimates,
  table B25001 (housing units), tract level, Denver County, via Census Reporter; allocated
  to the city's 78 statistical neighborhoods by tract area share (warehouse layer
  acs_neighborhood_units.parquet; Denver County total 359,581 units, 359,351 allocated).
  Same denominators as the October 17 and 18, 2026 briefs.

## Program rules context (the city's own documents)
- City and County of Denver, Department of Licensing and Consumer Protection,
  "Short-term rental frequently asked questions," denvergov.org:
  https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Business-Licensing/Business-licenses/Short-term-rentals/Short-term-rental-FAQ?lang_update=638598197018372468
  Fetched and read in full in the fix loop (2026-10-19). The FAQ states the eligibility
  rules this brief relies on, in the city's own words: primary residence is "the place
  in which a person's habitation is fixed for the term of the license and is the
  person's usual place of return"; "A person can have only one primary residence";
  the STR location is "always a single residential dwelling unit"; and the Department
  requires documentation of primary residency on application and renewal, applying
  the criteria in the Denver Revised Municipal Code. The eligibility consequence is
  stated in Finding 1: the licensee is a person licensing their one primary
  residence, a single dwelling unit, so the register's name field cannot distinguish
  an unconcentrated licensed market from a one-license-per-person intake.
  Fix loop F-3 (2026-10-19): this city document replaces the University of Denver,
  Sturm College of Law summary ("The Sharing Economy Matures") as the package's
  program-rules citation; the law-school PDF is no longer relied on for program
  rules. The brief states the rule as program context only; it tests no license
  against it.

## Budget calendar (Who can act)
- City and County of Denver, Denver City Council news release, "Denver City Council Makes Budget Recommendations," published October 9, 2026, denvergov.org: https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Denver-City-Council/News/2027-budget-recommendations - the four 2027 budget dates used in the brief: final proposed budget due October 19, 2026; public hearing October 26; last amendment vote November 2; final passage November 9 (charter deadline). Verified live 2026-10-18 during the traffic brief's QA run; the same citation is carried here.
