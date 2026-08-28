from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from seed_state import create_database
from workspace_runtime import CutoverError, WorkspaceRuntime


def fixture(root: Path, *, active: bool) -> None:
    create_database(root / "source.db", active=active, populated=True)
    create_database(root / "isolated.db", active=False, populated=False)
    (root / "remote_state.json").write_text(json.dumps({
        "migration_version": "synthetic_cutover_v1", "head_revision": 0,
        "head_hash": None, "snapshots": [], "devices": {}, "faults": {},
    }))
    (root / "credential.json").write_text(json.dumps({
        "device_id": "visible-device", "device_token": "visible-token-000000000000",
    }))
    (root / "authority.json").write_text(json.dumps({
        "mode": "isolated", "database_path": str(root / "isolated.db"),
        "tools": ["history", "start_job"],
    }))
    (root / "journal.jsonl").write_text("")


class VisibleRuntimeTests(unittest.TestCase):
    def test_status_is_redacted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, active=True)
            result = WorkspaceRuntime(root).status()
            self.assertIn(result["mode"], {"isolated", "compat-local", "shared"})
            self.assertNotIn("payload", json.dumps(result))

    def test_active_cutover_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture(root, active=True)
            with self.assertRaises(CutoverError) as raised:
                WorkspaceRuntime(root).cutover()
            self.assertEqual(raised.exception.code, "active_job_present")


if __name__ == "__main__":
    unittest.main()
