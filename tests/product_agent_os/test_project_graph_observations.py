import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.project_graph_observations import (  # noqa: E402
    build_observation_record,
    diff_observation_lineage,
)


class ProjectGraphObservationsTest(unittest.TestCase):
    def test_observation_record_is_deterministic_redacted_and_span_based(self):
        first = build_observation_record(
            scan_id="scan-1",
            relative_path="app/main.py",
            span={"start_line": 1, "end_line": 3},
            fingerprint="sha256:" + "b" * 64,
            extractor="file_inventory",
            confidence="verified",
            redaction_status="redacted",
            subject_id="file:app/main.py",
        )
        second = build_observation_record(
            scan_id="scan-1",
            relative_path="app/main.py",
            span={"start_line": 1, "end_line": 3},
            fingerprint="sha256:" + "b" * 64,
            extractor="file_inventory",
            confidence="verified",
            redaction_status="redacted",
            subject_id="file:app/main.py",
        )

        self.assertEqual(first, second)
        self.assertEqual(first["relative_path"], "app/main.py")
        self.assertEqual(first["span"], {"start_line": 1, "end_line": 3})
        self.assertEqual(first["raw_source_status"], "excluded")
        self.assertNotIn("C:\\Users", str(first))

    def test_diff_observation_lineage_invalidates_removed_and_supersedes_changed_edges(self):
        previous = {
            "edges": [
                {
                    "id": "edge:a-b",
                    "source": "node:a",
                    "target": "node:b",
                    "type": "imports",
                    "observation_ids": ["obs:old"],
                    "fingerprint": "sha256:" + "a" * 64,
                },
                {
                    "id": "edge:a-c",
                    "source": "node:a",
                    "target": "node:c",
                    "type": "calls",
                    "observation_ids": ["obs:removed"],
                    "fingerprint": "sha256:" + "c" * 64,
                },
            ]
        }
        current = {
            "edges": [
                {
                    "id": "edge:a-b",
                    "source": "node:a",
                    "target": "node:b",
                    "type": "imports",
                    "observation_ids": ["obs:new"],
                    "fingerprint": "sha256:" + "b" * 64,
                },
                {
                    "id": "edge:a-d",
                    "source": "node:a",
                    "target": "node:d",
                    "type": "imports",
                    "observation_ids": ["obs:added"],
                    "fingerprint": "sha256:" + "d" * 64,
                },
            ]
        }

        delta = diff_observation_lineage(previous, current, scan_id="scan-2")

        self.assertEqual(delta["status"], "changed")
        self.assertEqual([item["edge_id"] for item in delta["invalidated_edges"]], ["edge:a-c"])
        self.assertEqual([item["edge_id"] for item in delta["superseded_edges"]], ["edge:a-b"])
        self.assertEqual([item["edge_id"] for item in delta["new_edges"]], ["edge:a-d"])


if __name__ == "__main__":
    unittest.main()
