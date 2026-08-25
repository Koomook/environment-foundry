from __future__ import annotations

import json
from pathlib import Path
from typing import Iterator

from .models import NormalizedEpisode


def _take(iterator: Iterator[NormalizedEpisode], limit: int | None):
    for index, item in enumerate(iterator):
        if limit is not None and index >= limit:
            break
        yield item


def load_crmarena_pro(
    path: str | Path,
    *,
    source_revision: str,
    split: str,
    limit: int | None = None,
) -> Iterator[NormalizedEpisode]:
    """Load the public CRMArenaPro JSON while preserving every upstream row."""

    source_path = Path(path).resolve()
    rows = json.loads(source_path.read_text())
    if not isinstance(rows, list):
        raise ValueError("CRMArenaPro source must be a JSON array")

    def convert() -> Iterator[NormalizedEpisode]:
        for row in rows:
            required = {
                "idx",
                "answer",
                "task",
                "persona",
                "metadata",
                "reward_metric",
                "query",
            }
            missing = sorted(required - row.keys())
            if missing:
                raise ValueError(f"CRMArenaPro row missing keys: {missing}")
            privacy_task = row["reward_metric"] == "privacy_rejection"
            yield NormalizedEpisode(
                schema_version="environment-foundry.normalized-episode.v2",
                episode_id=f"crmarena-pro:{split}:{row['idx']}",
                source={
                    "name": "Salesforce/CRMArenaPro",
                    "kind": "dataset+remote-environment",
                    "revision": source_revision,
                    "upstream_schema": sorted(row.keys()),
                },
                split=split,
                capability_level=2,
                task={
                    "family": row["task"],
                    "instruction": row["query"],
                    "persona": row["persona"],
                    "policy_sensitive": privacy_task,
                },
                observation={
                    "initial": {
                        "query": row["query"],
                        "metadata": row["metadata"],
                        "persona": row["persona"],
                    },
                    "boundary": "query, metadata, persona, and results of agent-authored Salesforce queries",
                    "partial_observability": True,
                },
                action_space=[
                    {
                        "name": "execute",
                        "input": "SOQL/SOSL query string",
                        "effect": "read from a shared remote Salesforce org",
                    },
                    {
                        "name": "respond",
                        "input": "final natural-language answer",
                        "effect": "terminate and grade",
                    },
                ],
                transition={
                    "mode": "remote_shared_state",
                    "implementation": "SalesforceConnector.run_query",
                    "reset": "logical task/action reset only",
                    "state_restore": False,
                },
                termination={
                    "conditions": ["respond action", "agent turn limit"],
                    "truncation_explicit_in_row": False,
                },
                grader={
                    "metric": row["reward_metric"],
                    "hidden_reference": row["answer"],
                    "reference_visible_to_policy": False,
                    "upstream_implementation": "crm_sandbox.env.env.Evaluator",
                    "model_judge_required": privacy_task
                    or row["reward_metric"] == "exact_match",
                },
                rights={
                    "license": "CC-BY-NC-4.0",
                    "commercial_use": False,
                    "training_permission": "not established by this adapter",
                },
                raw_ref={
                    "path": str(source_path),
                    "row_selector": {"idx": row["idx"]},
                    "raw": row,
                },
                provenance=[
                    {
                        "url": "https://huggingface.co/datasets/Salesforce/CRMArenaPro",
                        "revision": source_revision,
                    }
                ],
                limitations=[
                    "The public row is a task specification, not an interaction trajectory.",
                    "Upstream reset does not restore the shared Salesforce org per episode.",
                    "The local evaluator is an explicit approximation of LLM-based answer parsing.",
                    "No delayed company outcome is represented.",
                ],
            )

    yield from _take(convert(), limit)


