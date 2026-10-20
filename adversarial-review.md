# Adversarial Review - Denver Short-Term Rental Licenses Brief (2026-10-19)

Reviewer role: Section 11.1 step 4 adversarial pass (attack, not approve),
with the Section 12.8 physical-falsifiability brief (attack as a
knowledgeable Denver local). Standards applied: brief-writing-standards.md
Sections 2, 3, 11.3, 12.1/12.4/12.5/12.7/12.8.

Materials read end to end: brief-draft.md, stats.json, sources.md,
verification.md, reviewer-notes.md, social-drafts.md, substack-draft.md,
all three charts and hero.png (viewed), code/build_stats.py, the stack
README STR section (Phase 3 additions), and the denver_str_licenses
manifest entry. The independent verifier's ledger
(verification-ledger-independent.md) was read in full and its counts are
relied on where noted; every other number below was recomputed by this
reviewer from the raw snapshot (data/str_licenses_raw_2026-10-19.parquet)
with independent code. Denver program rules were checked against the
City and County of Denver's own STR FAQ on denvergov.org (primary
residence = the place where habitation is fixed for the license term and
the person's usual place of return; a person can have only one primary
residence; the STR location is always a single residential dwelling unit).

Bottom line up front: every number in this package reproduces. The
arithmetic is not the problem. The problems are (1) one blocking privacy
breach in a shipped data file, (2) a headline that converts an
eligibility-rule artifact of a personal-name intake field into a market
finding, and (3) several places where the prose claims one layer more
than the layer measured. Severity tally: BLOCKING 1, SHOULD-FIX 8,
FLAG-FOR-ALEX 10.

---

## BLOCKING

### F-1. The package ships every licensee's name, street address, and TAX_ID in data/str_licenses_raw_2026-10-19.parquet - product-rule breach

