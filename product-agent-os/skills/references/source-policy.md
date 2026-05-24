# Product-Agent OS Source Policy

Use this reference when a skill depends on current facts, external documentation, security claims, or product behavior.

Rules:

- Official OpenAI documentation is source of truth for Codex, plugins, skills, subagents, hooks, approvals, MCP, Agents SDK, and models.
- Context7 is official only when the underlying source is official.
- Community claims are intake material until marked with `trust_level` and `verification_status`.
- Memory and chat history are recall layers, not source of truth.
- Do not store secrets, tokens, credentials, private keys, private customer data, or raw private chat logs.
- Separate supported facts, assumptions, unsupported claims, and missing context.
- For source drift risk, refresh the source before making durable rules.
- Do not turn unsupported community claims into Product-Agent OS rules without verification status.
