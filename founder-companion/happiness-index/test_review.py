import json
import tempfile
import unittest
from pathlib import Path

import review


class ReviewTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.candidates = self.root / "candidates.json"
        self.state = self.root / "state.json"
        self.events = self.root / "events.jsonl"
        self.candidates.write_text(
            json.dumps(
                {
                    "review_order": ["D1", "D2"],
                    "items": [
                        {"id": "D1", "title": "one"},
                        {"id": "D2", "title": "two"},
                    ],
                }
            )
        )
        self.state.write_text(
            json.dumps(
                {
                    "current_item": "D1",
                    "completed": 0,
                    "total": 2,
                    "items": {},
                }
            )
        )

    def tearDown(self):
        self.tempdir.cleanup()

    def test_record_is_append_only_and_advances(self):
        event = review.append_event(
            "D1",
            "CONFIRM",
            "meaning",
            "codex:test",
            "turn-1",
            candidates_path=self.candidates,
            state_path=self.state,
            events_path=self.events,
        )
        self.assertEqual(event["disposition"], "CONFIRM")
        state = json.loads(self.state.read_text())
        self.assertEqual(state["current_item"], "D2")
        self.assertEqual(state["completed"], 1)

    def test_idempotency_returns_same_event(self):
        first = review.append_event(
            "D1",
            "PARK",
            "later",
            "codex:test",
            "turn-2",
            candidates_path=self.candidates,
            state_path=self.state,
            events_path=self.events,
        )
        second = review.append_event(
            "D2",
            "CONFIRM",
            "ignored",
            "codex:test",
            "turn-2",
            candidates_path=self.candidates,
            state_path=self.state,
            events_path=self.events,
        )
        self.assertEqual(first["event_id"], second["event_id"])
        self.assertEqual(len(self.events.read_text().splitlines()), 1)

    def test_rejects_out_of_order(self):
        with self.assertRaises(ValueError):
            review.append_event(
                "D2",
                "CONFIRM",
                "meaning",
                "codex:test",
                "turn-3",
                candidates_path=self.candidates,
                state_path=self.state,
                events_path=self.events,
            )


if __name__ == "__main__":
    unittest.main()
