from dataclasses import dataclass
import os


@dataclass
class Config:
    taxonomy_path: str = "taxonomy_v2.json"
    output_dir: str = "generated_items"

    # Models
    generation_model: str = "claude-sonnet-4-6"

    # Generation params
    items_per_batch: int = 10
    temperature: float = 0.7
    max_retries: int = 3

    # Items per skill (grammar)
    grammar_cloze: int = 15
    grammar_mc: int = 10
    grammar_error_correction: int = 8

    # Items per skill (vocabulary)
    vocab_cloze: int = 15
    vocab_mc: int = 10
    vocab_word_formation: int = 5

    # Rate limiting
    delay_between_calls: float = 1.0  # seconds

    # Cost tracking (USD per 1M tokens)
    sonnet_input_price: float = 3.0
    sonnet_output_price: float = 15.0
    sonnet_cache_write_price: float = 3.75
    sonnet_cache_read_price: float = 0.30

    @property
    def api_key(self) -> str:
        key = os.environ.get("ANTHROPIC_API_KEY", "")
        if not key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")
        return key
