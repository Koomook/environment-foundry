from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class NormalizedEpisode:
    """Loss-minimizing projection of an upstream task or scenario.

    ``raw_ref`` and ``provenance`` keep the projection auditable. A normalized
    episode does not imply that the source is interactive, resettable, causal,
    rights-valid for training, or a validated simulator.
    """

    schema_version: str
    episode_id: str
    source: dict[str, Any]
    split: str
    capability_level: int
    task: dict[str, Any]
    observation: dict[str, Any]
    action_space: list[dict[str, Any]]
    transition: dict[str, Any]
    termination: dict[str, Any]
    grader: dict[str, Any]
    rights: dict[str, Any]
    raw_ref: dict[str, Any]
    provenance: list[dict[str, Any]]
    limitations: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
