from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from .baselines import policy_guard_baseline
from .environment import OfflineSubmissionEnvironment
from .loaders import (
    load_crmarena_pro,
    load_gaia2_parquet,
    load_the_agent_company,
)
from .validation import validate_episode


def _loader(args):
    if args.source == "crmarena-pro":
        return load_crmarena_pro(
            args.path,
            source_revision=args.revision,
            split=args.split,
            limit=args.limit,
        )
    if args.source == "the-agent-company":
        return load_the_agent_company(
            args.path, source_revision=args.revision, limit=args.limit
        )
    return load_gaia2_parquet(
        args.path, source_revision=args.revision, limit=args.limit
    )


def command_inspect(args) -> int:
    episodes = list(_loader(args))
    payload = {
        "source": args.source,
        "path": str(Path(args.path).resolve()),
        "sha256": hashlib.sha256(Path(args.path).read_bytes()).hexdigest()
        if Path(args.path).is_file()
        else None,
        "episodes_decoded": len(episodes),
        "capability_levels": dict(
            sorted(Counter(str(item.capability_level) for item in episodes).items())
        ),
        "task_families": dict(
            sorted(Counter(item.task["family"] for item in episodes).items())
        ),
        "episode_ids": [item.episode_id for item in episodes[:3]],
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


def command_decode(args) -> int:
    episodes = list(_loader(args))
    failures = []
    for episode in episodes:
        failures.extend(
            {
                "episode_id": episode.episode_id,
                "message": message,
            }
            for message in validate_episode(episode, args.schema)
        )
    print(
        json.dumps(
            {
                "decoded": [episode.to_dict() for episode in episodes],
                "schema_failures": failures,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return int(bool(failures))


def command_baseline(args) -> int:
    episodes = list(_loader(args))
    env = OfflineSubmissionEnvironment(episodes)
    results = []
    for index, episode in enumerate(episodes):
        env.reset(index)
        action = policy_guard_baseline(episode)
        _, reward, done, info = env.step(action)
        results.append(
            {
                "episode_id": episode.episode_id,
                "action": action,
                "reward": reward,
                "done": done,
                "evaluation": info["evaluation"],
            }
        )
    print(
        json.dumps(
            {
                "setting": "local deterministic approximation; not upstream score",
                "episodes": len(results),
                "mean_reward": sum(item["reward"] for item in results) / len(results),
                "results": results,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


def _add_source_arguments(parser):
    parser.add_argument(
        "--source",
        required=True,
        choices=["crmarena-pro", "the-agent-company", "gaia2"],
    )
    parser.add_argument("--path", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--split", default="unknown")
    parser.add_argument("--limit", type=int)


def main() -> int:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(required=True)
    inspect_parser = subparsers.add_parser("inspect")
    _add_source_arguments(inspect_parser)
    inspect_parser.set_defaults(func=command_inspect)
    decode_parser = subparsers.add_parser("decode")
    _add_source_arguments(decode_parser)
    decode_parser.add_argument(
        "--schema",
        default="knowledge/lab/schemas/normalized-episode-v2.schema.json",
    )
    decode_parser.set_defaults(func=command_decode)
    baseline_parser = subparsers.add_parser("baseline")
    _add_source_arguments(baseline_parser)
    baseline_parser.set_defaults(func=command_baseline)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
