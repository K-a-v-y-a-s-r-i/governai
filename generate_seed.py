"""Ask local models every prompt in test_prompts.json and save their REAL answers
to seed_data.json, ready for seed.py. Fully offline.

Usage:
    python generate_seed.py --models "Llama 3.1 8B" "Mistral 7B"
    python generate_seed.py --models "Llama 3.1 8B" --per-category 5   (faster)

Pasted answers from other models (e.g. Claude Opus 5.5) already in seed_data.json are kept.
"""
import argparse
import json
from pathlib import Path

from generate import LOCAL_MODELS, ask_model

parser = argparse.ArgumentParser()
parser.add_argument("--models", nargs="+", required=True, choices=list(LOCAL_MODELS))
parser.add_argument("--per-category", type=int, default=10)
parser.add_argument("--out", default="seed_data.json")
args = parser.parse_args()

prompts = json.loads(Path("test_prompts.json").read_text(encoding="utf-8"))
out = Path(args.out)
existing = json.loads(out.read_text(encoding="utf-8")) if out.exists() else []
# Drop the placeholder example rows
existing = [r for r in existing if r.get("model") != "Example Model"]
done = {(r["model"], r["prompt"]) for r in existing}

jobs = [(m, p) for m in args.models
        for cat, plist in prompts.items() if not cat.startswith("_")
        for p in plist[: args.per_category]
        if (m, p) not in done]
print(f"Generating {len(jobs)} answers...")

for i, (model, prompt) in enumerate(jobs, 1):
    try:
        answer = ask_model(model, prompt)
    except Exception as e:
        print(f"[{i}/{len(jobs)}] {model}: error ({e}), skipped")
        continue
    existing.append({"model": model, "prompt": prompt, "response": answer})
    out.write_text(json.dumps(existing, indent=2, ensure_ascii=False), encoding="utf-8")  # save as we go
    print(f"[{i}/{len(jobs)}] {model}: done")

print(f"Saved to {out}. Next: python seed.py")
