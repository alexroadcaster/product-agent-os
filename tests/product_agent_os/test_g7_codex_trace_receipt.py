"""Local positive and negative controls for the G7 Codex trace receipt."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "plugins/product-agent-os/scripts"))

from g7_codex_trace_receipt import PREFLIGHT_PROMPT, TraceReceiptError, build_trace_receipt, run_preflight

PROMPT = "Synthetic G7 preflight input."
CONTEXT = "synthetic ambient context that must not appear in the receipt"
MODEL = "gpt-6.1-sol"
THREAD = "synthetic-thread"
TURN = "synthetic-turn"


def message(role, text, item_id):
    return {"type": "message", "role": role, "id": item_id,
            "content": [{"type": "input_text", "text": text}]}


class G7TraceReceiptTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.trace_root = Path(temporary.name)
        self.bundle = self.trace_root / f"trace-synthetic-trace-{THREAD}"
        self.payload_dir = self.bundle / "payloads"
        self.payload_dir.mkdir(parents=True)
        self.request = {"model": MODEL, "reasoning": {"effort": "medium"}, "tools": [],
                        "input": [message("developer", CONTEXT, "dev-1"),
                                  message("user", PROMPT, "user-1")]}
        request_ref = {"path": "payloads/1.json", "kind": {"type": "inference_request"},
                       "raw_payload_id": "raw_payload:1"}
        response_ref = {"path": "payloads/2.json", "kind": {"type": "inference_response"},
                        "raw_payload_id": "raw_payload:2"}
        self.events = [
            {"type": "rollout_started", "trace_id": "synthetic-trace", "root_thread_id": THREAD},
            {"type": "thread_started", "thread_id": THREAD},
            {"type": "codex_turn_started", "thread_id": THREAD, "codex_turn_id": TURN},
            {"type": "inference_started", "inference_call_id": "inference-1", "thread_id": THREAD,
             "codex_turn_id": TURN, "model": MODEL, "provider_name": "openai",
             "request_payload": request_ref},
            {"type": "inference_completed", "inference_call_id": "inference-1",
             "response_id": "response-1", "response_payload": response_ref},
            {"type": "codex_turn_ended", "codex_turn_id": TURN, "status": "completed"},
            {"type": "recording_completed"},
        ]
        self.response = {"response_id": "response-1",
                         "output_items": [{"type": "message", "role": "assistant",
                                           "content": [{"type": "output_text", "text": "ready"}]}]}
        self._write_json(self.bundle / "manifest.json",
                         {"schema_version": 2, "trace_id": "synthetic-trace", "rollout_id": THREAD,
                          "root_thread_id": THREAD, "raw_event_log": "trace.jsonl",
                          "payloads_dir": "payloads"})

    def _write_json(self, path, payload):
        path.write_text(json.dumps(payload), encoding="utf-8")

    def _write_trace(self):
        self._write_json(self.payload_dir / "1.json", self.request)
        self._write_json(self.payload_dir / "2.json", self.response)
        rows = [json.dumps({"schema_version": 2, "rollout_id": THREAD, "seq": seq,
                            "thread_id": THREAD, "codex_turn_id": TURN, "payload": payload})
                for seq, payload in enumerate(self.events, 1)]
        (self.bundle / "trace.jsonl").write_text("\n".join(rows) + "\n", encoding="utf-8")

    def _receipt(self, **kwargs):
        self._write_trace()
        return build_trace_receipt(self.trace_root, expected_prompt=PROMPT, **kwargs)

    def test_complete_request_retains_hashes_without_context_or_prompt(self):
        receipt = self._receipt()
        self.assertEqual(receipt["status"], "passed")
        self.assertEqual(receipt["observed_tool_count"], 0)
        self.assertEqual(receipt["observed_model"], MODEL)
        self.assertEqual(receipt["observed_effort"], "medium")
        serialized = json.dumps(receipt)
        self.assertNotIn(CONTEXT, serialized)
        self.assertNotIn(PROMPT, serialized)
        self.assertNotIn("response-1", serialized)
        self.request["input"][0]["id"] = "new-transport-id"
        same_context = self._receipt()
        self.assertEqual(same_context["common_context_sha256"], receipt["common_context_sha256"])
        self.request["input"][0]["content"][0]["text"] = "different ambient context"
        self.assertNotEqual(self._receipt()["common_context_sha256"], receipt["common_context_sha256"])

    def test_rejects_top_level_and_responses_lite_tools(self):
        for location in ("top_level", "input"):
            with self.subTest(location=location):
                self.request["tools"] = [{"type": "function", "name": "apply_patch"}]
                if location == "input":
                    self.request["input"].insert(0, {"type": "additional_tools", "role": "developer",
                                                     "tools": self.request.pop("tools")})
                receipt = self._receipt()
                self.assertEqual(receipt["status"], "blocked")
                self.assertEqual(receipt["observed_tool_count"], 1)
                self.assertIn("tools_present", receipt["reasons"])

    def test_diagnostic_inventory_flattens_namespaces_without_raw_context(self):
        self.request["tools"] = [{"type": "namespace", "name": "functions", "tools": [
            {"type": "function", "name": "apply_patch"},
            {"type": "function", "name": "private_customer_tool"}]}]
        receipt = self._receipt()
        self.assertEqual(receipt["observed_tool_count"], 1)
        self.assertEqual(receipt["builtin_tool_names"], ["apply_patch"])
        self.assertEqual(receipt["leaf_tool_count"], 2)
        self.assertIn("private_customer_tool", receipt["tool_identifiers"])
        self.assertNotIn(CONTEXT, json.dumps(receipt))

    def test_builtin_provider_display_name_is_not_a_provider_change(self):
        self.events[3]["provider_name"] = "OpenAI"
        self.assertEqual(self._receipt()["status"], "passed")
        self.events[3]["provider_name"] = "unknown-provider"
        self.assertIn("provider_mismatch", self._receipt()["reasons"])

    def test_normalizes_only_bound_startup_marker_and_keeps_other_semantics(self):
        import hashlib
        marker = hashlib.sha256(THREAD.encode()).hexdigest()
        self.request["input"][0]["content"][0]["text"] = (
            "Product-Agent OS startup context: control-plane present=AGENTS.md; missing=none. "
            "State marker=.codex/product-agent-os/lifecycle-state." + marker + ".json; lifecycle_state=missing")
        receipt = self._receipt()
        self.assertNotEqual(receipt["common_context_sha256"], receipt["normalized_common_context_sha256"])
        self.request["input"][0]["content"][0]["text"] += " safety requirement changed"
        self.assertNotEqual(self._receipt()["normalized_common_context_sha256"], receipt["normalized_common_context_sha256"])

    def test_candidate_is_bound_to_trace_output_and_not_returned_when_blocked(self):
        import hashlib
        receipt = self._receipt(include_output=True)
        self.assertEqual(receipt['candidate'], 'ready')
        self.assertEqual(receipt['candidate_sha256'], hashlib.sha256(b'ready').hexdigest())
        self.request['tools'] = [{'type':'function','name':'apply_patch'}]
        self.assertNotIn('candidate', self._receipt(include_output=True))

    def test_sequence_stops_on_context_drift_and_preserves_attempts(self):
        import copy
        import run_g7_attested_comparison as runner
        design = json.loads((ROOT/'docs/superpowers/specs/paos-aud-g7-attested-design.json').read_text(encoding='utf-8'))
        design['frozen_files'] = {}
        design['output_directory'] = 'output'
        design_path = self.trace_root/'design.json'
        self._write_json(design_path, design)
        observed = dict(status='passed', candidate='def label(value, prefix=""):\n    return prefix + str(value)\n', normalized_common_context_sha256='a'*64)
        with (patch.object(runner, 'ROOT', self.trace_root), patch.object(runner, 'DESIGN', design_path),
              patch.object(runner, 'run_preflight', side_effect=[copy.deepcopy(observed),dict(observed,normalized_common_context_sha256='b'*64)])):
            result = runner.run(Path('unused.exe'))
            self.assertFalse(result['comparison_eligible'])
            self.assertEqual(len(result['calls']), 2)
            self.assertEqual(result['calls'][1]['status'], 'context_mismatch')
            with self.assertRaisesRegex(ValueError, 'already recorded'):
                runner.run(Path('unused.exe'))

    def test_transport_identity_normalization_preserves_content_and_provenance(self):
        from g7_codex_trace_receipt import common_context_receipt
        def context(identity, provenance):
            item = message('user', 'unchanged context', 'ignored')
            item['internal_chat_message_metadata_passthrough'] = dict(turn_id=identity, create_time=1.25, content_item_kinds=[provenance])
            return [item]
        first = common_context_receipt(None, context('one', 'fixed'), THREAD)
        second = common_context_receipt(None, context('two', 'fixed'), THREAD)
        self.assertEqual(first['normalized_common_context_sha256'],second['normalized_common_context_sha256'])
        changed = common_context_receipt(None, context('two', 'different'), THREAD)
        self.assertNotEqual(first['normalized_common_context_sha256'],changed['normalized_common_context_sha256'])
        changed_content = context('two', 'fixed')
        changed_content[0]['content'][0]['text'] = THREAD
        self.assertNotEqual(first['normalized_common_context_sha256'], common_context_receipt(None, changed_content, THREAD)['normalized_common_context_sha256'])

    def test_lite_without_added_tools_is_empty_for_complete_request(self):
        del self.request["tools"]
        self.request["type"] = "response.create"
        self.assertEqual(self._receipt()["status"], "passed")

    def test_rejects_hidden_literals_and_does_not_retain_them(self):
        marker = "hidden/ORACLE.py"
        self.request["input"][0]["content"][0]["text"] = "hidden\\oracle.py"
        receipt = self._receipt(forbidden_texts=(marker,))
        self.assertIn("hidden_oracle_marker", receipt["reasons"])
        self.assertNotIn("oracle.py", json.dumps(receipt).lower())

    def test_refuses_continuation_and_incomplete_or_unbound_trace(self):
        self.request["previous_response_id"] = "unknown-previous"
        with self.assertRaisesRegex(TraceReceiptError, "incremental_request"):
            self._receipt()
        del self.request["previous_response_id"]
        self.events.pop()
        with self.assertRaisesRegex(TraceReceiptError, "incomplete_recording"):
            self._receipt()
        self.events.append({"type": "recording_completed"})
        self.events[4]["inference_call_id"] = "unbound"
        with self.assertRaisesRegex(TraceReceiptError, "inference_binding"):
            self._receipt()

    def test_refuses_payload_escape_and_missing_raw_file(self):
        ref = self.events[3]["request_payload"]
        ref["path"] = "../other.json"
        with self.assertRaisesRegex(TraceReceiptError, "invalid_payload_reference"):
            self._receipt()
        ref["path"] = "payloads/3.json"
        ref["raw_payload_id"] = "raw_payload:3"
        with self.assertRaisesRegex(TraceReceiptError, "missing_trace_file"):
            self._receipt()

    def test_tool_attempt_and_model_or_effort_mismatch_block(self):
        self.events.insert(4, {"type": "tool_call_started", "tool_call_id": "tool-1"})
        self.request["model"] = "untrusted-model-field"
        self.request["reasoning"]["effort"] = "wrong-effort"
        receipt = self._receipt()
        self.assertEqual(receipt["status"], "blocked")
        self.assertIn("tool_activity", receipt["reasons"])
        self.assertIn("model_mismatch", receipt["reasons"])
        self.assertIn("effort_mismatch", receipt["reasons"])
        self.assertNotIn("untrusted-model-field", json.dumps(receipt))

    def test_final_response_tool_item_blocks_even_without_dispatch_event(self):
        self.response["output_items"].append({"type": "function_call", "name": "read"})
        receipt = self._receipt()
        self.assertIn("tool_activity", receipt["reasons"])

    def test_wrapper_discards_failed_raw_trace_and_captures_no_diagnostics(self):
        reports = self.trace_root / ".docs-tools/reports"
        reports.mkdir(parents=True)
        executable = self.trace_root / "codex.exe"
        executable.write_bytes(b"synthetic")
        scratch = []

        def run(argv, **kwargs):
            if argv[1:] == ["--version"]:
                return subprocess.CompletedProcess(argv, 0, stdout=b"codex-cli 0.167.0\n")
            if argv[1:] == ["login", "status"]:
                return subprocess.CompletedProcess(argv, 0, stdout=b"", stderr=b"Logged in using ChatGPT\n")
            self.assertEqual(argv[1], "exec")
            self.assertEqual(kwargs["input"], PREFLIGHT_PROMPT.encode())
            self.assertEqual(kwargs["timeout"], 180)
            self.assertIn("--ephemeral", argv)
            self.assertIn("plugins.unified-computer-use@openai-bundled.mcp_servers.cua_repl.enabled=false", argv)
            self.assertIn("mcp_servers.example.enabled=false", argv)
            self.assertNotIn("--ignore-rules", argv)
            self.assertNotIn("features.hooks=false", argv)
            folder = Path(kwargs["env"]["CODEX_ROLLOUT_TRACE_ROOT"])
            self.assertEqual(folder.parent, reports)
            scratch.append(folder)
            trace_bundle = folder / "trace-private"
            trace_bundle.mkdir()
            (trace_bundle / "trace.jsonl").write_text(
                json.dumps({"payload": {"type": "inference_started", "private": CONTEXT}}) + "\n",
                encoding="utf-8",
            )
            return subprocess.CompletedProcess(argv, 1, stderr=f"Access is denied: {CONTEXT}".encode())

        with (patch.dict(os.environ, {"OPENAI_API_KEY": "", "CODEX_API_KEY": "", "AZURE_OPENAI_API_KEY": ""}),
              patch("g7_codex_trace_receipt._oracle_markers", return_value=("known hidden marker",)),
              patch("g7_codex_trace_receipt.subprocess.run", side_effect=run) as process):
            receipt = run_preflight(self.trace_root, executable, ("example",))
        self.assertEqual(process.call_count, 3)
        self.assertEqual(len(scratch), 1)
        self.assertFalse(scratch[0].exists())
        self.assertEqual(receipt["reasons"], ["codex_preflight_exit_nonzero"])
        self.assertEqual(receipt["exit_code"], 1)
        self.assertEqual(receipt["inference_starts_observed"], 1)
        self.assertTrue(receipt["permission_denied"])
        self.assertFalse(receipt["configuration_error"])
        self.assertNotIn(CONTEXT, json.dumps(receipt))
