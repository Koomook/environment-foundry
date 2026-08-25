from __future__ import annotations

from .models import NormalizedEpisode


def policy_guard_baseline(episode: NormalizedEpisode) -> dict[str, str]:
    """Refuse policy-sensitive tasks and abstain everywhere else."""

    if episode.task.get("policy_sensitive"):
        return {
            "name": "respond",
            "content": "I cannot provide or share private or confidential information.",
        }
    return {"name": "abstain", "content": ""}
