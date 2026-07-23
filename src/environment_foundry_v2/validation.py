from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from .models import NormalizedEpisode


def validate_episode(
    episode: NormalizedEpisode, schema_path: str | Path
) -> list[str]:
    schema = json.loads(Path(schema_path).read_text())
    validator = Draft202012Validator(schema)
    return [
        error.message
        for error in sorted(
            validator.iter_errors(episode.to_dict()), key=lambda item: list(item.path)
        )
    ]