- Count: the file is the full raw snapshot: 2,338 rows with columns
  ENTITY_NAME, ADDRESS, ZIP, PARCEL_NUM, and TAX_ID for every record
  (verified by reading the parquet's schema and row count in this pass).
- Mechanism: the builder copied the raw warehouse snapshot into the
  package as a "working copy" (README lists it under data/), and the
  package's product-rule checks enumerated only prose artifacts.
  reviewer-notes.md claims "no licensee name and no street address
  appears in stats.json, the brief, the charts, the hero, or the social
  copy" - a list that silently omits the one file that contains all of
  them. verification.md makes the same omission. The social drafts then
  promise a public repo with "methods and data," and the warehouse's own
  data-minimization rule (Phase 3) dropped TAX_ID from the cleaned layer
  precisely so this identifier would not circulate; the raw copy
  re-imports it.
- Proposed treatment (the fix I would accept): remove the raw parquet
  from the publishable package before any repo is created (the archived
  snapshot already lives in the warehouse, which is where it belongs);
  if a data file ships, it is the aggregate neighborhood panel and
  banded holder counts only, with no name, address, parcel number, or
  TAX_ID at any grain. Correct the product-rule sentences in
  reviewer-notes.md and verification.md to enumerate every file in the
  package, including data/ and code/. This finding is BLOCKING under the
  task's privacy rule regardless of the fact that the source register is
  itself public: the product rule for this series is aggregates only,
  and TAX_ID republication is a new exposure the source's own warehouse
  handling already decided against.

## SHOULD-FIX

### F-2. Headline framing: "concentration is structurally absent" overclaims what a name count on a rule-capped register can show

- Count: CORRECT. 2,083 active licenses, 2,080 distinct normalized
  names, 2,077 singleton holders, 3 holders with 2, maximum 2;
  99.71 percent of active licenses are their holder's only license.
  Reproduced by the builder, the independent verifier (ledger rows
  26-36), and this reviewer.
- Mechanism: OVERSTATED. Denver's licensing intake makes this result
  substantially structural by design, in a stronger sense than the
  brief ever states. Per the city's own STR FAQ, the licensee is a
  person whose primary residence the unit is; a person can have only
  one primary residence; the STR location is always a single
  residential dwelling unit. An applicant who is a company, or a person
  seeking a fifth license, cannot file that way at all. A name-field
  count on such a register therefore cannot distinguish "the licensed
  market has no concentrated operators" from "the intake form only
  admits one license per natural person" - the register would read flat
  under both worlds, including a world of concentrated property
  ownership behind the names. The brief's caveats cover beneficial
  ownership through other people's names (Finding 1, Data notes, "What
  this might mean" alternative 2), but nowhere state the intake-design
  point, and the framing language spends the stronger claim anyway:
  reviewer-notes.md calls concentration "structurally absent"; the
  lede calls the register "as unconcentrated as a register can be";
  Finding 1's heading says "there is no concentration to measure"; the
  "What this might mean" settlement sentence says "within the licensed
  system, there is no holder concentration." Section 2 requires the
  one-line summary to be a finding a skeptic could verify from the
  data, not a conclusion about what it means.
- Proposed treatment: keep every number; reframe the claim to the
  narrower true one - licenses are filed one per person under personal
  names, which is the shape the primary-residence intake rules require,
  and the register contains no field that could reveal common ownership
  or control behind those names. Delete "structurally absent" wherever
  it appears, qualify Finding 1's heading and the settlement sentence
  with "by licensee name as filed," and add the intake-design sentence
  to Finding 1 and the Data notes. The hero figure (99.7 percent) can
  stay; its caption already carries the counts.

### F-3. The 0.0 percent business-entity finding: count is real, rule is not circular, but the brief never establishes whether an entity could file at all

- Count: CORRECT, and the circularity attack fails. This reviewer
  re-ran a token census over all 2,338 names: zero occurrences of any
  entity token family (no LLC, TRUST, ESTATE, TRUSTEE, FAMILY, DBA,
  MGMT, or similar token anywhere in the register). The independent
  verifier's broader rule (adding TRUSTEE and ESTATE singular) and
  substring scans also return 0 on all three bases (ledger rows 37-40
  and classification deep-dive). The 60-token rule did not manufacture
  the zero; the field contains no entity-style strings.
- Mechanism: the finding's meaning is undetermined by the package.
  Every name in the register is a 2-to-5-token personal name. That is
  consistent with two very different worlds: (a) entities and trusts
  are eligible applicants and none chose to file, or (b) ENTITY_NAME
  is the individual applicant's name by system design, in which case
  0.0 percent is a property of the form, not of the market. The brief
  never establishes which. Its only program-rules citation (sources.md)
  is a University of Denver law-school PDF summarizing requirements -
  a secondary source - where Section 3 requires the city's own
  definitions from the city's own document. Secondary guidance found
  in this pass states a Denver STR license may sit in the name of a
  natural person, a trust, or a nonprofit, which if true makes the
  zero-trust result substantive; the brief neither cites nor tests
  that eligibility question, yet Finding 1 spends the result as ruling
  out "the corporate-holder pattern" and the settlement sentence
  repeats "no corporate-name holding" without the "as filed" scope
  that Finding 1's own careful sentence carries.
- Proposed treatment: cite the city's own STR FAQ / Denver Revised
  Municipal Code for the primary-residence rule and for who may hold
  a license (natural person only, or trusts/nonprofits eligible), and
  state the consequence in one sentence in Finding 1: either "entity
  applicants are not accepted, so this measures the form" or "trusts
  may hold licenses and none appear." Move the "classification of the
  name as filed, not of beneficial ownership" scope sentence into the
  lede and into the "What this might mean" settlement sentence so the
  caveat travels with the number everywhere the number appears
  (Section 12.5's spirit; the number itself is consistent - see F-18).

### F-4. Finding 2: parcels are not buildings, and the brief's own warehouse rule says so

- Count: CORRECT on the parcel basis. 12 multi-license parcels, 84
  active licenses, maximum 32, every license under a distinct holder
  name (ledger rows 48-53; this reviewer reproduced the parcel table
  and the per-parcel assessor unit counts).
- Mechanism: the prose converts a parcel result into a building claim
  ("The stacking is by building, not by operator"; "the only form of
  license stacking the register contains"). The stack README's
  canonical-key section states the opposite convention: condo units
  are individual parcels with their own schednum, and building-level
  statements must aggregate units first. A parcel rollup therefore
  splits condo buildings across parcels by construction, and the
  brief's only address check used full address strings (unit identity
  kept), which cannot detect building-level clustering either. This
  reviewer's crude base-address rollup (unit designator stripped from
  the address string) finds a different picture the brief never
  computed: 19 multi-license base addresses holding 63 active
  licenses, maximum 17 at one base address, 13 of the 19 spanning
  more than one parcel. The rollup is indicative, not definitive
  (address formats vary), but it proves the building-level question
  was never actually asked. A second loose thread: one of the 12
  parcels carries 4 active licenses against a TOT_UNITS of 1 on its
  own assessor record, which the "licensed unit by unit" story does
  not explain (the other 11 sit on records of 125 to 579 units).
- Proposed treatment: either (a) run a proper base-address / building
  rollup, print it beside the parcel table, and explain the
  TOT_UNITS=1 parcel, or (b) restrict Finding 2 strictly to parcel
  language - delete "by building" and "the only form of license
  stacking the register contains," and add one sentence stating that
  condo buildings spread across unit parcels are not aggregated here.
  Option (a) is the better brief; option (b) is the minimum honest fix.

### F-5. The three two-license holders sit in unexplained tension with the one-primary-residence rule the brief itself cites

- Count: CORRECT. Three holders with exactly 2 active licenses each;
  each pair is two distinct license numbers on two distinct parcels at
  two distinct addresses (builder Control B; ledger row 41). This
  reviewer adds, in aggregate only: the pairs' original issue years
  are years apart (2017+2026, 2022+2025, 2024+2026), and two of the
  three pairs are in different ZIP codes.
- Mechanism: the brief uses the pairs for exactly one purpose - to
  prove they are not duplicate filings - and then moves on. But under
  the rule printed two paragraphs later (one person, one primary
  residence, one single dwelling unit), two simultaneous active
  licenses under one name is the most rule-relevant pattern in the
  entire register. Innocent mechanisms exist and are plausible
  (a mid-term move with the old license not yet surrendered, an
  overlapping renewal and new license), which is exactly why the
  brief should print the tension with the mechanisms alongside, the
  way Finding 5 handles the 47 past-expiration records. Printing
  nothing leaves the inference to the reader: a licensing-office
  reader will spot it instantly (Section 12.8), and a hostile reader
  will read the silence either as a miss or as an implied violation
  the brief was too cautious to state. Section 2 forbids both.
- Proposed treatment: one short neutral paragraph in Finding 1 noting
  that three names hold two active licenses on distinct parcels, that
  Denver's rule contemplates one primary residence per person, that
  the register cannot show whether these are moves or overlaps in
  progress, and that no conclusion about any license follows - the
  same no-conclusion discipline Finding 5 already uses.

### F-6. The 47 past-expiration actives: Finding 5 is careful, but the mechanism was never tested and Who can act demands the wrong fix

- Count: CORRECT. 47 active-status licenses (2.26 percent) carry an
  expiration date before the October 19, 2026 pull (ledger row 74).
- Mechanism: UNTESTED, and the data in the register point away from
  the simple reading. This reviewer's recomputation: the lag is a
  median of 230 days and a maximum of 1,374 days (20 of the 47 expired
  more than a year before the pull), yet 29 of the 47 carry a
  MOST_RECENTLY_ISSUED_DATE in 2025 or 2026 - i.e., most of these
  licenses were acted on recently while their expiration field stayed
  old. That pattern is consistent with EXPIRATION_DATE not advancing
  on renewal (a stale-field artifact), and city guidance also allows
  a complete pending renewal to continue operating while it is
  reviewed. Finding 5 itself claims nothing, which is correct. But
  Who can act escalates the item into a task for the licensing office
  - "reconcile the 47 records" - with a success criterion of "zero
  active-status records with a past expiration date." If the field
  is an original-term date, that target asks the office to falsify a
  correct field, and the office can dismiss the whole item, taking
  the brief's credibility with it.
- Proposed treatment: run and print the MOST_RECENTLY_ISSUED
  cross-tab for the 47 in Finding 5 (one sentence: how many were
  re-issued after their printed expiration date), and rewrite the
  Who can act item to ask the office to document which field is
  authoritative for a license's current term, with success stated as
  that documentation existing - not as a zero count.

### F-7. Who can act is addressed to a department name the city has retired - and the package knows it

- Count: not a count; a naming fact. The brief, sources.md, and
  social copy say "Department of Excise and Licenses" throughout.
  The package's own stats.json meta field records the publisher as
  "Denver Excise and Licenses (now the Department of Licensing and
  Consumer Protection)." Current city pages administer the STR
  program under the Department of Licensing and Consumer Protection.
