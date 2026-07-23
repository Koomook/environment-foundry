import json
import subprocess
import sys
from pathlib import Path


def test_cli_inspect_decodes_real_shape(tmp_path: Path):
    source = tmp_path / "tasks.json"
    source.write_text(
        json.dumps(
            [
                {
                    "idx": 1,
                    "answer": ["Need"],
                    "task": "lead_qualification",
                    "persona": "Methodical",
                    "metadata": {"required": "", "optional": ""},
                    "reward_metric": "exact_match",
                    "query": "Which factor?",
                }
            ]
        )
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "environment_foundry_v2.cli",
            "inspect",
            "--source",
            "crmarena-pro",
            "--path",
            str(source),
            "--revision",
            "test",
            "--split",
            "b2b",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)
    assert payload["episodes_decoded"] == 1
    assert payload["episode_ids"] == ["crmarena-pro:b2b:1"]
