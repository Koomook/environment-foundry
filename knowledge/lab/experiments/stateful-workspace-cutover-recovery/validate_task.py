#!/usr/bin/env python3
"""Validate no-op/oracle controls and kill behavior-changing oracle mutants."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
TASK = ROOT / "terminal-bench" / "stateful-workspace-cutover"
TESTS = TASK / "tests" / "test_runtime.py"
BASELINE = TASK / "environment" / "workspace_runtime.py"
ORACLE = TASK / "solution" / "workspace_runtime.py"
RESULT = ROOT / "results" / "validation.json"


def run_case(name: str, artifact: Path) -> dict[str, Any]:
    environment = os.environ.copy()
    environment["WORKSPACE_RUNTIME_ARTIFACT"] = str(artifact)
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", str(TESTS)],
        cwd=ROOT.parents[3],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    lines = (completed.stdout + completed.stderr).splitlines()
    return {
        "name": name,
        "passed": completed.returncode == 0,
        "returncode": completed.returncode,
        "output_tail": lines[-12:],
    }


def mutate(source: str, old: str, new: str, *, name: str) -> str:
    count = source.count(old)
    if count != 1:
        raise RuntimeError(f"mutant {name}: expected one target, found {count}")
    return source.replace(old, new, 1)


def main() -> int:
    oracle_source = ORACLE.read_text()
    report: dict[str, Any] = {
        "schema_version": "stateful-workspace-cutover.validation.v1",
        "baseline": run_case("nop-buggy-starter", BASELINE),
        "oracle_runs": [
            run_case("oracle-1", ORACLE),
            run_case("oracle-2", ORACLE),
        ],
        "mutants": [],
    }
    mutations = {
        "split-lineage-recovery": (
            '"mode": "compat-local",\n                "database_path": str(self.source),',
            '"mode": "isolated",\n                "database_path": str(self.isolated),',
        ),
        "ignore-active-job": (
            'if self._active():\n            raise CutoverError("active_job_present")',
            'if False:\n            raise CutoverError("active_job_present")',
        ),
        "store-raw-token": (
            "digest = hashlib.sha256(token.encode()).hexdigest()",
            "digest = token",
        ),
        "skip-pullback-verification": (
            'if self.semantic_hash(temporary) != expected_hash:\n                raise CutoverError("pullback_hash_mismatch")',
            'if False and self.semantic_hash(temporary) != expected_hash:\n                raise CutoverError("pullback_hash_mismatch")',
        ),
        "overwrite-populated-head": (
            'if remote.get("head_revision") != 0 or snapshots != []:\n            raise CutoverError("remote_head_not_empty")',
            'if False:\n            raise CutoverError("remote_head_not_empty")',
        ),
        "count-only-semantic-hash": (
            'return hashlib.sha256(encoded).hexdigest()',
            'return str(sum(len(item.get("rows", [])) for item in table_documents))',
        ),
        "remove-remote-lock": (
            "fcntl.flock(stream.fileno(), fcntl.LOCK_EX)",
            "pass  # mutant removes the exclusive lock",
        ),
    }
    with tempfile.TemporaryDirectory() as directory:
        mutant_root = Path(directory)
        for name, (old, new) in mutations.items():
            mutant_path = mutant_root / f"{name}.py"
            mutant_path.write_text(mutate(oracle_source, old, new, name=name))
            outcome = run_case(name, mutant_path)
            outcome["killed"] = not outcome["passed"]
            report["mutants"].append(outcome)

    report["summary"] = {
        "baseline_rejected": not report["baseline"]["passed"],
        "oracle_deterministic_pass": all(run["passed"] for run in report["oracle_runs"]),
        "mutants_total": len(report["mutants"]),
        "mutants_killed": sum(1 for mutant in report["mutants"] if mutant["killed"]),
    }
    report["passed"] = (
        report["summary"]["baseline_rejected"]
        and report["summary"]["oracle_deterministic_pass"]
        and report["summary"]["mutants_killed"] == report["summary"]["mutants_total"]
    )
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    RESULT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(
        "Task validation: "
        f"{'PASS' if report['passed'] else 'FAIL'} "
        f"(baseline_rejected={report['summary']['baseline_rejected']}, "
        f"oracle_runs={len(report['oracle_runs'])}, "
        f"mutants={report['summary']['mutants_killed']}/{report['summary']['mutants_total']})"
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
