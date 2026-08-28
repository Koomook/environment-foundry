#!/usr/bin/env python3
"""Small operator CLI for exploring the synthetic workspace runtime."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workspace_runtime import CutoverError, WorkspaceRuntime


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=("status", "recover", "cutover"))
    parser.add_argument("--root", default="/app/state")
    args = parser.parse_args()
    runtime = WorkspaceRuntime(Path(args.root))
    try:
        result = getattr(runtime, args.command)()
    except CutoverError as error:
        print(json.dumps({"ok": False, "error": error.code}, sort_keys=True))
        return 2
    print(json.dumps({"ok": True, "result": result}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

