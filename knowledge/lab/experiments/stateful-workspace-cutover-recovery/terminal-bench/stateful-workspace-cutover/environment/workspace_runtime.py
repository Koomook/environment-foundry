"""Buggy starter runtime: functional tooling, wrong data lineage and unsafe cutover."""

from __future__ import annotations

import hashlib
import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any


EXACT_MIGRATION = "synthetic_cutover_v1"


class CutoverError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class WorkspaceRuntime:
    # The deterministic mock may set `faults.partial_export`,
    # `faults.pull_corrupt`, or `faults.stale_after_enroll` in remote_state.json.
    # A production-safe implementation must fail closed under those injected
    # conditions without exposing credential material.
    def __init__(self, root: Path | str):
        self.root = Path(root).resolve()
        self.source = self.root / "source.db"
        self.isolated = self.root / "isolated.db"
        self.remote_file = self.root / "remote_state.json"
        self.credential_file = self.root / "credential.json"
        self.authority_file = self.root / "authority.json"
        self.journal_file = self.root / "journal.jsonl"

    @staticmethod
    def semantic_hash(database: Path | str) -> str:
        # BUG: SQLite file bytes are not a canonical semantic representation.
        return hashlib.sha256(Path(database).read_bytes()).hexdigest()

    @staticmethod
    def _json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text())

    @staticmethod
    def _write(path: Path, value: dict[str, Any]) -> None:
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")

    def _active(self) -> bool:
        with sqlite3.connect(self.source) as connection:
            return bool(connection.execute("SELECT 1 FROM jobs WHERE status = 'active' LIMIT 1").fetchone())

    def _record_count(self, database: Path) -> int:
        with sqlite3.connect(database) as connection:
            return int(connection.execute("SELECT COUNT(*) FROM records").fetchone()[0])

    def status(self) -> dict[str, Any]:
        authority = self._json(self.authority_file)
        database = Path(authority["database_path"])
        return {
            "mode": authority["mode"],
            "active_job": self._active(),
            "record_count": self._record_count(database),
            "tools": list(authority.get("tools", [])),
        }

    def recover(self) -> dict[str, Any]:
        # BUG: enabling tools chooses a new empty store, splitting the lineage.
        authority = {
            "mode": "isolated",
            "database_path": str(self.isolated),
            "tools": ["history", "start_job"],
        }
        self._write(self.authority_file, authority)
        return self.status()

    def cutover(self) -> dict[str, Any]:
        if self._active():
            raise CutoverError("active_job_present")
        remote = self._json(self.remote_file)
        credential = self._json(self.credential_file)
        export = self.root / "export.db"
        shutil.copy2(self.source, export)

        # BUGS: raw token retention, no migration/head/CAS checks, no fresh
        # pull-back, and authority switches before semantic verification.
        remote["devices"][credential["device_id"]] = credential["device_token"]
        remote["head_revision"] = 1
        remote["head_hash"] = self.semantic_hash(export)
        remote["snapshots"] = [{"revision": 1, "path": str(export)}]
        self._write(self.remote_file, remote)
        self._write(
            self.authority_file,
            {"mode": "shared", "database_path": str(export), "tools": ["history", "start_job"]},
        )
        return self.status()
