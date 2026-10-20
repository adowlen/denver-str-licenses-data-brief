"""Warehouse deposit for the Denver STR licenses brief (2026-10-19).

Standing deposit rule (2026-10-16): every study lands in the stack.
- Raw snapshot + pull log were archived by code/pull_data.py at
  stack/denver/snapshots/2026-10-19/str_licenses.parquet and
  pull_log_str_2026-10-19.json.
- This script registers the new snapshot in stack/denver/manifest.json
  (the superseded 2026-10-15 snapshot record moves to snapshot_history,
  the refresh convention in stack/README.md) and appends the study
  deposit entry to stack/denver/verification.md.
- The cleaned layer (layers/str_licenses_clean.parquet) is NOT rebuilt
  here: it remains derived from the 2026-10-15 snapshot until the next
  stack refresh cycle rebuilds it. The brief bridges the fresh snapshot
  to parcels by LICENSE_NUM against that layer (see build_stats.py).
Idempotent: re-running changes nothing twice.
"""
import hashlib
import json
import os

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
SNAP = f"{STACK}/snapshots/2026-10-19/str_licenses.parquet"
PULL_LOG = f"{STACK}/snapshots/2026-10-19/pull_log_str_2026-10-19.json"

log = json.load(open(PULL_LOG))
assert log["rows"] == 2338 and os.path.exists(SNAP)

manifest_path = f"{STACK}/manifest.json"
manifest = json.load(open(manifest_path))
entry = next(e for e in manifest["layers"] if e["name"] == "denver_str_licenses")
if entry.get("snapshot_date") != "2026-10-19":
    entry.setdefault("snapshot_history", []).append({
        "snapshot_date": entry.get("snapshot_date"),
        "row_count": entry.get("row_count"),
        "service_last_edit_utc": entry.get("service_last_edit_utc"),
        "files": entry.get("files"),
    })
    h = hashlib.sha256()
    with open(SNAP, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    assert h.hexdigest() == log["sha256"]
    cleaned = next(f for f in entry["files"] if "layers/" in f["path"])
    entry["files"] = [
        {"path": "snapshots/2026-10-19/str_licenses.parquet",
         "role": "raw snapshot (immutable), attribute table - the service is a table with no geometry",
         "size_bytes": log["size_bytes"], "sha256": log["sha256"]},
        {"path": "snapshots/2026-10-15/str_licenses.parquet",
         "role": "prior raw snapshot (immutable), superseded 2026-10-19; retained in snapshot_history",
         "size_bytes": 122428,
         "sha256": "b7dd487c0a5bf1bf389e05480e286e1a73a1345204d70285a5bae6060bddc599"},
        cleaned,
    ]
    entry["snapshot_date"] = "2026-10-19"
    entry["row_count"] = 2338
    entry["service_last_edit_utc"] = log["service_last_edit_utc"]
    entry["notes"] = entry["notes"] + (
        " REFRESH 2026-10-19 (STR licenses brief): fresh snapshot 2,338 rows "
        "(Active 2,083; Delinquent 137; Closed - Expired 116; About to Expire 1; "
        "Closed - Surrendered 1); drift vs 2026-10-15: rows -11, active -15 "
        "(12 license numbers left, 1 entered, 7 Active -> Delinquent, 2 Delinquent -> Active). "
        "The cleaned layer still derives from the 2026-10-15 snapshot; the brief bridges the "
        "fresh snapshot by LICENSE_NUM (match 2,335/2,338 = 99.87%). Rebuild the cleaned layer "
        "at the next refresh cycle."
    )
    manifest["last_updated"] = "2026-10-19"
    with open(manifest_path, "w") as fh:
        json.dump(manifest, fh, indent=1)
    print("manifest updated: denver_str_licenses snapshot_date 2026-10-19")
else:
    print("manifest already at 2026-10-19; no change")

verif_path = f"{STACK}/verification.md"
verif = open(verif_path).read()
marker = "## Study deposit - Denver STR licenses brief (2026-10-19)"
if marker not in verif:
    block = """

## Study deposit - Denver STR licenses brief (2026-10-19)

Deposited under the standing warehouse deposit rule (2026-10-16) by the
denver-str-licenses-brief-2026-10-19 package build.

ARCHIVED SNAPSHOT: snapshots/2026-10-19/str_licenses.parquet - fresh full-service pull of
ODC_short_term_rental_licenses_active_or_pending_renewal (layer 54), 2,338 rows, pulled
2026-10-19T11:27:59Z, service last edit 2026-10-19T09:44:04Z; pull log + sha256 at
snapshots/2026-10-19/pull_log_str_2026-10-19.json. Supersedes snapshots/2026-10-15/
str_licenses.parquet (2,349 rows) as the current register snapshot; the 2026-10-15 file is
retained unchanged and recorded in the manifest entry's snapshot_history.

DRIFT (2026-10-15 -> 2026-10-19, by LICENSE_NUM): rows -11 (12 license numbers left,
1 entered); Active 2,098 -> 2,083 (net -15: 11 active left the register, 7 Active ->
Delinquent, 2 Delinquent -> Active, 1 entered as Active); Delinquent 133 -> 137;
Closed - Expired unchanged at 116 (one Delinquent -> Closed - Expired offset by one
Closed - Expired leaving). No ENTITY_NAME or PARCEL_NUM changed on any continuing license.

CLEANED LAYER: layers/str_licenses_clean.parquet is unchanged and still derives from the
2026-10-15 snapshot. The brief bridges the fresh snapshot to parcels by LICENSE_NUM
against that layer plus one key match for the entered license (fresh match outcome:
key 2,321 + key-fresh 1 + address_strict 13 + unmatched 3 = 99.87% matched, the same rate
as the Phase 3 bridge). Rebuild the cleaned layer from the 2026-10-19 snapshot at the
next refresh cycle.

VERIFICATION STATUS: Section 10 pre-flight audit passed (all assertions, including the
parcel-bridge control: recomputed licenses-per-parcel from the raw 2026-10-15 snapshot
reproduces the cleaned layer on all 2,265 parcels, 0 mismatches). Record in the package
verification.md (hidden_files/denver-str-licenses-brief-2026-10-19/verification.md).
manifest.json: denver_str_licenses entry updated in place (layer count unchanged).
"""
    with open(verif_path, "a") as fh:
        fh.write(block)
    print("verification.md deposit entry appended")
else:
    print("verification.md already carries the deposit entry; no change")
