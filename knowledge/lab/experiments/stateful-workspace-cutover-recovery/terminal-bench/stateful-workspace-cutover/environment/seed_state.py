#!/usr/bin/env python3
"""Create the agent-visible, entirely synthetic initial state."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path


def create_database(path: Path, *, active: bool, populated: bool) -> None:
    connection = sqlite3.connect(path)
    connection.executescript(
        """
        CREATE TABLE records (
            id TEXT PRIMARY KEY,
            kind TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        CREATE TABLE jobs (
            id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            payload TEXT NOT NULL
        );
        CREATE TABLE metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )
    if populated:
        connection.executemany(
            "INSERT INTO records VALUES (?, ?, ?)",
            [
                (f"synthetic-{index:02d}", "activity", json.dumps({"score": index * 3, "bucket": index % 4}, sort_keys=True))
                for index in range(1, 13)
            ],
        )
        connection.execute(
            "INSERT INTO jobs VALUES (?, ?, ?)",
            ("job-synthetic-active", "active" if active else "complete", json.dumps({"phase": "review"}, sort_keys=True)),
        )
        connection.execute("INSERT INTO metadata VALUES (?, ?)", ("lineage", "synthetic-v1"))
    connection.commit()
    connection.close()


def main() -> None:
    root = Path(sys.argv[1]).resolve()
    root.mkdir(parents=True, exist_ok=True)
    create_database(root / "source.db", active=True, populated=True)
    create_database(root / "isolated.db", active=False, populated=False)
    (root / "remote_state.json").write_text(
        json.dumps(
            {
                "migration_version": "synthetic_cutover_v1",
                "head_revision": 0,
                "head_hash": None,
                "snapshots": [],
                "devices": {},
                "faults": {},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    (root / "credential.json").write_text(
        json.dumps(
            {
                "device_id": "device-synthetic-source",
                "device_token": "synthetic-opaque-token-not-a-real-secret",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    (root / "authority.json").write_text(
        json.dumps(
            {
                "mode": "isolated",
                "database_path": str(root / "isolated.db"),
                "tools": ["history", "start_job"],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )
    (root / "journal.jsonl").write_text("")


if __name__ == "__main__":
    main()