def load_the_agent_company(
    root: str | Path,
    *,
    source_revision: str,
    limit: int | None = None,
) -> Iterator[NormalizedEpisode]:
    """Project TheAgentCompany task directories without copying their assets."""

    tasks_root = Path(root).resolve() / "workspaces" / "tasks"
    if not tasks_root.is_dir():
        raise ValueError(f"missing TheAgentCompany tasks directory: {tasks_root}")

    def convert() -> Iterator[NormalizedEpisode]:
        for task_dir in sorted(path for path in tasks_root.iterdir() if path.is_dir()):
            task_file = task_dir / "task.md"
            evaluator_file = task_dir / "evaluator.py"
            if not task_file.exists() or not evaluator_file.exists():
                continue
            instruction = task_file.read_text().strip()
            has_scenario = (task_dir / "scenarios.json").exists()
            yield NormalizedEpisode(
                schema_version="environment-foundry.normalized-episode.v2",
                episode_id=f"the-agent-company:{task_dir.name}",
                source={
                    "name": "TheAgentCompany/TheAgentCompany",
                    "kind": "dockerized multi-app benchmark",
                    "revision": source_revision,
                    "upstream_schema": [
                        "task.md",
                        "evaluator.py",
                        "Dockerfile",
                        "dependencies.yml",
                    ],
                },
                split="v1.0.0-public-task-images",
                capability_level=3,
                task={
                    "family": task_dir.name.split("-", 1)[0],
                    "instruction": instruction,
                    "scenario_variants": has_scenario,
                },
                observation={
                    "initial": {"instruction": instruction},
                    "boundary": "browser, workspace, terminal, and simulated company apps",
                    "partial_observability": True,
                },
                action_space=[
                    {
                        "name": "computer_or_shell_action",
                        "input": "agent-platform-specific",
                        "effect": "changes files or simulated company application state",
                    }
                ],
                transition={
                    "mode": "dockerized_multi_app",
                    "implementation": "task image plus company service backups",
                    "reset": "/utils/init.sh in the task image",
                    "state_restore": True,
                },
                termination={
                    "conditions": ["agent completion or harness limit"],
                    "truncation_explicit_in_task": False,
                },
                grader={
                    "metric": "weighted deterministic checkpoints",
                    "hidden_reference": None,
                    "reference_visible_to_policy": False,
                    "upstream_implementation": str(evaluator_file),
                    "model_judge_required": False,
                },
                rights={
                    "license": "MIT",
                    "commercial_use": True,
                    "training_permission": "code license permits use; service/content dependencies require separate review",
                },
                raw_ref={
                    "path": str(task_dir),
                    "row_selector": {"task_slug": task_dir.name},
                    "raw": {
                        "instruction": instruction,
                        "files": sorted(path.name for path in task_dir.iterdir()),
                    },
                },
                provenance=[
                    {
                        "url": "https://github.com/TheAgentCompany/TheAgentCompany",
                        "revision": source_revision,
                    }
                ],
                limitations=[
                    "The task is consequential inside a simulated company, not a longitudinal real company.",
                    "No delayed revenue, trust, or relationship outcome is observed.",
                    "A normalized projection cannot execute the upstream Docker/service stack.",
                ],
            )

    yield from _take(convert(), limit)


def load_gaia2_parquet(
    path: str | Path,
    *,
    source_revision: str,
    limit: int | None = None,
) -> Iterator[NormalizedEpisode]:
    """Load the real Gaia2 Parquet schema when the optional extra is present."""

    try:
        import pyarrow.parquet as parquet
    except ImportError as error:
        raise RuntimeError(
            "Gaia2 Parquet support requires: uv sync --extra parquet"
        ) from error

    source_path = Path(path).resolve()
    rows = parquet.read_table(source_path).to_pylist()

    def convert() -> Iterator[NormalizedEpisode]:
        for row in rows:
            required = {"id", "scenario_id", "split", "data", "category"}
            missing = sorted(required - row.keys())
            if missing:
                raise ValueError(f"Gaia2 row missing keys: {missing}")
            scenario = json.loads(row["data"])
            definition = scenario.get("metadata", {}).get("definition", {})
            apps = scenario.get("apps", [])
            events = scenario.get("events", [])
            yield NormalizedEpisode(
                schema_version="environment-foundry.normalized-episode.v2",
                episode_id=f"gaia2:{row['scenario_id']}",
                source={
                    "name": "meta-agents-research-environments/gaia2",
                    "kind": "dynamic event-driven multi-app environment",
                    "revision": source_revision,
                    "upstream_schema": sorted(row.keys()),
                },
                split=row["split"],
                capability_level=3,
                task={
                    "family": row["category"],
                    "instruction": definition.get("description")
                    or definition.get("task")
                    or "",
                    "scenario_tags": definition.get("tags", []),
                },
                observation={
                    "initial": {
                        "start_time": definition.get("start_time"),
                        "apps": [
                            {
                                "name": app.get("name"),
                                "class_name": app.get("class_name"),
                            }
                            for app in apps
                        ],
                    },
                    "boundary": "scenario app state plus temporally delivered events",
                    "partial_observability": True,
                },
                action_space=[
                    {
                        "name": "app_action",
                        "input": "typed action exposed by the scenario's apps",
                        "effect": "changes app state and may trigger events",
                    }
                ],
                transition={
                    "mode": "event_driven_simulation",
                    "implementation": "Meta Agents Research Environments",
                    "reset": "re-import scenario JSON and app state",
                    "state_restore": True,
                    "scheduled_events": len(events),
                },
                termination={
                    "conditions": ["scenario oracle completion or harness limit"],
                    "truncation_explicit_in_row": False,
                },
                grader={
                    "metric": "scenario oracle/checkers",
                    "hidden_reference": None,
                    "reference_visible_to_policy": False,
                    "upstream_implementation": "ARE oracle and Gaia2 judge",
                    "model_judge_required": True,
                },
                rights={
                    "license": "CC-BY-4.0 dataset; MIT code",
                    "commercial_use": True,
                    "training_permission": "dataset license permits adaptation with attribution",
                },
                raw_ref={
                    "path": str(source_path),
                    "row_selector": {"scenario_id": row["scenario_id"]},
                    "raw": row,
                },
                provenance=[
                    {
                        "url": "https://huggingface.co/datasets/meta-agents-research-environments/gaia2",
                        "revision": source_revision,
                    }
                ],
                limitations=[
                    "Dynamic simulation is not evidence of real-world causal validity.",
                    "The scenarios do not close longitudinal company economic outcomes.",
                    "LLM-judge components require separate calibration and exploitation tests.",
                ],
            )

    yield from _take(convert(), limit)
