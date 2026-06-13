"""
Usage:
    python run.py test                  # 2 skills only (~$0.30)
    python run.py generate              # all skills
    python run.py generate --skip-filters   # no LLM filters (cheaper)
    python run.py stats                 # show stats on generated items
"""
import sys
import os

# Allow running from the project root without installing
sys.path.insert(0, os.path.dirname(__file__))

from content_generation.config import Config
from content_generation.pipeline import Pipeline


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    command = args[0]
    flags = args[1:]

    config = Config()

    if "--skip-filters" in flags:
        config.skip_llm_filters = True
        print("LLM filters disabled.")

    if "--no-dedup" in flags:
        config.enable_dedup = False
        print("Deduplication disabled.")

    pipeline = Pipeline(config)

    if command == "test":
        pipeline.run_test()

    elif command == "generate":
        pipeline.run_all()

    elif command == "stats":
        pipeline.stats()

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
