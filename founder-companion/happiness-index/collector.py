#!/usr/bin/env python3
"""Collect a founder-private, provenance-preserving Life Index snapshot.

The collector intentionally does not infer another person's happiness or turn
passive activity counts into a decision-grade happiness score. It records what
is observable, marks proxy-only and missing dimensions, and preserves every run
under the ignored private plane.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[2]
PRIVATE_ROOT = (
    REPO_ROOT / "private-plane/payload/founder-companion/happiness-index"
)
SNAPSHOT_ROOT = PRIVATE_ROOT / "snapshots"
CONTEXT_LEDGER_DB = (
    Path.home() / "team-attention/personal-context-vault/var/ledger.db"
)
HEALTH_WORKBOOK = (
    REPO_ROOT
    / "private-plane/payload/founder-companion/outputs/"
    "019f9dd5-6548-7503-8237-3d097e31719b/"
    "구봉 Health & Training OS.xlsx"
)
HEALTH_VALIDATION = HEALTH_WORKBOOK.with_name("validation.json")
DEEP_THOUGHT_REGISTRY = PRIVATE_ROOT / "sources/deep-thought-registry.json"
CANDIDATES_PATH = PRIVATE_ROOT / "dimensions/candidates.json"
REVIEW_STATE_PATH = PRIVATE_ROOT / "reviews/state.json"
GIT_ROOTS = [
    REPO_ROOT,
    Path.home() / "team-attention/deep-thought",
]
DIMENSION_WEIGHTS = {
    "experienced_wellbeing_presence": 0.20,
    "family_presence_stewardship": 0.20,
    "health_usable_capacity": 0.15,
    "meaningful_work_company_proof": 0.15,
    "cash_safety_freedom": 0.15,
    "learning_possibility": 0.10,
    "integrity_self_trust": 0.05,
}


def iso_z(value: datetime) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def parse_time(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(UTC)
    except ValueError:
        return None


def run_json(command: list[str], timeout: int = 45) -> tuple[Any | None, str | None]:
    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return json.loads(completed.stdout), None
    except FileNotFoundError:
        return None, f"command-not-found:{command[0]}"
    except subprocess.TimeoutExpired:
        return None, f"timeout:{command[0]}"
    except subprocess.CalledProcessError as exc:
        detail = (exc.stderr or "").strip().splitlines()
        return None, f"command-failed:{command[0]}:{detail[-1] if detail else exc.returncode}"
    except json.JSONDecodeError:
        return None, f"invalid-json:{command[0]}"


def file_receipt(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": str(path), "exists": False}
    stat = path.stat()
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": stat.st_size,
        "modified_at": iso_z(datetime.fromtimestamp(stat.st_mtime, UTC)),
    }


def hashed_file_receipt(path: Path) -> dict[str, Any]:
    receipt = file_receipt(path)
    if receipt["exists"]:
        receipt["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    return receipt


def collect_definition_state() -> dict[str, Any]:
    current_item = None
    completed = None
    total = None
    if REVIEW_STATE_PATH.exists():
        try:
            state = json.loads(REVIEW_STATE_PATH.read_text(encoding="utf-8"))
            current_item = state.get("current_item")
            completed = state.get("completed")
            total = state.get("total")
        except (OSError, json.JSONDecodeError):
            pass
    return {
        "status": "under-founder-review",
        "candidates": hashed_file_receipt(CANDIDATES_PATH),
        "review_state": hashed_file_receipt(REVIEW_STATE_PATH),
        "current_item": current_item,
        "completed": completed,
        "total": total,
        "weight_status": "suspended-until-meaning-review",
    }


def collect_deep_thought_context() -> dict[str, Any]:
    """Verify registered Deep Thought context without copying its content."""
    if not DEEP_THOUGHT_REGISTRY.exists():
        return {
            "status": "unconfigured",
            "registry": file_receipt(DEEP_THOUGHT_REGISTRY),
            "sources": [],
        }
    try:
        registry = json.loads(DEEP_THOUGHT_REGISTRY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return {
            "status": "unavailable",
            "registry": file_receipt(DEEP_THOUGHT_REGISTRY),
            "error": str(exc),
            "sources": [],
        }
    receipts = []
    for source in registry.get("sources", []):
        path = Path(source["path"])
        exists = path.is_file()
        current_hash = (
            hashlib.sha256(path.read_bytes()).hexdigest() if exists else None
        )
        receipts.append(
            {
                "source_id": source["id"],
                "type": source.get("type"),
                "locator": str(path),
                "exists": exists,
                "expected_sha256": source.get("sha256"),
                "current_sha256": current_hash,
                "hash_matches": current_hash == source.get("sha256") if exists else False,
                "modified_at": file_receipt(path).get("modified_at"),
            }
        )
    missing = [item["source_id"] for item in receipts if not item["exists"]]
    changed = [
        item["source_id"]
        for item in receipts
        if item["exists"] and not item["hash_matches"]
    ]
    return {
        "status": "observed" if not missing and not changed else "review-required",
        "registry": file_receipt(DEEP_THOUGHT_REGISTRY),
        "sources": receipts,
        "missing_sources": missing,
        "changed_sources": changed,
        "source_boundary": (
            "path, type, timestamps, and hashes only; no Deep Thought content copied"
        ),
    }


def collect_monologue(start: datetime, end: datetime) -> dict[str, Any]:
    payload, error = run_json(
        [
            "monologue",
            "notes",
            "all",
            "-created-after",
            iso_z(start),
            "-created-before",
            iso_z(end),
            "-limit",
            "100",
        ]
    )
    if error:
        return {"status": "unavailable", "error": error, "notes": []}
    items = payload.get("items", payload if isinstance(payload, list) else [])
    notes = [
        {
            "note_id": item.get("note_id"),
            "title": item.get("title"),
            "summary": item.get("summary"),
            "created_at": item.get("created_at"),
            "updated_at": item.get("updated_at"),
        }
        for item in items
    ]
    return {
        "status": "observed",
        "count": len(notes),
        "notes": notes,
        "source_boundary": "metadata and provider summary; full transcript stays at Monologue source",
    }


def event_bounds(event: dict[str, Any]) -> tuple[datetime | None, datetime | None]:
    start_value = event.get("start", {})
    end_value = event.get("end", {})
    start_raw = start_value.get("dateTime")
    end_raw = end_value.get("dateTime")
    if start_raw and end_raw:
        return parse_time(start_raw), parse_time(end_raw)
    start_date = start_value.get("date")
    end_date = end_value.get("date")
    if start_date and end_date:
        return (
            datetime.combine(date.fromisoformat(start_date), datetime.min.time(), UTC),
            datetime.combine(date.fromisoformat(end_date), datetime.min.time(), UTC),
        )
    return None, None


def collect_calendar(start: datetime, end: datetime) -> dict[str, Any]:
    payload, error = run_json(
        [
            "gog",
            "cal",
            "events",
            "primary",
            "--from",
            start.date().isoformat(),
            "--to",
            end.date().isoformat(),
            "-j",
            "--results-only",
        ]
    )
    if error:
        return {"status": "unavailable", "error": error, "events": []}
    events = []
    timed_minutes = 0
    category_minutes: Counter[str] = Counter()
    for event in payload if isinstance(payload, list) else []:
        event_start, event_end = event_bounds(event)
        minutes = 0
        if event_start and event_end:
            minutes = max(0, int((event_end - event_start).total_seconds() / 60))
            timed_minutes += minutes
        summary = event.get("summary") or ""
        lowered = summary.lower()
        category = "unclassified"
        if any(token in lowered for token in ("focus", "light", "company", "회사")):
            category = "work-labelled"
        elif any(token in lowered for token in ("운동", "달리", "헬스", "run", "cardio")):
            category = "movement-labelled"
        elif any(token in lowered for token in ("가족", "유주", "예진")):
            category = "family-labelled"
        category_minutes[category] += minutes
        events.append(
            {
                "event_id": event.get("id"),
                "summary": summary,
                "start": event.get("start"),
                "end": event.get("end"),
                "status": event.get("status"),
                "category_hint": category,
                "scheduled_minutes": minutes,
            }
        )
    return {
        "status": "observed",
        "count": len(events),
        "scheduled_minutes": timed_minutes,
        "category_minutes": dict(category_minutes),
        "events": events,
        "source_boundary": "calendar is planned time, not proof of attendance, presence, or outcome",
    }


def codex_files_for_window(start: datetime, end: datetime) -> list[Path]:
    roots = [Path.home() / ".codex/sessions", Path.home() / ".codex/archived_sessions"]
    files: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*.jsonl"):
            stat = path.stat()
            modified = datetime.fromtimestamp(stat.st_mtime, UTC)
            if modified >= start - timedelta(days=1) and modified <= end + timedelta(days=1):
                files.append(path)
    return files


def collect_codex(start: datetime, end: datetime) -> dict[str, Any]:
    counts: Counter[str] = Counter()
    active_files: list[dict[str, Any]] = []
    for path in codex_files_for_window(start, end):
        per_file: Counter[str] = Counter()
        try:
            with path.open(encoding="utf-8") as handle:
                for line in handle:
                    try:
                        record = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    timestamp = parse_time(record.get("timestamp"))
                    if not timestamp or timestamp < start or timestamp >= end:
                        continue
                    payload = record.get("payload") or {}
                    record_type = record.get("type") or "unknown"
                    payload_type = payload.get("type") or "unknown"
                    key = f"{record_type}:{payload_type}"
                    counts[key] += 1
                    per_file[key] += 1
                    if payload_type == "message":
                        role = payload.get("role") or "unknown"
                        counts[f"message:{role}"] += 1
                        per_file[f"message:{role}"] += 1
                    if record_type == "event_msg" and payload_type == "patch_apply_end":
                        counts["artifact:file_patch"] += 1
                        per_file["artifact:file_patch"] += 1
        except OSError:
            continue
        if per_file:
            active_files.append(
                {
                    "locator": str(path),
                    "events": sum(per_file.values()),
                    "counts": dict(per_file),
                }
            )
    return {
        "status": "observed" if active_files else "missing",
        "active_session_files": len(active_files),
        "counts": dict(counts),
        "sessions": active_files,
        "source_boundary": "activity and artifact events only; activity is not meaningful outcome",
    }


def collect_git(start: datetime) -> dict[str, Any]:
    repositories = []
    for root in GIT_ROOTS:
        if not (root / ".git").exists():
            continue
        log, log_error = run_json(
            [
                "git",
                "-C",
                str(root),
                "log",
                f"--since={iso_z(start)}",
                "--pretty=format:[%H,%cI,%s]",
            ]
        )
        # The compact git format above is not valid JSON when subjects contain
        # quotes, so fall back to a delimiter-safe text command.
        commits: list[dict[str, str]] = []
        if log_error:
            try:
                completed = subprocess.run(
                    [
                        "git",
                        "-C",
                        str(root),
                        "log",
                        f"--since={iso_z(start)}",
                        "--pretty=format:%H%x1f%cI%x1f%s%x1e",
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                    timeout=20,
                )
                for record in completed.stdout.split("\x1e"):
                    fields = record.strip().split("\x1f")
                    if len(fields) == 3:
                        commits.append(
                            {"sha": fields[0], "committed_at": fields[1], "subject": fields[2]}
                        )
            except (FileNotFoundError, subprocess.SubprocessError):
                pass
        status_count = 0
        try:
            completed = subprocess.run(
                ["git", "-C", str(root), "status", "--short"],
                check=True,
                capture_output=True,
                text=True,
                timeout=20,
            )
            status_count = len([line for line in completed.stdout.splitlines() if line])
        except (FileNotFoundError, subprocess.SubprocessError):
            pass
        repositories.append(
            {
                "path": str(root),
                "commits": commits,
                "commit_count": len(commits),
                "dirty_path_count": status_count,
            }
        )
    return {
        "status": "observed" if repositories else "unavailable",
        "repositories": repositories,
        "total_commits": sum(repo["commit_count"] for repo in repositories),
        "source_boundary": "commit and dirty-path counts are output proxies, not value or completion",
    }


def collect_context_ledger(start: datetime) -> dict[str, Any]:
    receipt = file_receipt(CONTEXT_LEDGER_DB)
    if not CONTEXT_LEDGER_DB.exists():
        return {"status": "unavailable", "database": receipt}
    try:
        connection = sqlite3.connect(f"file:{CONTEXT_LEDGER_DB}?mode=ro", uri=True)
        counts = connection.execute(
            """
            SELECT source, COUNT(*), MAX(occurred_at)
            FROM events
            WHERE occurred_at >= ?
            GROUP BY source
            ORDER BY source
            """,
            (iso_z(start),),
        ).fetchall()
        health = connection.execute(
            """
            SELECT source, available, detail, checked_at
            FROM source_health
            ORDER BY source
            """
        ).fetchall()
        connection.close()
    except sqlite3.Error as exc:
        return {"status": "unavailable", "database": receipt, "error": str(exc)}
    now = datetime.now(UTC)
    freshness_by_source = {}
    for source, _, occurred_at in counts:
        observed_at = parse_time(occurred_at)
        threshold = timedelta(hours=2) if source == "ambient-audio" else timedelta(hours=24)
        freshness_by_source[source] = (
            "fresh"
            if observed_at and now - observed_at < threshold
            else "stale-or-sparse"
        )
    health_freshness = {}
    for source, _, _, checked_at in health:
        observed_at = parse_time(checked_at)
        health_freshness[source] = (
            "fresh"
            if observed_at and now - observed_at < timedelta(hours=24)
            else "stale"
        )
    stale_sources = sorted(
        {
            source
            for source, status in freshness_by_source.items()
            if status != "fresh"
        }
        | {
            source
            for source, status in health_freshness.items()
            if status != "fresh"
        }
    )
    return {
        "status": "observed",
        "database": receipt,
        "event_counts": [
            {"source": row[0], "count": row[1], "last_event_at": row[2]} for row in counts
        ],
        "source_health": [
            {
                "source": row[0],
                "available": bool(row[1]),
                "detail": row[2],
                "checked_at": row[3],
            }
            for row in health
        ],
        "freshness": "fresh" if not stale_sources else "partial-stale",
        "freshness_by_source": freshness_by_source,
        "source_health_freshness": health_freshness,
        "stale_sources": stale_sources,
        "source_boundary": "processed ledger counts only; no raw conversation copied",
    }


def collect_health() -> dict[str, Any]:
    workbook_receipt = file_receipt(HEALTH_WORKBOOK)
    validation_receipt = file_receipt(HEALTH_VALIDATION)
    current_week = None
    error = None
    if HEALTH_VALIDATION.exists():
        try:
            payload = json.loads(HEALTH_VALIDATION.read_text(encoding="utf-8"))
            dashboard = payload.get("dashboard")
            table = json.loads(dashboard) if isinstance(dashboard, str) else dashboard
            rows = (table or {}).get("values", [])
            today = datetime.now().date()
            candidates = []
            for row in rows[1:]:
                if not row or not row[0]:
                    continue
                raw_date = str(row[0]).replace("Z", "+00:00")
                try:
                    week_start = datetime.fromisoformat(raw_date).date()
                except ValueError:
                    continue
                if week_start <= today < week_start + timedelta(days=7):
                    candidates.append(row)
            if candidates:
                row = candidates[-1]
                current_week = {
                    "week_start": row[0],
                    "strength_sets_done": row[1],
                    "strength_volume": row[2],
                    "cardio_sessions": row[3],
                    "cardio_minutes": row[4],
                    "average_sleep_hours": row[5],
                    "average_energy": row[6],
                    "max_pain": row[7],
                    "planned_sessions": row[8],
                    "completed_sessions": row[9],
                    "adherence": row[10],
                    "decision": row[11],
                    "learning": row[12],
                }
        except (json.JSONDecodeError, TypeError, IndexError) as exc:
            error = str(exc)
    has_current_measurement = bool(
        current_week
        and any(
            current_week.get(field) not in (None, "", 0)
            for field in (
                "strength_sets_done",
                "cardio_sessions",
                "cardio_minutes",
                "average_sleep_hours",
                "average_energy",
                "max_pain",
            )
        )
    )
    return {
        "status": "observed" if has_current_measurement else "missing-current-measurement",
        "workbook": workbook_receipt,
        "validation": validation_receipt,
        "current_week": current_week,
        "error": error,
        "source_boundary": "read-only dashboard projection; not diagnosis or training clearance",
    }


def dimension_coverage(sources: dict[str, Any]) -> dict[str, dict[str, Any]]:
    monologue_count = sources["monologue"].get("count", 0)
    calendar_count = sources["calendar"].get("count", 0)
    health_observed = sources["health"].get("status") == "observed"
    work_observed = (
        sources["codex"].get("active_session_files", 0) > 0
        or sources["git"].get("total_commits", 0) > 0
    )
    coverage = {
        "experienced_wellbeing_presence": {
            "coverage": 0.45 if monologue_count else 0.10,
            "status": "proxy-only" if monologue_count else "missing",
            "reason": "natural voice can contain self-report but silence is not low well-being",
        },
        "family_presence_stewardship": {
            "coverage": 0.30 if calendar_count or monologue_count else 0.0,
            "status": "proxy-only" if calendar_count or monologue_count else "missing",
            "reason": "calendar and founder speech cannot establish presence quality or another person's happiness",
        },
        "health_usable_capacity": {
            "coverage": 0.85 if health_observed else 0.0,
            "status": "observed" if health_observed else "missing",
            "reason": "current Health OS measurement exists" if health_observed else "Health OS has no current measurement",
        },
        "meaningful_work_company_proof": {
            "coverage": 0.65 if work_observed else 0.0,
            "status": "observed-proxies" if work_observed else "missing",
            "reason": "artifacts and activity observed; value and outcome still require review",
        },
        "cash_safety_freedom": {
            "coverage": 0.0,
            "status": "missing",
            "reason": "no authorized bank, accounting, or cash-ledger connector",
        },
        "learning_possibility": {
            "coverage": 0.35 if monologue_count or work_observed else 0.0,
            "status": "proxy-only" if monologue_count or work_observed else "missing",
            "reason": "notes and artifacts show attempts, not validated capability change",
        },
        "integrity_self_trust": {
            "coverage": 0.20 if calendar_count and work_observed else 0.0,
            "status": "proxy-only" if calendar_count and work_observed else "missing",
            "reason": "planned and produced traces exist, but promise truth and renegotiation are not resolved",
        },
    }
    return coverage


def build_snapshot(days: int, now: datetime | None = None) -> dict[str, Any]:
    end = (now or datetime.now(UTC)).astimezone(UTC)
    start = end - timedelta(days=days)
    sources = {
        "deep_thought_context": collect_deep_thought_context(),
        "monologue": collect_monologue(start, end),
        "calendar": collect_calendar(start, end),
        "codex": collect_codex(start, end),
        "git": collect_git(start),
        "context_ledger": collect_context_ledger(start),
        "health": collect_health(),
        "cash": {
            "status": "unconfigured",
            "source_boundary": "no financial source inferred from email, speech, or company data",
        },
    }
    legacy_proxy_coverage = dimension_coverage(sources)
    confidence = sum(
        DIMENSION_WEIGHTS[name] * item["coverage"]
        for name, item in legacy_proxy_coverage.items()
    )
    return {
        "schema_version": "0.3",
        "generated_at": iso_z(end),
        "window": {"start": iso_z(start), "end": iso_z(end), "days": days},
        "privacy_class": "founder-private",
        "definition_state": collect_definition_state(),
        "sources": sources,
        "legacy_proxy_coverage": legacy_proxy_coverage,
        "calculation": {
            "formula_version": "v0.1",
            "baseline_anchor": 100,
            "current_index": 100,
            "score_status": "baseline-anchor-only-dimensions-under-review",
            "confidence": round(confidence, 4),
            "confidence_status": "legacy-source-coverage-only",
            "decision_grade": False,
            "explanation": (
                "The first passive snapshot anchors comparison at 100. "
                "Candidate meanings and weights are still under founder review, and "
                "insufficient direct coverage prevents an absolute or decision-grade score."
            ),
        },
        "non_inference_rules": [
            "calendar time is not proof of attendance or presence",
            "agent activity is not meaningful outcome",
            "founder speech does not establish another person's happiness",
            "missing data is not imputed as good or bad",
        ],
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, delete=False
    ) as handle:
        json.dump(payload, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
        temp_path = Path(handle.name)
    os.replace(temp_path, path)


def persist_snapshot(snapshot: dict[str, Any]) -> tuple[Path, str]:
    generated = parse_time(snapshot["generated_at"]) or datetime.now(UTC)
    stamp = generated.strftime("%Y%m%dT%H%M%SZ")
    path = SNAPSHOT_ROOT / f"{stamp}.json"
    atomic_json(path, snapshot)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    receipt = {
        "snapshot": str(path),
        "sha256": digest,
        "generated_at": snapshot["generated_at"],
        "score_status": snapshot["calculation"]["score_status"],
        "confidence": snapshot["calculation"]["confidence"],
    }
    atomic_json(SNAPSHOT_ROOT / "latest.json", receipt)
    baseline_path = SNAPSHOT_ROOT / "baseline.json"
    if not baseline_path.exists():
        atomic_json(
            baseline_path,
            {
                "baseline_snapshot": str(path),
                "sha256": digest,
                "anchor": 100,
                "created_at": snapshot["generated_at"],
                "status": "provisional-passive-baseline",
            },
        )
    return path, digest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Collect and preserve an automatic Life Index snapshot."
    )
    parser.add_argument("--days", type=int, default=7, choices=range(1, 32))
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="collect and print the summary without persisting",
    )
    args = parser.parse_args()
    snapshot = build_snapshot(args.days)
    path = None
    digest = None
    if not args.dry_run:
        path, digest = persist_snapshot(snapshot)
    summary = {
        "ok": True,
        "snapshot": str(path) if path else None,
        "sha256": digest,
        "window": snapshot["window"],
        "calculation": snapshot["calculation"],
        "definition_state": snapshot["definition_state"],
        "legacy_proxy_coverage": snapshot["legacy_proxy_coverage"],
        "source_status": {
            name: (
                f"{value.get('status', 'unknown')}:{value['freshness']}"
                if value.get("freshness")
                else value.get("status", "unknown")
            )
            for name, value in snapshot["sources"].items()
        },
    }
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
