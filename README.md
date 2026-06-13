# adaptkt-item-bank

A synthetic item bank of English-language exercises for an adaptive learning /
Knowledge Tracing (KT) prototype, together with the LLM-based pipeline that
produced it. Each exercise is tied to a single knowledge component (skill),
carries a numeric difficulty target on the Pearson Global Scale of English (GSE),
and — for selected-response types — includes distractors with a per-distractor
diagnostic rationale.

The bank covers 87 skills (60 grammar skills and 27 vocabulary domains) in the
CEFR A1–B2 range (GSE 25–59) and contains four exercise types: cloze,
multiple choice, error correction, and word formation. Generation is fully
LLM-based; no corpora, dictionaries, or rule engines are used. A single system
prompt (an expert CEFR item-writer persona) is combined with a per-skill user
prompt that injects the skill's GSE band, linguistic description, key structures,
and a catalogue of common learner errors. The model returns a JSON array of
exercise objects, which are validated against a Pydantic schema and passed
through a structural filter (schema validity, distractor collision, exact-prompt
deduplication).

## Context

This repository is part of the Master's thesis *"Analysis of artificial intelligence methods for adaptive foreign language learning based on analyzing learner's progress"* (Astana IT University, 2026). It is one of
four open-source repositories released with the thesis (see
[Related repositories](#related-repositories)). The item bank is the content
foundation on which the Knowledge Tracing experiments are run.

## Installation

Requires Python 3.13.

```
pip install -r requirements.txt
```

Generation calls the Anthropic API and requires a key in the environment:

```
export ANTHROPIC_API_KEY=your-key-here
```

The key is read directly from `ANTHROPIC_API_KEY` (see `content_generation/config.py`);
no `.env` file is loaded. A key is needed only for regeneration — inspecting or
using the already-generated bank in `generated_items/` requires no key.

## Usage

The generation pipeline is driven by `run.py`:

```
python run.py test                      # 2 skills only, smoke test (~$0.30)
python run.py generate                  # full run, all 87 skills
python run.py generate --skip-filters   # skip the structural filter
python run.py stats                     # summary stats over generated_items/
```

Output is written to `generated_items/`, one JSON file per skill, plus a merged
bundle `all_exercises.json`. Per-skill files already present are skipped, so an
interrupted run resumes where it stopped.

The bank is produced in two stages:

1. **Generate + filter.** `python run.py generate` produces 2,757 accepted items
   (`generated_items/all_exercises.json`), out of 2,790 generated; 33 are
   rejected as exact-duplicate prompts within a skill.
2. **Cross-skill deduplication.** `dedupe_item_bank.py` removes prompts that
   collide across different skills, yielding 2,752 canonical items
   (`generated_items/all_exercises_dedup.json`). This is the canonical set
   consumed by the other repositories.

```
python dedupe_item_bank.py \
    --input generated_items/all_exercises.json \
    --output generated_items/all_exercises_dedup.json
```

## Repository structure

```
run.py                          Entry point (test / generate / stats)
dedupe_item_bank.py             Stage-2 cross-skill deduplication
taxonomy_v2.json                Skill taxonomy: 60 grammar skills, 27 vocab domains,
                                GSE bands, prerequisite edges
requirements.txt
content_generation/
    config.py                   Model, item counts, pricing, rate limiting
    prompts.py                  System prompt and per-type user-prompt builders
    skill_descriptions.py       Per-skill linguistic descriptions and learner errors
    generator.py                Anthropic API calls, retries, JSON extraction, costing
    filters.py                  Schema / distractor-collision / dedup checks
    schemas.py                  Pydantic models for the exercise schema
    pipeline.py                 Orchestration and per-skill / full-run / stats logic
generated_items/                Generated item bank (one JSON per skill)
    all_exercises.json          Merged bank, 2,757 accepted items
    all_exercises_dedup.json    Canonical bank, 2,752 items after cross-skill dedup
    <skill_id>.json             Per-skill files (accepted items plus rejected ones)
    sample_for_llm.json         Small sample of the schema and item types
```

## Data

The generated item bank is included in this repository under `generated_items/`.
The per-skill files retain their `rejected` arrays (items removed by the filter,
with rejection reasons) for transparency. The canonical set used downstream is
`generated_items/all_exercises_dedup.json` (2,752 items).

Regeneration is **not deterministic**: there is no random seed and the sampling
temperature is 0.7, so `python run.py generate` produces a different bank on each
run. The reported reference run used `claude-sonnet-4-6`, cost approximately
USD 11.94, and took about 2 h 47 min for all 87 skills.

The GSE difficulty values and descriptor IDs in `taxonomy_v2.json` are drawn from
the publicly available Pearson GSE Teacher Toolkit. The prerequisite graph is
based on the English Grammar Profile and the *Cambridge Grammar in Use* ordering.

## Related repositories

Part of the four-repository release accompanying the thesis. Replace the
placeholder slugs below with the published repository names.

- [adaptkt-item-bank](https://github.com/snurmukhambet/adaptkt-item-bank) — this repository
- [adaptkt-simulator](https://github.com/snurmukhambet/adaptkt-simulator)
- [adaptkt-kt-benchmark](https://github.com/snurmukhambet/adaptkt-kt-benchmark)
- [adaptkt-demo](https://github.com/snurmukhambet/adaptkt-demo)

## License

Released under the MIT License. See [LICENSE](LICENSE).
