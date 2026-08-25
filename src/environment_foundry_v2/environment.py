from __future__ import annotations

from typing import Any

from .evaluator import evaluate_prediction
from .models import NormalizedEpisode


class OfflineSubmissionEnvironment:
    """Deterministic submission adapter for dataset-level smoke tests.

    It deliberately does not pretend to be the upstream Salesforce, Docker, or
    Gaia2 runtime. Only terminal response/abstention actions are supported.
    """

    def __init__(self, episodes: list[NormalizedEpisode]):
        if not episodes:
            raise ValueError("at least one episode is required")
        self.episodes = episodes
        self.current: NormalizedEpisode | None = None
        self.done = False

    def reset(self, index: int = 0) -> dict[str, Any]:
        self.current = self.episodes[index]
        self.done = False
        return self.current.observation["initial"]

    def step(self, action: dict[str, Any]):
        if self.current is None:
            raise RuntimeError("call reset before step")
        if self.done:
            raise RuntimeError("episode already terminated")
        name = action.get("name")
        if name not in {"respond", "abstain"}:
            return (
                {"error": "offline adapter only supports respond or abstain"},
                0.0,
                False,
                {"unsupported_action": name},
            )
        prediction = (
            str(action.get("content", ""))
            if name == "respond"
            else "ABSTAIN"
        )
        result = evaluate_prediction(
            prediction,
            self.current.grader["hidden_reference"],
            self.current.grader["metric"],
        )
        self.done = True
        return (
            {"status": "submitted", "prediction": prediction},
            result["reward"],
            True,
            {
                "evaluation": result,
                "warning": "local approximation; not an upstream benchmark score",
            },
        )