- Mechanism: internal inconsistency plus a Section 12.8 local-
  knowledge failure. Denver readers - including the office being
  asked to act - know the current name. A "Who can act" item addressed
  to a renamed department, in a brief whose own metadata acknowledges
  the rename, reads as not knowing the ground. reviewer-notes.md
  flags "naming an agency" under Section 11.3 but not the rename.
- Proposed treatment: use the current department name in Who can act
  and the lede, with one parenthetical ("formerly Excise and
  Licenses; the dataset is still published under that name"), and
  align sources.md and stats.json wording.

### F-8. Finding 5's vintage story never discloses that the register purges its dead

- Count: CORRECT as a description of today's active stock (ledger
  rows 71-73: 61.0 percent of active licenses originally issued in
  2023 or later).
- Mechanism: the register is a rolling current register, not an
  archive: the brief's own drift section shows 12 license numbers
  leaving the table in four days, and across a decade of annual
  licenses the whole table holds only 253 non-active records. The
  issue-year distribution of licenses active today is therefore
  survivor stock. It cannot be read as issuance history, and the
  brief never says so: Finding 5's heading ("The register is young")
  and prose ("were first issued as follows"; "the register's center
  of gravity is the current decade's second half, not the program's
  2016 start") invite a growth reading that a purged register cannot
  support on its own. The vintage chart's title does say "active,"
  which makes the prose's looser framing the defect.
- Proposed treatment: one sentence in Finding 5 stating that the
  vintage describes licenses active today, that lapsed licenses leave
  this table (12 records in the four-day drift), and that the table
  is therefore not an issuance series for the program's history.

### F-9. The over-merge is printed as an "upper bound" on concentration; over the mechanism that matters, it is not one

- Count: CORRECT as computed. First-initial-plus-surname grouping:
  2,034 groups, maximum 4, 92 licenses (4.4 percent) in groups of two
  or more (ledger rows 42-44).
- Mechanism: the bound covers only one splitting mechanism - middle
  names and initials. It cannot catch an operator split across a
  surname change (marriage, divorce, hyphenation change), a name-order
  swap, or a generational suffix treated as the surname token (6
  active names end in a suffix token, and the merge keys on the last
  token). The brief's sentence - "that is an upper bound built by
  deliberately over-counting" - asserts a bound over identity
  splitting generally. It is an upper bound over initial/middle-name
  variation only. The Data notes' household sentence partly covers
  the gap, but the Finding 1 sentence stands unqualified where the
  headline's defense is made.
- Proposed treatment: qualify the sentence in place ("an upper bound
  on splitting by middle names and initials; it cannot bound
  splitting across a changed surname"), or drop the words "upper
  bound" for "a deliberately over-merged count."

## FLAG-FOR-ALEX (adjudicated items, scope calls, and places the brief survives attack)

### F-10. Delinquent treatment - attack fails; the brief's strict basis is sound and the sensitivity is immaterial

Count/mechanism/treatment adjudicated separately per Section 12.7.
Count: including Delinquent licenses in an "operating footprint"
(2,220 licenses) or Delinquent plus About to Expire (2,221) changes
the headline negligibly - this reviewer recomputed: 2,217 holders,
maximum 2, 4 holders with two, 99.64 percent of licenses held by
sole-license holders. Mechanism: the builder's worry in
reviewer-notes.md (should Delinquent ever count as operating?) is a
legitimate definition question but it cannot move any finding in
this package. Treatment: no fix required; optionally print the
one-line sensitivity in Finding 5 so the definition call is visibly
immaterial rather than asserted.

### F-11. TAX_ID was dropped untested as a holder key - tested here; it cannot rescue beneficial ownership (but see F-1)

This reviewer tested the key the builder discarded. Active licenses:
maximum licenses per TAX_ID is 1; TAX_ID is per-license/per-property
in practice (2,336 distinct values for 2,338 register rows; 4 holders
carry 2 TAX_IDs register-wide; 1 TAX_ID maps to 2 holder names
register-wide, none active). A TAX_ID-based concentration count would
show even less concentration and would prove nothing about persons.
The omission is immaterial to every count. The only TAX_ID problem
in the package is its presence in the shipped raw file (F-1).

### F-12. Household-level common control - the brief's caveat is conservative; a partial test exists and comes back empty

The brief says household-level control "cannot be seen in this
field." A partial test can in fact be run: same base address plus
same surname under two distinct holder names. This reviewer ran it
over the active register: zero such groups. The caveat could be
strengthened ("no two active licenses at the same address sit under
different names sharing a surname") if Alex wants the defense
printed; not required. Spouse pairs under different surnames and
manager-client structures remain invisible, as the brief states.

### F-13. Finding 4 (Spearman 0.64) survives attack - recorded so the fix loop does not relitigate it

Recomputed from the package panel: rho 0.643 on rates, 0.622 on raw
counts, 0.600 including DIA (all as printed). Robustness checks the
brief did not print: restricting to neighborhoods with at least
2,000 ACS units gives 0.655; excluding the zero-permit downtown trio
(CBD, Civic Center, Union Station) gives 0.665. The parcel-level
comparison also survives restricting STR parcels to those with a
characteristics record (10.9 percent vs 3.6 percent, against the
printed 10.6 vs 3.6). The prose stays inside co-location language;
no causal drift found. No fix required. One residual note: the
neighborhood-level demolition correlation is 0.647, the same as
permits, so the Methods' claim that the demolition layer "added no
claim" is a judgment call, honestly recorded as a cut.

### F-14. Neighborhood denominator: ACS housing units is defensible and disclosed, but it is tenure-blind

Licenses per 1,000 housing units counts owner-occupied houses in the
denominator of neighborhoods where the licensed stock is drawn from
the rental segment. The top-rate neighborhoods (Whittier, Cole,
Skyland, Clayton) are renter-heavy inner neighborhoods, so the
ranking partly encodes tenure mix, not only STR intensity. The brief
discloses this in one sentence in Finding 3 ("not per rental unit;
neighborhoods differ in tenure mix"). No number is wrong. Alex's
call whether a per-renter-occupied-unit sensitivity belongs in the
package; this reviewer would not block on it.

### F-15. Rate rankings rest on small counts and allocated denominators; the median's basis is unstated

Section 3's small-numbers rule is technically satisfied - every
printed rate carries its count (chart top-12 minimum is Regis with
21 licenses, count annotated). But the top of the rate table rests
on 21 to 61 licenses over area-allocated fractional denominators
(e.g., Whittier 2,251.0 allocated units); the Whittier-Cole gap
(27.1 vs 24.8) is within plausible allocation noise, and no stability
note says so. Separately, the independent verifier (ledger row 69)
found the printed median neighborhood rate of 4.7 is computed over
all 78 neighborhoods including the three zeros (over the 75 with
licenses it would be 5.04); the brief does not state the basis.
Fix if Alex wants it: state the median basis in Methods and add one
stability sentence to Finding 3.

### F-16. The zero-license neighborhoods are land-use zeros, and DIA's 3 licenses go unmentioned

Auraria (campus), Sun Valley (largely public housing and
redevelopment land), and Kennedy (golf-course area) hold zero active
licenses for structural land-use reasons, not market reasons; the
brief and the chart footnote list them flatly beside market
neighborhoods. Conversely the DIA statistical neighborhood carries
3 active licenses, which Finding 3 never mentions (DIA appears only
as Finding 4's exclusion). No number is wrong; one context sentence
would keep a Denver reader from falsifying the implication
(Section 12.8).

### F-17. An in-stack ownership layer exists and was neither run nor disclosed as untested

The warehouse parcels layer carries assessor owner names (held as
lineage, per the stack README). A licenses-per-assessor-owner count,
in aggregate, is computable from layers this package already joins,
and it is the closest available test of property-level concentration
behind the personal licensee names. The brief's claims are about
licensees, so this is a scope gap, not an error - but the "What this
might mean" settlement sentence ("no corporate-name holding") is
exactly where a reader will ask whether anyone checked who owns the
parcels. Alex's call: run it, or add one Data-notes sentence stating
that property-ownership concentration was not tested in this brief.

### F-18. Cross-document figures and voice - mostly clean; one social sentence steps past the finding

Section 12.5 check: the hook number is identical everywhere it
appears (99.7 percent in hero, LinkedIn, and X; 99.71 in stats and
brief prose, a rounding, not a mismatch), and this reviewer found no
stale figure in any draft, no en or em dashes in the publishable
drafts (Section 9), and no verdict words from Section 2's list in the
brief itself. The name-classification caveat travels in the LinkedIn
page post ("a name carrying a business-entity marker") and in X
("a name with an LLC, corporation, trust, or company marker"). The
one sentence that steps past the verified finding is the personal
repost comment: "Whatever Denver's short-term rental debate is
about, in the licensed register it is not about multi-unit
operators." It is scoped to the register, but it pronounces on the
debate; combined with F-2's intake-design problem, Alex may want
the narrower form ("in the licensed register there are no
multi-license operators to point to - three people hold two").

### F-19. Section 11.3 flag list in reviewer-notes.md is good but incomplete

The builder flags agency naming, first use of the dataset, the
surprising zero results, and the Delinquent definition call - all
correct flags. Missing from the list: the department rename (F-7),
the raw-file product-rule breach (F-1), the two-license/rule tension
(F-5), and the untested assessor-owner layer (F-17). Dispositions
for F-1 through F-9 should be recorded in verification.md before
this package is presented as ready, per Section 11.5 (no package
ships with an open adversarial finding).

---

## Verdict on the headline claim's honesty

The number is honest: 99.71 percent of active licenses are their
holder's only license, verified three independent ways, robust to
name-variant merging, to the Delinquent definition question, and to
a TAX_ID cross-check. The headline built on it is not honest as
framed. "Concentration is structurally absent" presents as a market
discovery a result that Denver's eligibility rules substantially
guarantee in advance: a register that only admits a natural person
licensing their single primary residence, recorded in a field that
contains only personal names, could not have shown corporate holders
or ten-license operators no matter how the underlying property
market is owned or managed. The strongest TRUE headline is the
narrower one the data actually earn: Denver's STR licenses are filed
one per person under personal names - exactly the shape the
primary-residence rules require - and the register contains no field
that could reveal common ownership or control behind those names.
With that reframing (F-2, F-3), the building claim repaired (F-4),
and the raw file pulled from the package (F-1), the package's
remaining findings are sound and, in several places (F-10, F-12,
F-13), stronger than the builder claimed.

---

## Re-verification (2026-10-19, second adversarial pass)

Method: every fix was checked on the current artifacts, not on the
fix report. Files read end to end: brief-draft.md, substack-draft.md,
social-drafts.md, README.md, verification.md, reviewer-notes.md,
sources.md, stats.json. data/ and code/ listed and inspected;
code/leakage_scan.py re-run by this reviewer with the package venv
(exit 0); independent greps for the banned F-2 strings, the retired
department name, the old F-6 success target, en/em dashes (codepoint
count), and the truncation marker; the TOT_UNITS distribution of the
12 multi-license parcels recomputed independently from the warehouse
spine and bridge.

### F-1 (BLOCKING, raw parquet / product rule) - CLOSED

- data/ now contains exactly two files: audit_output.txt and
  neighborhood_panel.csv (aggregate panel; header is neighborhood /
  ACS units / counts / rates only). No parquet anywhere in the
  package (full file listing checked).
- leakage_scan.py re-run by this reviewer: value sets 2,334 name
  forms, 2,663 address forms, 2,258 parcel numbers, 2,336 TAX_IDs;
  result "TOTAL VALUE HITS: 0" and "LEAKAGE SCAN: PASSED", exit 0.
  Independent greps find TAX_ID / ENTITY_NAME only as column names
  and rule prose, never as values, in any package file.
- code/pull_data.py writes only to the warehouse snapshot path and
  its header states the raw snapshot is never copied into the
  package; no package-copy write remains in the code.
- Corrected product-rule sentences enumerate data/ and code/:
  README.md ("no licensee name, street address, parcel number, or
  TAX_ID value appears in the brief, the substack or social drafts,
  stats.json, the data/ files ..., the code/ files, the charts, or
  the hero"); verification.md F-1 entry (data files named, scan
  described over stats.json, all markdown, code/, charts/, hero);
  reviewer-notes.md pipeline record ("scans every file in the
  package (brief, substack and social drafts, stats.json, data/,
  code/, charts/, hero, and all markdown)"); stats.json meta
  product_rule likewise enumerates data/ and code/.

### F-2 (headline framing) - CLOSED

- Grep of the whole package: "structurally absent", "as
  unconcentrated as a register can be", and "no concentration to
  measure" survive only inside this review and verification.md's
  fix-loop record (both expected). Zero hits in brief-draft.md,
  substack-draft.md, social-drafts.md, README.md, reviewer-notes.md.
- New lede (brief and substack, identical): "Denver's short-term
  rental licenses are filed one per person under personal names,
  which is the shape the program's primary-residence rules require"
  plus "the register contains no field that could reveal common
  ownership or control behind those names." Finding 1 heading is now
  "By licensee name as filed, licenses sit one per person." The
  settlement sentence is scoped: "within the licensed system, by
  licensee name as filed, there is no holder concentration."
- Intake-design sentence present in Finding 1 ("a name-field count
  cannot distinguish "no concentrated operators" from "intake only
  admits one license per natural person"") AND in Data notes (same
  sentence, semicolon form).
- Hero text (per code/hero_composite.py, the text actually drawn):
  "99.7%" / "of active STR licenses are their holder's only license"
  - numeric only, no old framing. Social hooks are likewise numeric;
  see NEW ISSUE N-2 for one residual X-thread phrase.

### F-3 (eligibility citation / scope sentence) - CLOSED

- sources.md program-rules section cites the City and County of
  Denver, DLCP, "Short-term rental frequently asked questions"
  (denvergov.org, full URL printed, "Fetched and read in full in the
  fix loop") and records that the University of Denver PDF "is no
  longer relied on for program rules"; the DU document survives only
  in that removal note, in verification.md's fix record, and in this
  review. The brief's Sources list cites the DLCP FAQ.
- Scope sentence in the lede: "That count is a classification of the
  name as filed, not of beneficial ownership" - and in the settlement
  sentence of "What this might mean": "That is a classification of
  the name as filed, not of beneficial ownership." Both present in
  brief and substack drafts.

### F-4 (parcels vs buildings) - CLOSED (see NEW ISSUE N-1)

- Finding 2 prints the base-address rollup and every number matches
  stats.json base_address_rollup_active: 1,963 base addresses; 39
  multi-license; 159 licenses (brief prints 7.6 percent; stats 7.63);
  maximum 17; 27 spanning more than one parcel; 12 on a single
  parcel; every license a distinct holder. The unsupported phrases
  "by building" (on parcel evidence) and "the only form of license
  stacking the register contains" are gone; the remaining building
  language ("gives the building-level picture", "multi-unit
  buildings licensed unit by unit") is now backed by the rollup
  printed in the same finding, and the X thread's building sentence
  prints the rollup numbers alongside.
- TOT_UNITS=1 explanation printed: RESIDENTIAL-CONDOMINIUM master
  parcel, master appendage, 126,465 sq ft condo structure built
  2018, no characteristics record, four unit filings by four
  holders - all matching stats.json tot_units_1_parcel.

### F-5 (three two-license holders) - CLOSED

- Finding 1 carries the neutral paragraph: pairs on distinct parcels
  at distinct addresses, issued years apart "(2017 and 2026; 2022
  and 2025; 2024 and 2026)", two of three pairs in different ZIP
  codes, the one-primary-residence tension stated, innocent
  mechanisms printed ("a mid-term move with the old license not yet
  surrendered, or an overlapping renewal and new license in
  progress"), and the explicit close: "no conclusion about any
  license follows from the count alone." The paragraph states a
  tension and mechanisms; it does not allege or hint at a violation
  by any holder (no holder is identifiable; the mechanisms are given
  equal weight with the tension).

### F-6 (the 47 / Who can act target) - CLOSED

- Finding 5 prints the MOST_RECENTLY_ISSUED cross-tab for the 47:
  "falls in 2025 or 2026 for 29 of the 47 (by year: 2023, 2; 2024,
  16; 2025, 20; 2026, 9)", lag "median of 230 days and a maximum of
  1,374 days", "20 of the 47 expired more than a year before the
  pull", "4 of the 47 carry a most-recent issue date after their
  printed expiration date" - all matching stats.json
  expiry_hygiene.past_expiration_cross_tab.
- Who can act now asks DLCP to "publish documentation of which
  field is authoritative when status and expiration disagree", with
  success stated as "the holder summary is published with the
  dataset and the field documentation exists." The old target
  survives nowhere as a criterion; its only remaining occurrence is
  verification.md's fix record, negated ("NOT "zero active records
  with a past expiration date" (the old success line was removed)").

### F-7 (department name) - CLOSED

- "Department of Licensing and Consumer Protection" is used in the
  lede and in Who can act, each with the parenthetical "(formerly
  Excise and Licenses; the dataset is still published under the
  Excise and Licenses name)". No shipped draft addresses a
  "Department of Excise and Licenses" as the current department;
  remaining "Excise and Licenses" mentions are the dataset-name
  parentheticals and historical quotes in this review. stats.json
  meta publisher and sources.md are aligned.

### F-8 (survivor stock) - CLOSED

- Finding 5 carries the sentence: "That distribution describes
  licenses active today, not the program's issuance history: lapsed
  licenses exit this table (the whole table holds only 255
  non-active records across a decade of annual licensing, and 12
  records left in the four days between the October 15 and October
  19 snapshots), so the issue-year distribution is a survivor stock,
  not an issuance series." Heading is now "The active register is
  mostly recent"; "register is young" survives only in this review
  and verification.md's fix record. X thread item 6 now reads "The
  active register is mostly recent and moving" - no growth phrasing.

### F-9 (over-merge bound) - CLOSED

- Finding 1 (brief and substack): "that is an upper bound on
  splitting by middle names and initials only, built by deliberately
  over-counting, not a measurement. It cannot bound splitting across
  a changed surname (marriage, hyphenation), a name-order swap, or a
  generational suffix keyed as the surname token." No unqualified
  "upper bound" remains in the brief; reviewer-notes.md claim 1
  carries the same qualification.

### F-18 (personal repost) - CLOSED

- social-drafts.md personal repost now reads in full: "Denver's STR
  register has 2,083 active licenses and 2,080 license holders.
  Three people hold two licenses; nobody holds three; no license
  sits under an LLC or trust name. The licenses are filed one per
  person under personal names, the shape Denver's primary-residence
  rules require." The old sentence ("Whatever Denver's short-term
  rental debate is about...") survives only as a quote in this
  review. The repost stays inside the reframed finding.

### Dispositions completeness - PASS

- verification.md "Fix loop" section has an entry for every finding
  F-1 through F-19 (all 19 present, in order) plus a separate entry
  "Verifier caveat, ledger row 69 (median basis) - FIXED", and the
  row-69 basis (all 78, zeros counted; 5.04 over the 75) is stated
  in Finding 3, Methods, stats.json, and the audit output.
- F-14 and F-17 are recorded as OPEN flags for Alex, not resolved:
  F-14 "FLAG-FOR-ALEX, OPEN ... was NOT run and NOT resolved";
  F-17 "FLAG-FOR-ALEX, OPEN ... neither run in this loop nor
  resolved"; both are also listed under verification.md's "Items
  reserved for Alex" and in README.md's status line.
- reviewer-notes.md Section 11.3 flags include F-1, F-5, F-7, and
  F-17 as explicit bullets (F-17 marked OPEN).

### Final sweep

- En/em dashes: codepoint count in brief-draft.md, substack-draft.md,
  social-drafts.md is 0 / 0 / 0 for both U+2014 and U+2013 (hyphen
  minus only). No silent-truncation marker anywhere in the package.
- No verdict words were introduced by the edits: grep of the shipped
  drafts for illegal / fraud / abuse / violation / guilty family
  terms returns nothing; the F-5 paragraph is explicitly
  no-conclusion.
- Every other new figure in the edited text ties to stats.json
  (rollup, cross-tab, TOT_UNITS=1 block, DIA 3, median basis,
  land-use zeros via the zero-neighborhood list) - with the single
  exception recorded as N-1.

### NEW ISSUE N-1 (minor, stats-coverage gap in an otherwise true claim)

Finding 2 (brief-draft.md and substack-draft.md, identical) prints:
"the other multi-license parcels sit on records of 125 to 579
units, except one 2-license parcel whose record is a vacant
common-element parcel with a TOT_UNITS of 0." No figure for the
125-to-579 range or for the TOT_UNITS=0 parcel exists in stats.json
(the tot_units_1_parcel block covers only the TOT_UNITS=1 parcel).
This reviewer recomputed the distribution independently from the
warehouse spine: the 12 multi-license parcels' TOT_UNITS are 0, 1,
125, 218, 232, 274, 282, 282, 292, 319, 372, 579, and the 0-unit
parcel is classed "VACANT LAND /GENERAL COMMON ELEMENTS" with 2
licenses - so the sentence is TRUE (and it corrects this review's
own original "the other 11 sit on records of 125 to 579 units",
which overlooked the 0-unit parcel). It is flagged only because the
package rule is that printed figures tie to stats.json; the fix is
to add the multi-parcel TOT_UNITS list to stats.json, not to change
the prose. F-4 itself is closed: the claim is supported by the data,
just not by the stats file.

### NEW ISSUE N-2 (minor, residual social phrasing)

X thread item 2 in social-drafts.md opens: "Concentration by holder
is effectively zero: the top 5 holders account for 8 of 2,083 active
licenses (0.38%), the top 25 for 28 (1.34%)." This is not one of the
three banned F-2 strings, the numbers follow in the same item, and
the thread's item 1 scopes the count to the register; but
"effectively zero" is an unscoped summary in the spirit of the
removed "no concentration to measure", and it carries no "by
licensee name as filed" qualifier. Alex may want it narrowed at QA
(e.g. "By holder, the register is flat: ..."). Recorded as a flag,
not a reopening of F-2, whose specified checks all pass.

### Re-verification verdict

F-1 CLOSED. F-2 CLOSED. F-3 CLOSED. F-4 CLOSED (with N-1). F-5
CLOSED. F-6 CLOSED. F-7 CLOSED. F-8 CLOSED. F-9 CLOSED. F-18
CLOSED. Dispositions complete; F-14 and F-17 remain OPEN for Alex
as recorded. Two new minor issues (N-1, N-2), neither blocking.
Nothing was published by this pass.
