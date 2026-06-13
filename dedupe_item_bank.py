"""One-shot dedupe of the exercise bank.

Reads `all_exercises_clean.json`, finds duplicates by normalized prompt,
keeps the first occurrence of each prompt, writes `all_exercises_dedup.json`,
and prints a breakdown (intra-skill vs cross-skill collisions) so we can
judge whether the dedupe is meaningful.

Run from project root:
    python3 dedupe_item_bank.py
"""

from __future__ import annotations

import argparse
import json
import re
import string
import sys
from collections import Counter, defaultdict
from pathlib import Path


_PUNCT_RE = re.compile(f"[{re.escape(string.punctuation)}]")
_WS_RE = re.compile(r"\s+")


def normalize_prompt(prompt: str) -> str:
    """Lowercase, strip punctuation, collapse whitespace.

    Matching is intentionally aggressive: we want to catch prompts that
    differ only in capitalization, trailing periods, or extra spaces.
    """
    if not prompt:
        return ""
    s = prompt.lower()
    s = _PUNCT_RE.sub(" ", s)
    s = _WS_RE.sub(" ", s).strip()
    return s


def dedupe(items: list[dict]) -> tuple[list[dict], dict]:
    """Return (kept_items, report)."""
    seen_first: dict[str, dict] = {}  # norm_prompt -> first item
    duplicates: list[tuple[dict, dict]] = []  # (dup_item, original_item)
    empty_prompts = 0

    for item in items:
        norm = normalize_prompt(item.get("prompt", ""))
        if not norm:
            empty_prompts += 1
            # Keep items without prompts as-is (don't dedupe what we can't compare)
            continue
        if norm in seen_first:
            duplicates.append((item, seen_first[norm]))
        else:
            seen_first[norm] = item

    # Build kept list preserving original order
    dup_ids = {id(d) for d, _ in duplicates}
    kept = [it for it in items if id(it) not in dup_ids]

    intra_skill = sum(1 for d, o in duplicates if d.get("skill_id") == o.get("skill_id"))
    cross_skill = len(duplicates) - intra_skill

    skills_affected = Counter()
    cross_skill_pairs = Counter()
    for dup, orig in duplicates:
        skills_affected[dup.get("skill_id", "?")] += 1
        if dup.get("skill_id") != orig.get("skill_id"):
            pair = tuple(sorted([dup.get("skill_id", "?"), orig.get("skill_id", "?")]))
            cross_skill_pairs[pair] += 1

    report = {
        "input_total": len(items),
        "empty_prompts": empty_prompts,
        "duplicates_removed": len(duplicates),
        "kept": len(kept),
        "intra_skill_duplicates": intra_skill,
        "cross_skill_duplicates": cross_skill,
        "top_affected_skills": skills_affected.most_common(10),
        "top_cross_skill_pairs": cross_skill_pairs.most_common(10),
        "sample_duplicates": [
            {
                "kept_id": orig["id"],
                "kept_skill": orig.get("skill_id"),
                "removed_id": dup["id"],
                "removed_skill": dup.get("skill_id"),
                "prompt": dup.get("prompt", "")[:120],
            }
            for dup, orig in duplicates[:5]
        ],
    }
    return kept, report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="all_exercises_clean.json")
    parser.add_argument("--output", default="all_exercises_dedup.json")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    if not in_path.exists():
        print(f"ERROR: input not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    with in_path.open(encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "exercises" in data:
        items = data["exercises"]
        wrap = lambda kept: {**data, "total": len(kept), "exercises": kept}
    else:
        items = data
        wrap = lambda kept: kept

    kept, report = dedupe(items)

    with out_path.open("w", encoding="utf-8") as f:
        json.dump(wrap(kept), f, ensure_ascii=False, indent=2)

    print("=== Item bank dedupe report ===")
    print(f"Input file:           {in_path}")
    print(f"Output file:          {out_path}")
    print(f"Input items:          {report['input_total']:,}")
    print(f"Empty prompts (kept): {report['empty_prompts']}")
    print(f"Duplicates removed:   {report['duplicates_removed']:,}")
    print(f"Kept:                 {report['kept']:,}")
    print(f"  intra-skill dupes:  {report['intra_skill_duplicates']:,}")
    print(f"  cross-skill dupes:  {report['cross_skill_duplicates']:,}")
    if report["top_affected_skills"]:
        print("\nTop 10 affected skills (duplicates removed):")
        for skill, n in report["top_affected_skills"]:
            print(f"  {skill:<30} {n:>5}")
    if report["top_cross_skill_pairs"]:
        print("\nTop 10 cross-skill collision pairs:")
        for (a, b), n in report["top_cross_skill_pairs"]:
            print(f"  {a:<25} <-> {b:<25} {n:>5}")
    if report["sample_duplicates"]:
        print("\nSample duplicates (kept_id <- removed_id):")
        for d in report["sample_duplicates"]:
            cross = " [CROSS-SKILL]" if d["kept_skill"] != d["removed_skill"] else ""
            print(f"  {d['kept_id']} ({d['kept_skill']}){cross}")
            print(f"    <- {d['removed_id']} ({d['removed_skill']})")
            print(f"    prompt: {d['prompt']!r}")


if __name__ == "__main__":
    main()
