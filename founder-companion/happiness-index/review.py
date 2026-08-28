#!/usr/bin/env python3
"""Show and record one-at-a-time Life Index dimension reviews."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
import uuid
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_ROOT = REPO_ROOT / "private-plane/payload/founder-companion/happiness-index"
CANDIDATES_PATH = PRIVATE_ROOT / "dimensions/candidates.json"
STATE_PATH = PRIVATE_ROOT / "reviews/state.json"
EVENTS_PATH = PRIVATE_ROOT / "reviews/events.jsonl"
DISPOSITIONS = {"CONFIRM", "REVISE", "REJECT", "PARK"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def candidate_hash(path: Path = CANDIDATES_PATH) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def current_candidate(
    candidates_path: Path = CANDIDATES_PATH, state_path: Path = STATE_PATH
) -> dict[str, Any] | None:
    candidates = load_json(candidates_path)
    state = load_json(state_path)
    current_id = state.get("current_item")
    return next(
        (item for item in candidates["items"] if item["id"] == current_id), None
    )


def append_event(
    candidate_id: str,
    disposition: str,
    rephrase: str,
    source_locator: str,
    idempotency_key: str,
    *,
    candidates_path: Path = CANDIDATES_PATH,
    state_path: Path = STATE_PATH,
    events_path: Path = EVENTS_PATH,
) -> dict[str, Any]:
    disposition = disposition.upper()
    if disposition not in DISPOSITIONS:
        raise ValueError(f"invalid disposition: {disposition}")
    if not source_locator or not idempotency_key:
        raise ValueError("source_locator and idempotency_key are required")
    candidates = load_json(candidates_path)
    state = load_json(state_path)
    items_by_id = {item["id"]: item for item in candidates["items"]}
    if candidate_id not in items_by_id:
        raise ValueError(f"unknown candidate: {candidate_id}")
    if state.get("current_item") != candidate_id:
        raise ValueError(
            f"review order violation: current={state.get('current_item')} requested={candidate_id}"
        )
    if events_path.exists():
        for line in events_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            existing = json.loads(line)
            if existing.get("idempotency_key") == idempotency_key:
                return existing
    event = {
        "event_id": str(uuid.uuid4()),
        "recorded_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        "candidate_id": candidate_id,
        "candidate_title": items_by_id[candidate_id]["title"],
        "disposition": disposition,
        "founder_meaning_rephrase": rephrase,
        "source_locator": source_locator,
        "idempotency_key": idempotency_key,
        "candidate_set_hash": candidate_hash(candidates_path),
        "privacy_class": "founder-private",
    }
    events_path.parent.mkdir(parents=True, exist_ok=True)
    with events_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    state.setdefault("items", {})[candidate_id] = {
        "disposition": disposition,
        "event_id": event["event_id"],
        "recorded_at": event["recorded_at"],
    }
    order = candidates["review_order"]
    index = order.index(candidate_id)
    state["completed"] = len(state["items"])
    state["current_item"] = order[index + 1] if index + 1 < len(order) else None
    atomic_json(state_path, state)
    return event


def main() -> int:
    parser = argparse.ArgumentParser(description="Review Life Index dimensions.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("show")
    record = subparsers.add_parser("record")
    record.add_argument("candidate_id")
    record.add_argument("disposition", choices=sorted(DISPOSITIONS))
    record.add_argument("--rephrase", required=True)
    record.add_argument("--source-locator", required=True)
    record.add_argument("--idempotency-key", required=True)
    args = parser.parse_args()
    if args.command == "show":
        item = current_candidate()
        print(json.dumps(item, ensure_ascii=False, indent=2))
        return 0
    event = append_event(
        args.candidate_id,
        args.disposition,
        args.rephrase,
        args.source_locator,
        args.idempotency_key,
    )
    print(json.dumps(event, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
