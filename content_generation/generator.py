from __future__ import annotations
import json
import time
import re
from datetime import datetime, timezone

import anthropic

from .config import Config
from .schemas import Exercise, Provenance, AutoChecks
from .prompts import (
    SYSTEM_PROMPT,
    build_grammar_cloze_prompt,
    build_grammar_mc_prompt,
    build_grammar_error_correction_prompt,
    build_vocab_cloze_prompt,
    build_vocab_mc_prompt,
    build_vocab_word_formation_prompt,
)
from .skill_descriptions import get_description


_GRAMMAR_TEMPLATE_IDS = {
    "cloze": "grammar_cloze_v1",
    "multiple_choice": "grammar_mc_v1",
    "error_correction": "grammar_error_correction_v1",
}
_VOCAB_TEMPLATE_IDS = {
    "cloze": "vocab_cloze_v1",
    "multiple_choice": "vocab_mc_v1",
    "word_formation": "vocab_word_formation_v1",
}


def _compute_cost(usage, config: Config) -> float:
    input_cost = usage.input_tokens * config.sonnet_input_price / 1_000_000
    output_cost = usage.output_tokens * config.sonnet_output_price / 1_000_000
    cache_write = getattr(usage, "cache_creation_input_tokens", 0) * config.sonnet_cache_write_price / 1_000_000
    cache_read = getattr(usage, "cache_read_input_tokens", 0) * config.sonnet_cache_read_price / 1_000_000
    return input_cost + output_cost + cache_write + cache_read


