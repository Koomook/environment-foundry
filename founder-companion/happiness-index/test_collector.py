import tempfile
import unittest
import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import collector


class CollectorTests(unittest.TestCase):
    def test_parse_time_normalizes_utc(self):
        result = collector.parse_time("2026-07-27T17:00:00+09:00")
        self.assertEqual(result, datetime(2026, 7, 27, 8, 0, tzinfo=UTC))

    def test_dimension_coverage_does_not_infer_family_or_cash(self):
        sources = {
            "monologue": {"count": 3},
            "calendar": {"count": 8},
            "health": {"status": "missing-current-measurement"},
            "codex": {"active_session_files": 2},
            "git": {"total_commits": 1},
        }
        result = collector.dimension_coverage(sources)
        self.assertEqual(result["family_presence_stewardship"]["status"], "proxy-only")
        self.assertEqual(result["cash_safety_freedom"]["coverage"], 0.0)
        self.assertEqual(result["health_usable_capacity"]["coverage"], 0.0)

    def test_persist_keeps_immutable_snapshot_and_receipt(self):
        snapshot = {
            "generated_at": "2026-07-27T08:00:00Z",
            "calculation": {
                "score_status": "baseline-anchor-only",
                "confidence": 0.25,
            },
        }
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(collector, "SNAPSHOT_ROOT", Path(directory)):
                path, digest = collector.persist_snapshot(snapshot)
                self.assertTrue(path.exists())
                self.assertEqual(len(digest), 64)
                self.assertTrue((Path(directory) / "latest.json").exists())
                self.assertTrue((Path(directory) / "baseline.json").exists())

    def test_deep_thought_context_detects_source_drift_without_copying_content(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.md"
            source.write_text("private context", encoding="utf-8")
            digest = hashlib.sha256(source.read_bytes()).hexdigest()
            registry = root / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "sources": [
                            {
                                "id": "direct-context",
                                "type": "direct-founder-input",
                                "path": str(source),
                                "sha256": digest,
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            with patch.object(collector, "DEEP_THOUGHT_REGISTRY", registry):
                observed = collector.collect_deep_thought_context()
                self.assertEqual(observed["status"], "observed")
                self.assertNotIn("private context", json.dumps(observed))
                source.write_text("changed context", encoding="utf-8")
                changed = collector.collect_deep_thought_context()
                self.assertEqual(changed["status"], "review-required")
                self.assertEqual(changed["changed_sources"], ["direct-context"])


if __name__ == "__main__":
    unittest.main()
