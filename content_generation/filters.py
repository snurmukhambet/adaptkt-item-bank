from __future__ import annotations

from .config import Config
from .schemas import Exercise


class ExerciseFilter:
    """Lightweight filter: schema validation, distractor collision, exact-prompt dedup. No LLM calls."""

    def __init__(self, config: Config):
        self.config = config
        self._seen_prompts: set[str] = set()

    def reset_dedup(self) -> None:
        """Clear dedup state — call between skills so cross-skill prompts don't collide."""
        self._seen_prompts = set()

    def check_schema(self, item: dict) -> tuple[bool, str]:
        try:
            Exercise.model_validate(item)
            return True, "ok"
        except Exception as exc:
            return False, str(exc)

    def check_distractor_collision(self, item: dict) -> tuple[bool, str]:
        content = item.get("content", {})
        correct = (content.get("correct_answer") or "").strip().lower()
        distractors = content.get("distractors") or []
        for d in distractors:
            if d.strip().lower() == correct:
                return False, f"distractor '{d}' == correct_answer '{correct}'"
        return True, "ok"

    def check_duplicate(self, item: dict) -> tuple[bool, str]:
        prompt_text = (item.get("content", {}).get("prompt") or "").strip().lower()
        if not prompt_text:
            return True, "no prompt text"
        if prompt_text in self._seen_prompts:
            return False, "exact duplicate of a prior item"
        self._seen_prompts.add(prompt_text)
        return True, "ok"

    def filter_batch(
        self, items: list[dict], skill: dict
    ) -> tuple[list[dict], list[dict]]:
        # Reset dedup per skill — items across different skills are independent.
        self.reset_dedup()

        passed: list[dict] = []
        failed: list[dict] = []

        def _reject(item: dict, checks: dict, failed_check: str, reason: str) -> None:
            item["_filter_checks"] = checks
            item["rejection_reason"] = f"{failed_check}: {reason}"
            failed.append(item)

        for item in items:
            checks: dict = {}

            ok, reason = self.check_schema(item)
            checks["schema"] = (ok, reason)
            if not ok:
                _reject(item, checks, "schema", reason)
                continue

            ok, reason = self.check_distractor_collision(item)
            checks["distractor_collision"] = (ok, reason)
            if not ok:
                _reject(item, checks, "distractor_collision", reason)
                continue

            ok, reason = self.check_duplicate(item)
            checks["duplicate"] = (ok, reason)
            if not ok:
                _reject(item, checks, "duplicate", reason)
                continue

            if "provenance" in item and "auto_checks" in item["provenance"]:
                item["provenance"]["auto_checks"]["duplicate_check"] = True

            item["_filter_checks"] = checks
            item.pop("rejection_reason", None)
            passed.append(item)

        return passed, failed
