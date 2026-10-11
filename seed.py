"""Bulk-load real pasted responses from seed_data.json into GovernAI.

Usage:  python seed.py              (judges every entry that has a response)
        python seed.py --delay 6    (seconds between calls, for free-tier limits)
"""
import argparse
import json
import time
from pathlib import Path

from db import save
from judge import judge

parser = argparse.ArgumentParser()
parser.add_argument("--file", default="seed_data.json")
parser.add_argument("--delay", type=float, default=0.0,
                    help="extra seconds between calls (judge.py already paces itself)")
args = parser.parse_args()

rows = json.loads(Path(args.file).read_text(encoding="utf-8"))
rows = [r for r in rows if str(r.get("response", "")).strip()]
print(f"Judging {len(rows)} pairs...")

ok = failed_calls = 0
for i, r in enumerate(rows, 1):
    for attempt in range(3):
        try:
            j = judge(r["prompt"], r["response"])
            save(r["model"], r["prompt"], r["response"], j)
            ok += 1
            print(f'[{i}/{len(rows)}] {r["model"]}: {"PASS" if j["pass"] else "FAIL"} {j["category"]}')
            break
        except Exception as e:
            wait = max(args.delay, 10) * (attempt + 1)
            print(f"  retry in {wait:.0f}s ({e})")
            time.sleep(wait)
    else:
        failed_calls += 1
    time.sleep(args.delay)

print(f"Done: {ok} saved, {failed_calls} skipped after retries.")
