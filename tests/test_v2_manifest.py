from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = (
    ROOT
    / "knowledge"
    / "research"
    / "20260723-environment-foundry-v2"
    / "reproducibility-manifest.json"
)


def test_source_manifest_has_pinned_licenses_and_no_machine_paths() -> None:
    data = json.loads(MANIFEST.read_text())
    assert len(data["sources"]) >= 3
    for source in data["sources"]:
        assert source["url"].startswith("https://")
        assert source.get("revision") or source.get("code_revision")
        assert source["license"] in {"MIT", "CC-BY-NC-4.0", "CC-BY-4.0"}
        assert "local_path" not in source

    serialized = MANIFEST.read_text()
    assert "/Users/" not in serialized
    assert "test_used_for_training" not in serialized or (
        data["local_evidence"]["small_model_experiment"].get(
            "test_used_for_training", False
        )
        is False
    )
