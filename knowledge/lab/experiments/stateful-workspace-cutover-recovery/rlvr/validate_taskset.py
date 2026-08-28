#!/usr/bin/env python3
"""Fail-closed structural validation for the HUD v6 portable task rows."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
TASKSET = ROOT / "taskset.jsonl"
RECEIPT = ROOT.parent / "rights-receipt.json"


def main() -> int:
    rows = [json.loads(line) for line in TASKSET.read_text().splitlines() if line.strip()]
    receipt = json.loads(RECEIPT.read_text())
    errors: list[str] = []
    slugs = [row.get("slug") for row in rows]
    if len(rows) != 20:
        errors.append(f"expected 20 rows, found {len(rows)}")
    if len(set(slugs)) != len(slugs):
        errors.append("task slugs are not unique")
    splits = Counter(row.get("columns", {}).get("split") for row in rows)
    if splits != Counter({"train_candidate": 12, "dev": 4, "visible_eval": 4}):
        errors.append(f"unexpected split counts: {dict(splits)}")
    if receipt.get("status") != "pending_ef03" or receipt.get("grants", {}).get("training") is not False:
        errors.append("current receipt must fail closed on training pending EF-03")

    for index, row in enumerate(rows, start=1):
        label = row.get("slug") or f"row-{index}"
        if row.get("env") != "stateful-workspace-cutover" or row.get("id") != "repair-cutover":
            errors.append(f"{label}: wrong actor environment/template")
        args = row.get("args")
        if not isinstance(args, dict) or not isinstance(args.get("seed"), int) or not args.get("profile"):
            errors.append(f"{label}: invalid args")
        columns = row.get("columns")
        if not isinstance(columns, dict) or columns.get("rights") not in {"synthetic-candidate", "synthetic-eval"}:
            errors.append(f"{label}: invalid rights facet")
        if columns and columns.get("catalog_status") != "unimplemented-template":
            errors.append(f"{label}: catalog overstates executable status")
        if columns and columns.get("split") == "train_candidate":
            if columns.get("rights") != "synthetic-candidate" or columns.get("training_eligibility") != "pending_ef03":
                errors.append(f"{label}: candidate rights mismatch")
        elif columns and (
            columns.get("rights") != "synthetic-eval"
            or columns.get("training_eligibility") != "denied"
        ):
            errors.append(f"{label}: evaluation row is not fail-closed")
        agent_config = row.get("agent_config")
        if agent_config != {"timeout_seconds": 7200}:
            errors.append(f"{label}: invalid agent config")
        verifier = row.get("verifier")
        if not isinstance(verifier, dict):
            errors.append(f"{label}: missing verifier")
            continue
        if verifier.get("env") != "stateful-workspace-cutover-verifier" or verifier.get("id") != "verify-cutover":
            errors.append(f"{label}: wrong verifier environment/template")
        if verifier.get("verifier") is not None:
            errors.append(f"{label}: nested verifier is forbidden")
        if verifier.get("args", {}).get("case_slug") != label:
            errors.append(f"{label}: verifier case mismatch")

    if errors:
        print("HUD taskset validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("HUD draft catalog structural validation: PASS (20 rows; train_candidate=12, dev=4, visible_eval=4; training denied)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
