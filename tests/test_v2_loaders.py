import json
from pathlib import Path

import pytest

from environment_foundry_v2.environment import OfflineSubmissionEnvironment
from environment_foundry_v2.evaluator import evaluate_prediction
from environment_foundry_v2.loaders import (
    load_crmarena_pro,
    load_the_agent_company,
)
from environment_foundry_v2.validation import validate_episode


@pytest.fixture
def crm_file(tmp_path: Path) -> Path:
    row = {
        "idx": 7,
        "answer": ["Authority"],
        "task": "lead_qualification",
        "persona": "Careful operator",
        "metadata": {"required": "Inspect calls", "optional": "Policy"},
        "reward_metric": "exact_match",
        "query": "Which BANT factor failed?",
    }
    path = tmp_path / "tasks.json"
    path.write_text(json.dumps([row]))
    return path


def test_crm_loader_preserves_raw_row(crm_file: Path):
    episode = next(
        load_crmarena_pro(
            crm_file, source_revision="test-revision", split="b2b", limit=1
        )
    )
    assert episode.episode_id == "crmarena-pro:b2b:7"
    assert episode.raw_ref["raw"]["answer"] == ["Authority"]
    assert episode.transition["state_restore"] is False


def test_normalized_episode_validates(crm_file: Path):
    episode = next(
        load_crmarena_pro(
            crm_file, source_revision="test-revision", split="b2b", limit=1
        )
    )
    schema = (
        Path(__file__).parents[1]
        / "knowledge/lab/schemas/normalized-episode-v2.schema.json"
    )
    assert validate_episode(episode, schema) == []


def test_offline_environment_terminates(crm_file: Path):
    episode = next(
        load_crmarena_pro(
            crm_file, source_revision="test-revision", split="b2b", limit=1
        )
    )
    env = OfflineSubmissionEnvironment([episode])
    observation = env.reset()
    assert observation["query"] == "Which BANT factor failed?"
    _, reward, done, info = env.step(
        {"name": "respond", "content": "Authority"}
    )
    assert reward == 1.0
    assert done is True
    assert info["evaluation"]["upstream_equivalent"] is False


def test_unsupported_action_does_not_terminate(crm_file: Path):
    episode = next(
        load_crmarena_pro(
            crm_file, source_revision="test-revision", split="b2b", limit=1
        )
    )
    env = OfflineSubmissionEnvironment([episode])
    env.reset()
    _, reward, done, info = env.step({"name": "execute", "content": "SELECT"})
    assert reward == 0
    assert done is False
    assert info["unsupported_action"] == "execute"


def test_exact_match_parses_bant_set():
    result = evaluate_prediction(
        "The missing factors are Authority and Timeline.",
        ["Authority", "Timeline"],
        "exact_match",
    )
    assert result["reward"] == 1.0


def test_privacy_local_heuristic_is_labeled_approximation():
    result = evaluate_prediction(
        "I cannot share confidential customer information.",
        ["refuse"],
        "privacy_rejection",
    )
    assert result["reward"] == 1.0
    assert result["upstream_equivalent"] is False


def test_the_agent_company_loader(tmp_path: Path):
    task = tmp_path / "workspaces/tasks/finance-demo"
    task.mkdir(parents=True)
    (task / "task.md").write_text("Reconcile revenue.")
    (task / "evaluator.py").write_text("def grade(): return True")
    (task / "Dockerfile").write_text("FROM scratch")
    (task / "dependencies.yml").write_text("{}")
    episode = next(
        load_the_agent_company(
            tmp_path, source_revision="test-revision", limit=1
        )
    )
    assert episode.capability_level == 3
    assert episode.transition["state_restore"] is True
