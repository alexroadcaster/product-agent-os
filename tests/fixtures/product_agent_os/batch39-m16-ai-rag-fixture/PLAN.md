# Plan

1. Keep the AI behavior synthetic and local.
2. Use `prompts/answer-policy.md` as the prompt contract signal.
3. Use `rag/corpus.jsonl` and `rag/retrieval-config.json` as retrieval signals.
4. Use `evals/rag-eval-cases.jsonl` and `evals/eval-run-report.json` as static eval evidence.
5. Keep all model/provider behavior as `not_run_approval_required`.

