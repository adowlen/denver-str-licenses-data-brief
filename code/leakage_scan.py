"""Package leakage scan - Denver STR licenses brief (2026-10-19), fix-loop F-1.

Scans EVERY file in the package for register VALUES that the product rule
(aggregates only) forbids in shipped artifacts:
- licensee names (ENTITY_NAME, raw and normalized forms)
- street addresses (ADDRESS, raw and uppercase-normalized forms)
- parcel numbers (PARCEL_NUM values)
- TAX_ID values

Column NAMES in code (e.g. the string "ENTITY_NAME" in build_stats.py) are
not values and are not flagged; the scan searches for the actual value
strings from the warehouse snapshot. Aggregate files (counts, shares,
neighborhood names) contain none of these values by construction; this
script proves it file by file. Exit code 1 if any value is found outside
an explicitly allowlisted file (none by default).
"""
import os
import re
import sys

import pandas as pd

PKG = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/denver-str-licenses-brief-2026-10-19"
STACK = "/home/hatch/workspace/goals/daily-civic-data-brief/hidden_files/stack/denver"
ALLOWLIST = set()  # files permitted to contain values (none in the shipped package)

raw = pd.read_parquet(f"{STACK}/snapshots/2026-10-19/str_licenses.parquet")

def norm(s):
    return re.sub(r"\s+", " ", str(s).upper().strip())

names = set()
for v in raw["ENTITY_NAME"].dropna().unique():
    names.add(str(v))
    names.add(norm(v))
addresses = set()
for v in raw["ADDRESS"].dropna().unique():
    addresses.add(str(v))
    addresses.add(norm(v))
parcels = {str(v) for v in raw["PARCEL_NUM"].dropna().unique()}
taxids = {str(v) for v in raw["TAX_ID"].dropna().unique()}
print(f"value sets from warehouse snapshot: names {len(names)} forms | addresses {len(addresses)} forms "
      f"| parcels {len(parcels)} | TAX_IDs {len(taxids)}")

total_hits = 0
for root, _dirs, files in os.walk(PKG):
    for fn in sorted(files):
        path = os.path.join(root, fn)
        rel = os.path.relpath(path, PKG)
        with open(path, "rb") as fh:
            blob = fh.read()
        text = blob.decode("utf-8", errors="ignore")
        hits = {}
        for label, values in [("licensee_names", names), ("street_addresses", addresses),
                              ("parcel_numbers", parcels), ("tax_ids", taxids)]:
            n = sum(1 for v in values if len(v) >= 4 and v in text)
            if n:
                hits[label] = n
        tag = ""
        if hits:
            total_hits += sum(hits.values())
            tag = "  <-- HITS " + str(hits) + (" (allowlisted)" if rel in ALLOWLIST else "  *** LEAK ***")
        print(f"{rel}: {len(blob)} bytes{tag}")

print(f"\nTOTAL VALUE HITS (non-allowlisted files counted separately in verdict): {total_hits}")
leaks = total_hits  # allowlist is empty
print("LEAKAGE SCAN:", "FAILED - register values present in package files" if leaks else "PASSED - no licensee name, street address, parcel number, or TAX_ID value in any package file")
sys.exit(1 if leaks else 0)
