from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
ledger = (ROOT / "FORENSIC_UPLIFT_LEDGER.md").read_text()
failures = []


def check(name, condition, detail):
    if condition:
        print(f"[PASS] {name}")
    else:
        print(f"[FAIL] {name}: {detail}")
        failures.append(f"{name}: {detail}")


categories = {
    "UIUX": 20,
    "GAME": 20,
    "BACK": 20,
    "QOL": 20,
    "FEAT": 20,
}

all_ids = []
for prefix, required in categories.items():
    ids = re.findall(rf"^\| ({prefix}-\d{{2}}) \|", ledger, re.MULTILINE)
    all_ids.extend(ids)
    check(f"{prefix} count", len(ids) == required, f"expected {required}, found {len(ids)}")
    check(f"{prefix} unique", len(set(ids)) == required, "duplicate or missing IDs")

wow_ids = re.findall(r"^\| (WOW-\d{2}) \|", ledger, re.MULTILINE)
check("WOW count", len(wow_ids) >= 1, "missing additional flagship")
check("WOW unique", len(wow_ids) == len(set(wow_ids)), "duplicate WOW IDs")
check("Cross-category ID uniqueness", len(all_ids) == len(set(all_ids)), "duplicate mandatory IDs")
check("No proposed-only ledger rows", "| PROPOSED |" not in ledger, "proposed item cannot satisfy count")
check("Count gate declaration present", "UI/UX: **20 / 20**" in ledger and "Features: **20 / 20**" in ledger,
      "count-gate summary is missing")

print()
if failures:
    print(f"UPLIFT LEDGER RESULT: FAIL ({len(failures)} failures)")
    for failure in failures:
        print(f" - {failure}")
    sys.exit(1)

print("UPLIFT LEDGER RESULT: PASS — 100 distinct categorized IDs + WOW")
sys.exit(0)
