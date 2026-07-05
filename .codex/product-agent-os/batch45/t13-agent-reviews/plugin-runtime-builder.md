# B45-POSTQ4-T13 Plugin Runtime Builder Review

Task: `B45-POSTQ4-T13-STRICT_OUTPUT_SCHEMA_AND_HARNESS_HARDENING`

Result: read-only runtime implementation review. Files were not edited by the agent.

Recommendation: add a generic `codex_runtime_runner` model-output contract layer with strict `FINAL_JSON:` extraction, schema validation, no-op classification and pair classification. The parser must use `json.JSONDecoder().raw_decode`, not regex-based nested-brace extraction.

Test focus: invalid nested JSON strings, trailing content, missing required run fields, ignored probe/generated files, invalid-pair quarantine and reviewer blocking when `valid_pair_count < 8`.
