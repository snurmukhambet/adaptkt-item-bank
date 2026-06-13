from __future__ import annotations
import json
import os
import time
from pathlib import Path

from .config import Config
from .generator import ExerciseGenerator
from .filters import ExerciseFilter


def load_taxonomy(path: str) -> dict:
    with open(path) as f:
        return json.load(f)


class Pipeline:
    def __init__(self, config: Config):
        self.config = config
        self.generator = ExerciseGenerator(config)
        self.filter = ExerciseFilter(config)
        self.taxonomy = load_taxonomy(config.taxonomy_path)
        Path(config.output_dir).mkdir(parents=True, exist_ok=True)

    # Per-skill run

    def run_skill(self, skill: dict, exercise_types: list[str]) -> dict:
        skill_id = skill["id"]
        out_path = Path(self.config.output_dir) / f"{skill_id}.json"

        if out_path.exists():
            print(f"  SKIP {skill_id} (already exists: {out_path})")
            with open(out_path) as f:
                return json.load(f)

        print(f"\n{'='*60}")
        print(f"Skill: {skill['name']} ({skill_id}) | GSE {skill['gse_min']}–{skill['gse_max']}")
        print(f"Exercise types: {exercise_types}")

        # Generate
        valid_exercises, raw_failed = self.generator.generate_skill_items(skill, exercise_types)
        valid_dicts = [ex.model_dump() for ex in valid_exercises]

        print(f"  Generated: {len(valid_exercises)} valid, {len(raw_failed)} schema-failed")

        # Filter
        passed, filter_failed = self.filter.filter_batch(valid_dicts, skill)
        print(f"  Filtered:  {len(passed)} passed, {len(filter_failed)} rejected")

        result = {
            "skill_id": skill_id,
            "skill_name": skill["name"],
            "exercises": passed,
            "rejected": filter_failed,
            "stats": {
                "generated": len(valid_exercises),
                "schema_failed": len(raw_failed),
                "filter_passed": len(passed),
                "filter_rejected": len(filter_failed),
            },
        }

        # Atomic write: write to .tmp then rename to avoid corrupted files on crash.
        tmp_path = out_path.with_suffix(out_path.suffix + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        tmp_path.replace(out_path)

        print(f"  Saved → {out_path}")
        return result

    # Full run

    def run_all(self):
        print(f"\nStarting full generation run")
        print(f"Grammar skills: {len(self.taxonomy['grammar_skills'])}")
        print(f"Vocabulary domains: {len(self.taxonomy['vocabulary_domains'])}")

        try:
            from tqdm import tqdm
            use_tqdm = True
        except ImportError:
            use_tqdm = False

        all_skills = [
            (s, ["cloze", "multiple_choice", "error_correction"])
            for s in self.taxonomy["grammar_skills"]
        ] + [
            (s, ["cloze", "multiple_choice", "word_formation"])
            for s in self.taxonomy["vocabulary_domains"]
        ]

        iterator = tqdm(all_skills, desc="Skills") if use_tqdm else all_skills
        all_exercises: list[dict] = []
        total_generated = 0
        total_rejected = 0
        per_skill_summary: list[dict] = []

        for skill, ex_types in iterator:
            result = self.run_skill(skill, ex_types)
            all_exercises.extend(result.get("exercises", []))
            stats = result.get("stats", {})
            total_generated += stats.get("generated", 0)
            total_rejected += stats.get("filter_rejected", 0)
            per_skill_summary.append({
                "skill_id": result.get("skill_id"),
                "skill_name": result.get("skill_name"),
                "generated": stats.get("generated", 0),
                "accepted": stats.get("filter_passed", 0),
                "rejected": stats.get("filter_rejected", 0),
            })

        # Merge with metadata
        from datetime import datetime, timezone
        merge_path = Path(self.config.output_dir) / "all_exercises.json"
        bundle = {
            "metadata": {
                "total_generated": total_generated,
                "total_accepted": len(all_exercises),
                "total_rejected": total_rejected,
                "total_cost_usd": round(self.generator.total_cost, 4),
                "generation_model": self.config.generation_model,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "per_skill": per_skill_summary,
            },
            "exercises": all_exercises,
        }
        tmp = merge_path.with_suffix(merge_path.suffix + ".tmp")
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(bundle, f, ensure_ascii=False, indent=2)
        tmp.replace(merge_path)

        print(f"\n{'='*60}")
        print(f"Done! Total exercises accepted: {len(all_exercises)} / {total_generated} generated")
        print(f"Total rejected (schema/distractor/dedup): {total_rejected}")
        print(f"Generation cost (Sonnet): ${self.generator.total_cost:.4f}")
        print(f"Saved merged file → {merge_path}")

    # Test run (2 skills, for cost estimation)

    def run_test(self, n_skills: int = 2):
        print(f"\nTEST MODE: running {n_skills} skills")
        test_skills = []

        # Pick present_perfect from grammar
        for s in self.taxonomy["grammar_skills"]:
            if s["id"] == "present_perfect":
                test_skills.append((s, ["cloze", "multiple_choice", "error_correction"]))
                break

        # Pick vocab_food_cooking or first available vocab domain
        for s in self.taxonomy["vocabulary_domains"]:
            if "food" in s["id"] or "cooking" in s["id"]:
                test_skills.append((s, ["cloze", "multiple_choice", "word_formation"]))
                break

        # Fallback if specific IDs not found
        if len(test_skills) == 0:
            test_skills.append(
                (self.taxonomy["grammar_skills"][0], ["cloze", "multiple_choice", "error_correction"])
            )
        if len(test_skills) == 1:
            test_skills.append(
                (self.taxonomy["vocabulary_domains"][0], ["cloze", "multiple_choice", "word_formation"])
            )

        test_skills = test_skills[:n_skills]

        total_passed = 0
        total_generated = 0
        all_results = []

        for skill, ex_types in test_skills:
            # Temporarily lower counts for test run
            orig = {
                "grammar_cloze": self.config.grammar_cloze,
                "grammar_mc": self.config.grammar_mc,
                "grammar_error_correction": self.config.grammar_error_correction,
                "vocab_cloze": self.config.vocab_cloze,
                "vocab_mc": self.config.vocab_mc,
                "vocab_word_formation": self.config.vocab_word_formation,
                "items_per_batch": self.config.items_per_batch,
            }
            try:
                self.config.grammar_cloze = 5
                self.config.grammar_mc = 5
                self.config.grammar_error_correction = 3
                self.config.vocab_cloze = 5
                self.config.vocab_mc = 5
                self.config.vocab_word_formation = 3
                self.config.items_per_batch = 5

                result = self.run_skill(skill, ex_types)
                all_results.append(result)
                total_passed += result["stats"]["filter_passed"]
                total_generated += result["stats"]["generated"]
            finally:
                for k, v in orig.items():
                    setattr(self.config, k, v)

        gen_cost = self.generator.total_cost
        print(f"\n{'='*60}")
        print(f"TEST RUN COMPLETE")
        print(f"  Skills tested: {len(test_skills)}")
        print(f"  Items generated: {total_generated}")
        print(f"  Items passed filters: {total_passed}")
        print(f"  Generation cost (Sonnet): ${gen_cost:.4f}")
        print(f"\nSample items (first 2 from each skill):")
        for result in all_results:
            print(f"\n--- {result['skill_name']} ---")
            for ex in result["exercises"][:2]:
                content = ex.get("content", {})
                print(f"  [{ex.get('exercise_type')} GSE={ex.get('gse_target')}]")
                print(f"  Prompt: {content.get('prompt', '')[:80]}")
                print(f"  Answer: {content.get('correct_answer', '')}")
                distractors = content.get("distractors")
                if distractors:
                    print(f"  Distractors: {distractors}")

        return all_results

    # Stats

    def stats(self):
        output_dir = Path(self.config.output_dir)
        if not output_dir.exists():
            print(f"Output directory {output_dir} does not exist.")
            return

        skill_files = list(output_dir.glob("*.json"))
        skill_files = [f for f in skill_files if f.name != "all_exercises.json"]

        total_exercises = 0
        total_rejected = 0
        by_type: dict[str, int] = {}
        by_cefr: dict[str, int] = {}

        for path in skill_files:
            with open(path) as f:
                data = json.load(f)
            exercises = data.get("exercises", [])
            total_exercises += len(exercises)
            total_rejected += len(data.get("rejected", []))
            for ex in exercises:
                t = ex.get("exercise_type", "unknown")
                by_type[t] = by_type.get(t, 0) + 1
                c = ex.get("cefr_level", "unknown")
                by_cefr[c] = by_cefr.get(c, 0) + 1

        print(f"\n{'='*60}")
        print(f"STATS — {len(skill_files)} skill files")
        print(f"  Total exercises (passed): {total_exercises}")
        print(f"  Total rejected: {total_rejected}")
        pass_rate = total_exercises / (total_exercises + total_rejected) * 100 if (total_exercises + total_rejected) else 0
        print(f"  Pass rate: {pass_rate:.1f}%")
        print(f"\nBy type:")
        for t, n in sorted(by_type.items()):
            print(f"  {t}: {n}")
        print(f"\nBy CEFR:")
        for c, n in sorted(by_cefr.items()):
            print(f"  {c}: {n}")