def _extract_json(text: str) -> list[dict]:
    """Parse JSON array from model output, stripping any accidental markdown."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    parsed = json.loads(text)
    if not isinstance(parsed, list):
        # Sometimes the model wraps the array in {"items": [...]} or similar.
        if isinstance(parsed, dict):
            for v in parsed.values():
                if isinstance(v, list):
                    return v
        raise ValueError(f"Expected JSON array, got {type(parsed).__name__}")
    return parsed


class ExerciseGenerator:
    def __init__(self, config: Config):
        self.client = anthropic.Anthropic(api_key=config.api_key)
        self.config = config
        self.total_cost: float = 0.0

    def generate_batch(
        self,
        system_prompt: str,
        user_prompt: str,
        batch_id: str,
    ) -> list[dict]:
        model = self.config.generation_model
        last_exc: Exception | None = None

        for attempt in range(1, self.config.max_retries + 1):
            try:
                response = self.client.messages.create(
                    model=model,
                    max_tokens=4096,
                    temperature=self.config.temperature,
                    system=[
                        {
                            "type": "text",
                            "text": system_prompt,
                            "cache_control": {"type": "ephemeral"},
                        }
                    ],
                    messages=[{"role": "user", "content": user_prompt}],
                )

                raw = response.content[0].text
                items = _extract_json(raw)

                usage = response.usage
                cached = getattr(usage, "cache_read_input_tokens", 0)
                cost = _compute_cost(usage, self.config)
                self.total_cost += cost

                print(
                    f"  [{batch_id}] attempt {attempt}: {len(items)} items | "
                    f"in={usage.input_tokens} (cached={cached}) "
                    f"out={usage.output_tokens} | ${cost:.4f}"
                )
                return items

            except (json.JSONDecodeError, ValueError) as exc:
                last_exc = exc
                print(f"  [{batch_id}] attempt {attempt} JSON parse error: {exc}. Retrying...")
                time.sleep(self.config.delay_between_calls * attempt)
            except anthropic.APIError as exc:
                last_exc = exc
                print(f"  [{batch_id}] attempt {attempt} API error: {exc}. Retrying...")
                time.sleep(self.config.delay_between_calls * attempt * 2)

        raise RuntimeError(f"Failed after {self.config.max_retries} attempts for {batch_id}") from last_exc

    def _build_prompts(self, skill: dict, exercise_type: str) -> tuple[str, str]:
        is_grammar = skill["category"] == "grammar"
        desc = get_description(skill["id"]) if is_grammar else None

        if exercise_type == "cloze":
            if is_grammar:
                return build_grammar_cloze_prompt(skill, desc, self.config.items_per_batch)
            else:
                return build_vocab_cloze_prompt(skill, self.config.items_per_batch)
        elif exercise_type == "multiple_choice":
            if is_grammar:
                return build_grammar_mc_prompt(skill, desc, self.config.items_per_batch)
            else:
                return build_vocab_mc_prompt(skill, self.config.items_per_batch)
        elif exercise_type == "error_correction":
            return build_grammar_error_correction_prompt(skill, desc, self.config.items_per_batch)
        elif exercise_type == "word_formation":
            return build_vocab_word_formation_prompt(skill, self.config.items_per_batch)
        else:
            raise ValueError(f"Unknown exercise_type: {exercise_type}")

    def generate_skill_items(
        self,
        skill: dict,
        exercise_types: list[str],
    ) -> tuple[list[Exercise], list[dict]]:
        """Generate all exercise types for one skill. Returns (valid, raw_failed)."""
        valid: list[Exercise] = []
        raw_failed: list[dict] = []
        timestamp = datetime.now(timezone.utc).isoformat()

        is_grammar = skill["category"] == "grammar"
        for ex_type in exercise_types:
            target_count = self._target_count(ex_type, is_grammar)
            collected_raw: list[dict] = []

            batches_needed = -(-target_count // self.config.items_per_batch)  # ceiling div
            system_prompt, user_prompt = self._build_prompts(skill, ex_type)

            # Allow up to batches_needed + 1 attempts to fill target (one refill on shortfall)
            max_batches = batches_needed + 1
            batch_num = 0
            while len(collected_raw) < target_count and batch_num < max_batches:
                batch_num += 1
                remaining = target_count - len(collected_raw)
                if remaining <= 0:
                    break

                batch_size = min(self.config.items_per_batch, remaining)
                batch_id = f"{skill['id']}/{ex_type}/batch_{batch_num}"

                # Adjust user prompt for smaller final batch
                effective_prompt = user_prompt
                if batch_size < self.config.items_per_batch:
                    effective_prompt = user_prompt.replace(
                        f"exactly {self.config.items_per_batch} items",
                        f"exactly {batch_size} items",
                    ).replace(
                        f"Generate {self.config.items_per_batch}",
                        f"Generate {batch_size}",
                    )

                try:
                    raw_items = self.generate_batch(system_prompt, effective_prompt, batch_id)
                    collected_raw.extend(raw_items)
                except RuntimeError as exc:
                    print(f"  SKIPPING batch {batch_id}: {exc}")

                time.sleep(self.config.delay_between_calls)

            # Enrich and validate
            template_map = _GRAMMAR_TEMPLATE_IDS if is_grammar else _VOCAB_TEMPLATE_IDS
            for i, raw in enumerate(collected_raw):
                raw["id"] = f"ex_{skill['id']}_{ex_type}_{i:04d}"
                raw.setdefault("provenance", {})
                raw["provenance"].update(
                    {
                        "generator_model": self.config.generation_model,
                        "generation_timestamp": timestamp,
                        "template_id": template_map.get(ex_type, ex_type),
                        "batch_id": f"{skill['id']}_{ex_type}",
                        "auto_checks": {
                            "schema_valid": True,
                            "skill_match": None,
                            "ambiguity_check": None,
                            "duplicate_check": None,
                        },
                    }
                )
                raw.setdefault("difficulty_features", {"gse_target": raw.get("gse_target", skill["gse_mean"])})
                if "gse_target" not in raw.get("difficulty_features", {}):
                    raw["difficulty_features"]["gse_target"] = raw.get("gse_target", round(skill["gse_mean"]))

                try:
                    exercise = Exercise.model_validate(raw)
                    valid.append(exercise)
                except Exception as exc:
                    raw["_validation_error"] = str(exc)
                    raw_failed.append(raw)

        return valid, raw_failed

    def _target_count(self, exercise_type: str, is_grammar: bool = True) -> int:
        if is_grammar:
            mapping = {
                "cloze": self.config.grammar_cloze,
                "multiple_choice": self.config.grammar_mc,
                "error_correction": self.config.grammar_error_correction,
            }
        else:
            mapping = {
                "cloze": self.config.vocab_cloze,
                "multiple_choice": self.config.vocab_mc,
                "word_formation": self.config.vocab_word_formation,
            }
        return mapping.get(exercise_type, self.config.items_per_batch)
