# AI, LLM and retrieval evals

Source status: repository_source / static_contract_review; DG06, 2026-11-15.

Owner: AI/eval owner + verification owner. Scope/version: repository `259977f3b257ba7fc0e932396f8963262bd327ad`. Update for model, route, prompt, retrieval or eval contract changes. Rubrics and thresholds belong to [EVALS.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/EVALS.md); check selection belongs to [TEST.md](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/TEST.md). Links below do not imply a current provider run.

## Selection and comparison

For a material AI/RAG, prompt, model, tool or routing change, record the baseline before changing it, cases and expected behavior, then compare the candidate on comparable inputs. Include typical, edge, adversarial and regression cases according to risk; consider privacy, tool failures, unsupported claims, quality and available cost/latency data. Freeze relevant corpus, prompts, tools and permissions for a model comparison; vary model, effort and prompt separately where practical. Set thresholds, budget, stop conditions and independent review before the run. Unknown tokens/cost/latency are not zero.

| Layer | What it checks | What it does not prove |
| --- | --- | --- |
| [Behavioral fixture and transcript evals](../product-agent-os/behavioral-evals.md), [runner tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_transcript_session_evals.py) | Deterministic expected/forbidden terms, structure, routing, privacy and fixture contracts. | Semantic evaluation of all real responses, model quality or mass applicability. |
| [Retrieval evaluation](../ai/rag/evaluation.md), [quality tests](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_project_graph_search_quality.py) | Within cases and thresholds, pointer relevance/ranking and false positives. | Grounding of the final answer, complete coverage of a real project or live provider quality. |
| Provider gate / actual provider eval | A gate checks supplied data and conditions; an actual run requires separate authority, data, budget and trace. | A ready gate, proposal or configured model does not prove that a call occurred or the selected model is accessible. |

Full unittest discovery already includes fixture/transcript evals; the same set need not be rerun without changed relevant inputs or a specific reason. For a separate fixture set TEST points to `run_fixture_eval.py --summary`. Record failures and denominators, not only aggregates. If a mandatory baseline or access is missing, retain `not_verified`/`blocked`, not promotion. According to [LLM budgets](../ai/llm/budgets-and-observability.md), current duration/token/cost observability may be unavailable; F11/F15 and provider evaluation have separate owners and status.

Test sources are traceability: [fixture runner](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_fixture_eval_runner.py), [provider gate](https://github.com/alexroadcaster/product-agent-os/blob/259977f3b257ba7fc0e932396f8963262bd327ad/tests/product_agent_os/test_project_graph_embedding_provider.py). This page does not change rubrics, thresholds or authority.
