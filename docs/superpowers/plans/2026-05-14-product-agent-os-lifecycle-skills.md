---
title: "Archive - Product-Agent OS Lifecycle Skills Implementation Plan"
---

# Archive - Product-Agent OS Lifecycle Skills Implementation Plan {#product-agent-os-lifecycle-skills-implementation-plan}

> Историческая запись. Даты и verdicts ниже относятся к тому запуску; для текущего поведения используйте актуальные руководства.

Source status: `official + experiment`

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build packaged lifecycle skills for the `product-agent-os` Codex plugin without generating project infrastructure yet.

**Architecture:** This plan implements Track 2 from the [Product-Agent OS lifecycle skills design](../specs/2026-05-14-product-agent-os-lifecycle-skills-design.md). It adds concise `SKILL.md` packages, shared lifecycle references, UI metadata, and static validation tests that enforce routing, boundaries, source policy, and safety language.

**Tech Stack:** Codex skill package layout, Markdown, YAML-like metadata files, Python 3 standard library, `unittest`, `pathlib`, `re`.

---

## Scope

This plan covers only **Lifecycle skills**:

- packaged skill folders under `plugins/product-agent-os/skills/`;
- shared reference files under `plugins/product-agent-os/skills/references/`;
- `agents/openai.yaml` metadata for each lifecycle skill;
- structure and policy tests for skill packages;
- MkDocs navigation for this plan.

It intentionally does not create project templates, `.codex/agents/*.toml`, active hooks, workflow files, automations, MCP servers, or an Agents SDK runner. Those remain Track 3 and Track 4 work.

## File Structure

Create these files:

- `tests/product_agent_os/test_lifecycle_skills.py` - validates skill package structure, routing coverage, metadata, references, and safety boundaries.
- `plugins/product-agent-os/skills/references/lifecycle-states.md` - lifecycle order and transition rules.
- `plugins/product-agent-os/skills/references/handoff-contract.md` - handoff payload fields and rejection rules.
- `plugins/product-agent-os/skills/references/source-policy.md` - source, freshness, Context7, and secret policy.
- `plugins/product-agent-os/skills/references/complexity-routing.md` - profile-specific routing depth.
- `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`
- `plugins/product-agent-os/skills/project-lifecycle-orchestrator/agents/openai.yaml`
- `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`
- `plugins/product-agent-os/skills/workspace-discovery-auditor/agents/openai.yaml`
- `plugins/product-agent-os/skills/requirements-author/SKILL.md`
- `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- `plugins/product-agent-os/skills/implementation-planner/SKILL.md`
- `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`
- `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`
- `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`
- `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`
- `plugins/product-agent-os/skills/test-eval-designer/agents/openai.yaml`
- `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`
- `plugins/product-agent-os/skills/risk-reviewer/agents/openai.yaml`
- `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`
- `plugins/product-agent-os/skills/pr-release-operator/agents/openai.yaml`
- `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`
- `plugins/product-agent-os/skills/learning-loop-maintainer/agents/openai.yaml`
- `plugins/product-agent-os/skills/automation-promoter/SKILL.md`
- `plugins/product-agent-os/skills/automation-promoter/agents/openai.yaml`

Modify these files:

- `mkdocs.yml` - add this plan to navigation.

## Skill Inventory

Every skill uses the same required headings:

- `## Trigger`
- `## Boundaries`
- `## Inputs`
- `## Process`
- `## Outputs`
- `## Verification`
- `## Failure Modes`
- `## Final Response Contract`

Every `agents/openai.yaml` uses:

```yaml
interface:
  display_name: "..."
  short_description: "..."
  default_prompt: "Use $skill-name to ..."
policy:
  allow_implicit_invocation: false
```

## Task 1: Lifecycle Skill Validation Tests

**Files:**
- Create: `tests/product_agent_os/test_lifecycle_skills.py`

- [ ] **Step 1: Write the failing lifecycle skill tests**

Create `tests/product_agent_os/test_lifecycle_skills.py`:

```python
import re
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "plugins" / "product-agent-os" / "scripts"
SKILLS = ROOT / "plugins" / "product-agent-os" / "skills"
sys.path.insert(0, str(SCRIPTS))

from product_agent_os.contracts import LIFECYCLE_STATES  # noqa: E402


SKILL_NAMES = [
    "project-lifecycle-orchestrator",
    "workspace-discovery-auditor",
    "requirements-author",
    "implementation-planner",
    "agent-team-designer",
    "test-eval-designer",
    "risk-reviewer",
    "pr-release-operator",
    "learning-loop-maintainer",
    "automation-promoter",
]

REQUIRED_HEADINGS = [
    "## Trigger",
    "## Boundaries",
    "## Inputs",
    "## Process",
    "## Outputs",
    "## Verification",
    "## Failure Modes",
    "## Final Response Contract",
]

REFERENCES = [
    "lifecycle-states.md",
    "handoff-contract.md",
    "source-policy.md",
    "complexity-routing.md",
]

REFERENCE_TERMS = {
    "lifecycle-states.md": ["uninitialized", "maintenance", "Do not skip"],
    "handoff-contract.md": ["verification_evidence", "unsupported_claims", "stop_reason"],
    "source-policy.md": ["Official OpenAI documentation", "Context7", "Do not store secrets"],
    "complexity-routing.md": ["guided-small", "enterprise-governed", "autonomous-maintenance"],
}

REQUIRED_SKILL_LINKS = [
    "../references/lifecycle-states.md",
    "../references/handoff-contract.md",
    "../references/source-policy.md",
    "../references/complexity-routing.md",
]

ROUTING = {
    "uninitialized": "workspace-discovery-auditor",
    "infrastructure_planned": "requirements-author",
    "requirements_ready": "implementation-planner",
    "plan_ready": "agent-team-designer",
    "team_ready": "test-eval-designer",
    "build_active": "risk-reviewer",
    "quality_gate": "risk-reviewer",
    "review_ready": "pr-release-operator",
    "release_ready": "learning-loop-maintainer",
    "learning_ready": "automation-promoter",
    "maintenance": "project-lifecycle-orchestrator",
}

MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((?:<)?([^)>]+)(?:>)?\)")
REFERENCE_LINK_RE = re.compile(r"^\.\./references/[^/]+\.md$")

PERMISSIVE_PREFIX = r"(?:can|may|should|allowed to|is permitted to|will|must)"
FORBIDDEN_PERMISSIVE_PATTERNS = [
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write)\s+\.codex/agents\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:install|enable)\s+hooks\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|activate|start)\s+(?:active\s+)?automation\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|activate|start)\s+recurring\s+automation\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:mutate|change|modify|edit)\s+(?:global\s+)?(?:codex\s+)?config\b",
    rf"\b{PERMISSIVE_PREFIX}\s+store\s+secrets\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write|generate|modify)\s+project\s+templates\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|write|generate|modify)\s+workflow\s+files\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|run|call|connect to|use)\s+mcp\s+servers\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:create|run|use)\s+(?:an?\s+)?agents\s+sdk\s+runner\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:run|execute|perform)\s+destructive\s+commands\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:write|store|modify|use)\s+user-level\s+memory\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:call|modify|write to|connect to|use)\s+external\s+systems\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:perform|make|do)\s+external\s+writes\b",
    rf"\b{PERMISSIVE_PREFIX}\s+install\s+external\s+dependencies\b",
    rf"\b{PERMISSIVE_PREFIX}\s+(?:use\s+)?network\s+access\b",
]

NEGATIVE_PREFIX = r"(?:do not|never|must not|cannot|forbidden to|not permitted to)"

SECRET_BOUNDARY_PATTERNS = [rf"\b{NEGATIVE_PREFIX}\s+store\s+secrets\b"]
AUTOMATION_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+(?:create|activate|start)\s+(?:active\s+)?automation\b",
]
CONFIG_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+(?:mutate|change)\s+global\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+modify\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+edit\s+project\s+config\b",
    rf"\b{NEGATIVE_PREFIX}\s+change\s+global\s+codex\s+config\b",
]
EVIDENCE_BOUNDARY_PATTERNS = [
    rf"\b{NEGATIVE_PREFIX}\s+claim\b",
    r"\bwithout\s+evidence\b",
]


class LifecycleSkillsTest(unittest.TestCase):
    def test_required_skill_packages_exist(self):
        for name in SKILL_NAMES:
            with self.subTest(name=name):
                self.assertTrue((SKILLS / name / "SKILL.md").exists(), f"{name} must include SKILL.md")
                self.assertTrue((SKILLS / name / "agents" / "openai.yaml").exists(), f"{name} must include agents/openai.yaml")

    def test_skill_frontmatter_and_required_headings(self):
        for name in SKILL_NAMES:
            text = self._skill_text(name)
            with self.subTest(name=name):
                self._assert_frontmatter_has_only_name_and_description(name, text)
                self.assertRegex(text, r"^---\nname: " + re.escape(name) + r"\ndescription: .+\n---")
                self.assertRegex(text, r"(?m)^# .+")
                for heading in REQUIRED_HEADINGS:
                    self.assertIn(heading, text)

    def test_skill_metadata_disables_implicit_invocation(self):
        for name in SKILL_NAMES:
            metadata = (SKILLS / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
            with self.subTest(name=name):
                self.assertIn("interface:", metadata)
                self.assertIn("display_name:", metadata)
                self.assertIn("short_description:", metadata)
                self.assertIn("default_prompt:", metadata)
                self.assertIn(f"Use ${name}", metadata)
                self.assertIn("allow_implicit_invocation: false", metadata)

    def test_reference_files_exist_and_are_linked(self):
        for reference in REFERENCES:
            with self.subTest(reference=reference):
                path = SKILLS / "references" / reference
                self.assertTrue(path.exists(), f"{reference} must exist")
                text = path.read_text(encoding="utf-8")
                self.assertIn("Product-Agent OS", text)
                for term in REFERENCE_TERMS[reference]:
                    self.assertIn(term, text)

        for name in SKILL_NAMES:
            text = self._skill_text(name)
            with self.subTest(name=name):
                for link in REQUIRED_SKILL_LINKS:
                    self.assertIn(link, text)
                self._assert_reference_links_resolve(name, text)

    def test_orchestrator_routing_covers_all_lifecycle_states(self):
        self.assertEqual(set(ROUTING), set(LIFECYCLE_STATES))
        text = self._skill_text("project-lifecycle-orchestrator")
        for state, skill in ROUTING.items():
            with self.subTest(state=state):
                self.assertIn(state, text)
                self.assertIn(skill, text)

    def test_skills_state_track_two_boundaries(self):
        for name in SKILL_NAMES:
            text = self._skill_text(name).lower()
            with self.subTest(name=name):
                self.assertIn("track 2", text)
                self.assertIn("staged", text)
                self._assert_negative_boundary(name, text, SECRET_BOUNDARY_PATTERNS, "secret storage")
                self._assert_negative_boundary(name, text, AUTOMATION_BOUNDARY_PATTERNS, "active automation creation")
                self._assert_negative_boundary(name, text, CONFIG_BOUNDARY_PATTERNS, "config mutation")
                self._assert_negative_boundary(name, text, EVIDENCE_BOUNDARY_PATTERNS, "verification evidence claims")
                self.assertIn("approval", text)
                for pattern in FORBIDDEN_PERMISSIVE_PATTERNS:
                    self.assertNotRegex(text, pattern)

    def test_automation_skill_is_candidate_only(self):
        text = self._skill_text("automation-promoter").lower()
        self.assertIn("candidate_only", text)
        self.assertIn("manual stability evidence", text)

    def _skill_text(self, name: str) -> str:
        path = SKILLS / name / "SKILL.md"
        self.assertTrue(path.exists(), f"{name} must include SKILL.md")
        return path.read_text(encoding="utf-8")

    def _assert_frontmatter_has_only_name_and_description(self, name: str, text: str) -> None:
        match = re.match(r"^---\n(?P<frontmatter>.*?)\n---", text, re.DOTALL)
        self.assertIsNotNone(match, f"{name} must start with frontmatter")
        lines = [line.strip() for line in match.group("frontmatter").splitlines() if line.strip()]
        self.assertEqual(2, len(lines), f"{name} frontmatter must have only two keys")
        self.assertEqual(f"name: {name}", lines[0])
        self.assertRegex(lines[1], r"^description: .+$")

    def _assert_negative_boundary(self, name: str, text: str, patterns: list[str], boundary: str) -> None:
        self.assertTrue(
            any(re.search(pattern, text) for pattern in patterns),
            f"{name} must include a negative boundary for {boundary}",
        )

    def _assert_reference_links_resolve(self, name: str, text: str) -> None:
        links = {
            match.group(1).strip()
            for match in MARKDOWN_LINK_RE.finditer(text)
            if REFERENCE_LINK_RE.match(match.group(1).strip())
        }
        self.assertEqual(set(REQUIRED_SKILL_LINKS), links)

        reference_root = (SKILLS / "references").resolve()
        for link in sorted(links):
            path = (SKILLS / name / link).resolve()
            self.assertTrue(
                path.is_relative_to(reference_root),
                f"{name} reference link escapes shared references: {link}",
            )
            self.assertTrue(path.exists(), f"{name} reference link must resolve: {link}")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: FAIL because lifecycle skill packages and references do not exist.

## Task 2: Shared Lifecycle References

**Files:**
- Create: `plugins/product-agent-os/skills/references/lifecycle-states.md`
- Create: `plugins/product-agent-os/skills/references/handoff-contract.md`
- Create: `plugins/product-agent-os/skills/references/source-policy.md`
- Create: `plugins/product-agent-os/skills/references/complexity-routing.md`

- [ ] **Step 1: Add lifecycle state reference**

Create `plugins/product-agent-os/skills/references/lifecycle-states.md`:

```markdown
# Product-Agent OS Lifecycle States

Use this reference when a lifecycle skill needs state order, routing, or stop conditions.

State order:

1. `uninitialized`
2. `infrastructure_planned`
3. `requirements_ready`
4. `plan_ready`
5. `team_ready`
6. `build_active`
7. `quality_gate`
8. `review_ready`
9. `release_ready`
10. `learning_ready`
11. `maintenance`

Rules:

- Do not skip from `uninitialized` to `build_active`.
- Do not enter `requirements_ready` without a requirements packet.
- Do not enter `plan_ready` without acceptance criteria and verification strategy.
- Do not enter `team_ready` without ownership boundaries when work is parallel.
- Do not enter `release_ready` without verification evidence or documented failures.
- Do not enter `learning_ready` until delivery is complete or explicitly stopped.
- Treat `maintenance` as a routing state, not permission to create active automation.
```

- [ ] **Step 2: Add handoff contract reference**

Create `plugins/product-agent-os/skills/references/handoff-contract.md`:

```markdown
# Product-Agent OS Handoff Contract

Use this reference when a skill hands work to the next lifecycle role or reports a stop condition.

Required fields:

- `lifecycle_state`
- `goal`
- `constraints`
- `allowed_sources`
- `inputs_used`
- `verified_claims`
- `unsupported_claims`
- `files_touched`
- `files_proposed`
- `commands_run`
- `verification_evidence`
- `risks`
- `next_agent_task`
- `stop_reason`

Rules:

- `goal`, `constraints`, and `verification_evidence` must not be empty when a skill claims readiness.
- At least one of `files_touched` or `files_proposed` must be non-empty.
- `unsupported_claims` must be explicit when sources or runtime checks are missing.
- `commands_run` records command strings, not invented outcomes.
- `verification_evidence` records observed results from the current run.
- `stop_reason` is required when the skill cannot advance the lifecycle.
```

- [ ] **Step 3: Add source policy reference**

Create `plugins/product-agent-os/skills/references/source-policy.md`:

```markdown
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
```

- [ ] **Step 4: Add complexity routing reference**

Create `plugins/product-agent-os/skills/references/complexity-routing.md`:

```markdown
# Product-Agent OS Complexity Routing

Use this reference when adapting lifecycle depth to the project profile.

Profiles:

- `guided-small`: keep packets concise; propose minimal control-plane files; avoid custom agent generation.
- `standard-product`: require requirements, implementation plan, tests, release notes, and runlog evidence.
- `production-team`: require ownership boundaries, handoff fields, reviewer gates, and write-scope separation.
- `ai-product`: require prompt/context policy, deterministic checks, subjective eval criteria, and source fidelity.
- `enterprise-governed`: require approval gates, forbidden paths, audit evidence, and stricter source policy.
- `autonomous-maintenance`: require manual stability evidence before an automation candidate.

Complexity changes depth and risk gates. It does not change lifecycle order.
```

- [ ] **Step 5: Run lifecycle skill tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: FAIL because the skill packages do not exist yet, while reference-related assertions should pass once skills link them.

## Task 3: Orchestrator And Discovery Skills

**Files:**
- Create: `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`
- Create: `plugins/product-agent-os/skills/project-lifecycle-orchestrator/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`
- Create: `plugins/product-agent-os/skills/workspace-discovery-auditor/agents/openai.yaml`

- [ ] **Step 1: Add project lifecycle orchestrator skill**

Create `plugins/product-agent-os/skills/project-lifecycle-orchestrator/SKILL.md`:

```markdown
---
name: project-lifecycle-orchestrator
description: Route Product-Agent OS project work through lifecycle states. Use when the user asks to initialize, continue, recover, or guide a Codex project from audit through requirements, plan, team design, verification, review, release, learning, or automation candidate stages.
---

# Project Lifecycle Orchestrator

## Trigger

Use this skill when the user invokes Product-Agent OS, asks to guide a project end to end, asks for the next lifecycle step, or resumes a partially configured project.

## Boundaries

This is a Track 2 skill. Produce staged route packets and questions. Do not write project infrastructure directly, do not mutate global config, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- User goal or latest project request.
- Workspace path and visible project files.
- Existing `AGENTS.md`, `REQUIREMENTS.md`, `PLAN.md`, `TEST.md`, `EVALS.md`, `RUNLOG.md` when present.
- Discovery output from `plugins/product-agent-os/scripts/detect_project.py` when available.
- Current constraints, approvals, sandbox mode, and known blockers.

## Process

1. Read project rules before proposing action.
2. Determine the current lifecycle state.
3. Use this routing map:
   - `uninitialized` -> `workspace-discovery-auditor`
   - `infrastructure_planned` -> `requirements-author`
   - `requirements_ready` -> `implementation-planner`
   - `plan_ready` -> `agent-team-designer`
   - `team_ready` -> `test-eval-designer`
   - `build_active` -> `risk-reviewer`
   - `quality_gate` -> `risk-reviewer`
   - `review_ready` -> `pr-release-operator`
   - `release_ready` -> `learning-loop-maintainer`
   - `learning_ready` -> `automation-promoter`
   - `maintenance` -> `project-lifecycle-orchestrator`
4. Ask only blocking questions.
5. Return one recommended next skill or a stop condition.
6. Keep complexity profile as depth guidance, not permission to skip states.

## Outputs

Return a lifecycle route packet:

```yaml
lifecycle_route:
  current_state: ""
  next_state: ""
  recommended_skill: ""
  complexity_profile: ""
  blockers: []
  questions: []
  proposed_files: []
  approval_required: []
  stop_reason: ""
```

## Verification

Check that the selected state exists in the lifecycle reference and the recommended skill matches the routing map. If required evidence is missing, return a blocker instead of advancing.

## Failure Modes

- If state cannot be inferred, choose `uninitialized` and route to `workspace-discovery-auditor`.
- If user goal is absent, ask one blocking goal question.
- If project rules conflict with requested action, stop and show the conflict.
- If verification evidence is missing, do not claim readiness.

## Final Response Contract

Lead with the recommended next action. Include current state, next skill, blockers, questions, proposed files, approval requirements, and stop reason when blocked.
```

Create `plugins/product-agent-os/skills/project-lifecycle-orchestrator/agents/openai.yaml`:

```yaml
interface:
  display_name: "Lifecycle Orchestrator"
  short_description: "Routes Product-Agent OS lifecycle work."
  default_prompt: "Use $project-lifecycle-orchestrator to route this project to the next safe lifecycle step."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 2: Add workspace discovery auditor skill**

Create `plugins/product-agent-os/skills/workspace-discovery-auditor/SKILL.md`:

```markdown
---
name: workspace-discovery-auditor
description: Perform read-only Product-Agent OS workspace discovery and complexity profiling. Use when a project needs an audit before requirements, planning, infrastructure proposals, or lifecycle routing.
---

# Workspace Discovery Auditor

## Trigger

Use this skill for first-run project audit, greenfield workspace inspection, existing project readiness review, or profile inference before writing any project files.

## Boundaries

This is a Track 2 skill. It is read-only. Do not write files, do not modify config, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Workspace path.
- Allowed read scope.
- Existing project rules from `AGENTS.md`.
- Current sandbox and approval constraints.

## Process

1. Read project rules and obvious stack markers.
2. Prefer `plugins/product-agent-os/scripts/detect_project.py` for deterministic audit output.
3. Classify detected stack, existing control-plane files, missing control-plane files, `.codex/` assets, risks, and complexity profile.
4. Record missing tests as a gap, not a failure claim.
5. Return a staged audit packet with no writes.

## Outputs

Return a workspace audit packet:

```yaml
workspace_audit:
  status: "ready_for_plan | blocked | needs_user_input"
  detected_stack: []
  existing_control_plane: []
  missing_control_plane: []
  existing_codex_assets: []
  risks: []
  complexity_profile:
    name: ""
    confidence: ""
  next_action: ""
```

## Verification

Confirm no write commands were run. If a command was run, include the exact command and observed result. Do not claim tests or builds pass from file inspection.

## Failure Modes

- If workspace path is missing, ask for it.
- If workspace path does not exist, return blocked status.
- If reads are denied by sandbox or approvals, report the denied read and stop.
- If stack cannot be inferred, use `guided-small` with low confidence.

## Final Response Contract

Return detected facts, inferred profile, risks, missing files, blockers, and the next recommended lifecycle action.
```

Create `plugins/product-agent-os/skills/workspace-discovery-auditor/agents/openai.yaml`:

```yaml
interface:
  display_name: "Workspace Discovery"
  short_description: "Audits workspace state read-only."
  default_prompt: "Use $workspace-discovery-auditor to audit this workspace before planning changes."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 3: Run lifecycle skill tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: FAIL because the remaining eight skill packages do not exist.

## Task 4: Requirements, Planning, And Team Design Skills

**Files:**
- Create: `plugins/product-agent-os/skills/requirements-author/SKILL.md`
- Create: `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/implementation-planner/SKILL.md`
- Create: `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`
- Create: `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`

- [ ] **Step 1: Add requirements author skill**

Create `plugins/product-agent-os/skills/requirements-author/SKILL.md`:

```markdown
---
name: requirements-author
description: Convert a Product-Agent OS project goal into requirements, scope, non-goals, constraints, and acceptance criteria. Use after workspace discovery or when product intent is unclear before planning.
---

# Requirements Author

## Trigger

Use this skill when the project has an audit or goal but lacks explicit requirements, scope, non-goals, constraints, users, or acceptance criteria.

## Boundaries

This is a Track 2 skill. Produce a staged requirements packet. Do not write `REQUIREMENTS.md` directly, do not invent product decisions, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- User goal.
- Workspace audit packet.
- Existing product docs when present.
- Constraints, non-goals, risks, and open questions.

## Process

1. Restate the goal in operational language.
2. Identify target users and jobs to be done.
3. Separate in-scope work from non-goals.
4. Convert vague success into acceptance criteria.
5. Ask only blocking questions.
6. Mark assumptions and unsupported claims explicitly.

## Outputs

Return a requirements packet:

```yaml
requirements_packet:
  goal: ""
  users: []
  in_scope: []
  non_goals: []
  constraints: []
  acceptance_criteria: []
  open_questions: []
  files_proposed: ["REQUIREMENTS.md"]
```

## Verification

Check that at least one acceptance criterion exists and constraints are explicit. If user intent is missing, stop with questions.

## Failure Modes

- If goal is missing, ask for a goal.
- If scope spans unrelated systems, recommend splitting phases.
- If acceptance criteria depend on unsupported claims, label them as assumptions.
- If sensitive data appears, stop and ask for a redacted version.

## Final Response Contract

Return requirements, assumptions, unsupported claims, open questions, proposed file updates, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/requirements-author/agents/openai.yaml`:

```yaml
interface:
  display_name: "Requirements Author"
  short_description: "Turns goals into requirements."
  default_prompt: "Use $requirements-author to turn this project goal into acceptance criteria."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 2: Add implementation planner skill**

Create `plugins/product-agent-os/skills/implementation-planner/SKILL.md`:

```markdown
---
name: implementation-planner
description: Produce an executable Product-Agent OS implementation plan from approved requirements. Use when requirements are ready and the project needs slices, ownership, verification, rollback, and risks before code changes.
---

# Implementation Planner

## Trigger

Use this skill when requirements are ready and the project needs a staged implementation plan before any build slice.

## Boundaries

This is a Track 2 skill. Produce a staged implementation plan packet. Do not edit code, do not write `PLAN.md` directly, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Requirements packet.
- Workspace audit packet.
- Existing project conventions.
- Known test and build commands.
- Constraints and rollback needs.

## Process

1. Decompose work into focused slices.
2. Assign ownership boundaries by file or subsystem.
3. Name verification for each slice.
4. Identify rollback and migration risks.
5. Include approval gates for risky writes.
6. Keep unrelated refactors outside the plan.

## Outputs

Return an implementation plan packet:

```yaml
implementation_plan_packet:
  objective: ""
  slices: []
  ownership: []
  verification: []
  rollback: []
  risks: []
  files_proposed: ["PLAN.md"]
```

## Verification

Check that every slice has owner, files or subsystem scope, verification command or gap, and rollback note when risk is non-trivial.

## Failure Modes

- If requirements are incomplete, route back to `requirements-author`.
- If test commands are unknown, record a test gap and route to `test-eval-designer`.
- If write scopes overlap, route to `agent-team-designer`.
- If implementation requires external systems, require approval before action.

## Final Response Contract

Return slices, ownership, verification, rollback, risks, gaps, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/implementation-planner/agents/openai.yaml`:

```yaml
interface:
  display_name: "Implementation Planner"
  short_description: "Plans scoped build slices."
  default_prompt: "Use $implementation-planner to decompose these requirements into verified implementation slices."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 3: Add agent team designer skill**

Create `plugins/product-agent-os/skills/agent-team-designer/SKILL.md`:

```markdown
---
name: agent-team-designer
description: Design Product-Agent OS role ownership, handoff requirements, and model policies for a project. Use when work needs subagents, parallelism, role clarity, or review gates before implementation.
---

# Agent Team Designer

## Trigger

Use this skill when work needs role design, ownership separation, handoffs, parallel agents, or model and reasoning policy.

## Boundaries

This is a Track 2 skill. Produce a staged role and ownership packet. Do not create `.codex/agents/*.toml`, do not edit project config, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Implementation plan packet.
- Complexity profile.
- Existing team or project conventions.
- File ownership risks.
- Required review and verification gates.

## Process

1. Identify required roles from the work, not generic titles.
2. Assign ownership boundaries.
3. Define handoff fields and stop conditions.
4. Choose reasoning policy by risk and ambiguity.
5. Mark Track 3 candidates for `.codex/agents/*.toml`.
6. Prevent overlapping write scopes.

## Outputs

Return an agent team design packet:

```yaml
agent_team_design_packet:
  roles: []
  ownership_boundaries: []
  handoff_requirements: []
  model_policy: []
  files_proposed: []
  track_3_candidates: []
```

## Verification

Check that every role has ownership, inputs, outputs, verification expectation, and stop condition.

## Failure Modes

- If work is small, recommend a lightweight role plan.
- If ownership overlaps, stop and ask for scope split.
- If model policy is unspecified for high-risk work, propose escalation rules.
- If user requests actual agent files, record them as Track 3 candidates.

## Final Response Contract

Return roles, boundaries, handoff requirements, model policy, Track 3 candidates, risks, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/agent-team-designer/agents/openai.yaml`:

```yaml
interface:
  display_name: "Agent Team Designer"
  short_description: "Designs roles and handoffs."
  default_prompt: "Use $agent-team-designer to design role ownership and handoffs for this plan."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 4: Run lifecycle skill tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: FAIL because five skill packages are still missing.

## Task 5: Verification, Review, And Release Skills

**Files:**
- Create: `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`
- Create: `plugins/product-agent-os/skills/test-eval-designer/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`
- Create: `plugins/product-agent-os/skills/risk-reviewer/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`
- Create: `plugins/product-agent-os/skills/pr-release-operator/agents/openai.yaml`

- [ ] **Step 1: Add test and eval designer skill**

Create `plugins/product-agent-os/skills/test-eval-designer/SKILL.md`:

```markdown
---
name: test-eval-designer
description: Design deterministic tests, manual checks, and eval gates for Product-Agent OS projects. Use when a plan needs verification, subjective quality gates, AI evals, or test gap documentation before implementation or review.
---

# Test Eval Designer

## Trigger

Use this skill when the project needs test commands, eval criteria, quality gates, or explicit verification evidence requirements.

## Boundaries

This is a Track 2 skill. Produce a staged test and eval packet. Do not write `TEST.md` or `EVALS.md` directly, do not claim checks pass, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Requirements packet.
- Implementation plan packet.
- Workspace audit and stack.
- Known test, lint, build, docs, visual, or eval commands.
- Risk profile and acceptance criteria.

## Process

1. Map acceptance criteria to deterministic checks.
2. Add manual checks only when runtime verification cannot be automated.
3. Add eval gates for AI, UX, docs, or subjective quality.
4. Mark missing commands as test gaps.
5. Define evidence required before readiness claims.
6. Keep thresholds explicit.

## Outputs

Return a test and eval packet:

```yaml
test_eval_packet:
  deterministic_checks: []
  manual_checks: []
  evals: []
  thresholds: []
  evidence_required: []
  files_proposed: ["TEST.md", "EVALS.md"]
```

## Verification

Check that every acceptance criterion has a deterministic check, manual check, eval, or documented gap.

## Failure Modes

- If no tests exist, report a test gap.
- If a check needs credentials or external systems, require approval.
- If an eval is subjective, define rubric and threshold.
- If verification cannot run, do not claim readiness.

## Final Response Contract

Return checks, evals, thresholds, gaps, evidence requirements, proposed files, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/test-eval-designer/agents/openai.yaml`:

```yaml
interface:
  display_name: "Test Eval Designer"
  short_description: "Defines tests and eval gates."
  default_prompt: "Use $test-eval-designer to design verification and eval gates for this project."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 2: Add risk reviewer skill**

Create `plugins/product-agent-os/skills/risk-reviewer/SKILL.md`:

```markdown
---
name: risk-reviewer
description: Review Product-Agent OS plans, diffs, or quality gates for correctness, regressions, missing tests, security risk, approval risk, and unsupported claims. Use before declaring a build slice ready.
---

# Risk Reviewer

## Trigger

Use this skill when a diff, implementation slice, plan, or quality gate needs review before release or handoff.

## Boundaries

This is a Track 2 skill. Produce a staged risk review packet. Do not edit files, do not approve without evidence, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Diff summary or proposed changes.
- Requirements and plan packets.
- Commands run and verification evidence.
- Known risks, approvals, and source constraints.

## Process

1. Lead with findings by severity.
2. Check behavior against requirements.
3. Check missing tests and unverified claims.
4. Check approval, security, data, migration, and external system risks.
5. Return blocked, changes requested, or ready.
6. Keep summary secondary to findings.

## Outputs

Return a risk review packet:

```yaml
risk_review_packet:
  findings: []
  missing_tests: []
  approval_risks: []
  source_risks: []
  verdict: "blocked | changes_requested | ready"
  next_action: ""
```

## Verification

Check that every readiness claim cites current verification evidence. If evidence is absent, verdict cannot be ready.

## Failure Modes

- If diff or proposed change is unavailable, ask for it.
- If tests were not run, report missing verification.
- If source claims are unsupported, list them under source risks.
- If a finding is security-sensitive, avoid exposing secrets.

## Final Response Contract

Return findings first, then missing tests, approval risks, source risks, verdict, and next action.
```

Create `plugins/product-agent-os/skills/risk-reviewer/agents/openai.yaml`:

```yaml
interface:
  display_name: "Risk Reviewer"
  short_description: "Reviews risk before release."
  default_prompt: "Use $risk-reviewer to review this project slice before release readiness."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 3: Add PR release operator skill**

Create `plugins/product-agent-os/skills/pr-release-operator/SKILL.md`:

```markdown
---
name: pr-release-operator
description: Prepare Product-Agent OS PR or release packets from verified work. Use when review is complete and the project needs summary, checks, user impact, rollback, residual risks, and approval notes.
---

# PR Release Operator

## Trigger

Use this skill when work is review-ready and needs a PR packet, release packet, rollout note, or rollback note.

## Boundaries

This is a Track 2 skill. Produce a staged PR or release packet. Do not publish externally, do not push, do not open PRs, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Requirements and plan packets.
- Review verdict.
- Commands run and verification evidence.
- User impact, rollback notes, and residual risks.

## Process

1. Summarize what changed and why.
2. Include verification commands and observed results.
3. Document user impact and rollback.
4. List residual risks and approvals.
5. Prepare staged PR or release text.
6. Ask for explicit approval before external publishing actions.

## Outputs

Return a PR or release packet:

```yaml
pr_release_packet:
  summary: ""
  checks_run: []
  user_impact: ""
  rollback: ""
  residual_risks: []
  approval_required: []
```

## Verification

Check that each listed check has observed evidence and the rollback note matches the risk profile.

## Failure Modes

- If review verdict is blocked, route back to `risk-reviewer`.
- If checks are absent, report missing evidence.
- If rollback is missing for risky work, ask for rollback strategy.
- If external publish is requested, require approval.

## Final Response Contract

Return summary, checks, user impact, rollback, residual risks, approval requirements, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/pr-release-operator/agents/openai.yaml`:

```yaml
interface:
  display_name: "PR Release Operator"
  short_description: "Prepares PR and release packets."
  default_prompt: "Use $pr-release-operator to prepare a PR or release packet from verified work."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 4: Run lifecycle skill tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: FAIL because two skill packages are still missing.

## Task 6: Learning And Automation Candidate Skills

**Files:**
- Create: `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`
- Create: `plugins/product-agent-os/skills/learning-loop-maintainer/agents/openai.yaml`
- Create: `plugins/product-agent-os/skills/automation-promoter/SKILL.md`
- Create: `plugins/product-agent-os/skills/automation-promoter/agents/openai.yaml`

- [ ] **Step 1: Add learning loop maintainer skill**

Create `plugins/product-agent-os/skills/learning-loop-maintainer/SKILL.md`:

```markdown
---
name: learning-loop-maintainer
description: Capture Product-Agent OS project lessons, failures, durable rule candidates, skill candidates, and runlog compaction proposals after delivery or stop conditions.
---

# Learning Loop Maintainer

## Trigger

Use this skill after delivery, after a stopped lifecycle run, or when runlog evidence needs compaction into lessons and next actions.

## Boundaries

This is a Track 2 skill. Produce a staged learning packet. Do not edit `AGENTS.md`, do not promote durable rules without evidence, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Final result or stop reason.
- Runlog evidence.
- Failures, decisions, and review findings.
- Reusable methods and repeated gaps.

## Process

1. Extract decisions from evidence.
2. Separate failures from risks and open questions.
3. Propose durable rule candidates only when evidence supports them.
4. Propose skill candidates only after repeated manual success or clear reuse.
5. Propose runlog compaction without deleting evidence.
6. Route stable recurring workflows to `automation-promoter`.

## Outputs

Return a learning loop packet:

```yaml
learning_loop_packet:
  decisions: []
  failures: []
  durable_rules_candidate: []
  skill_candidates: []
  runlog_compaction: []
  next_action: ""
```

## Verification

Check that each durable rule candidate cites evidence or a repeated failure. If evidence is missing, keep it as an observation.

## Failure Modes

- If runlog evidence is absent, ask for evidence.
- If a lesson contains secrets, stop and request redaction.
- If a rule is project-specific, keep it out of global guidance.
- If automation is requested too early, route to candidate-only analysis.

## Final Response Contract

Return decisions, failures, durable rule candidates, skill candidates, runlog compaction proposal, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/learning-loop-maintainer/agents/openai.yaml`:

```yaml
interface:
  display_name: "Learning Loop"
  short_description: "Captures lessons and candidates."
  default_prompt: "Use $learning-loop-maintainer to capture lessons from this Product-Agent OS run."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 2: Add automation promoter skill**

Create `plugins/product-agent-os/skills/automation-promoter/SKILL.md`:

```markdown
---
name: automation-promoter
description: Evaluate whether a stable Product-Agent OS workflow is ready to become an automation candidate. Use only after manual stability evidence exists and the user asks about recurring or repeated workflow promotion.
---

# Automation Promoter

## Trigger

Use this skill when a recurring workflow may be promoted from manual process to automation candidate.

## Boundaries

This is a Track 2 skill. Produce a candidate_only packet. Do not activate recurring jobs, do not schedule jobs, do not modify external systems, do not create active automation, and do not store secrets.

Read shared references when needed: [lifecycle states](<../references/lifecycle-states.md>), [handoff contract](<../references/handoff-contract.md>), [source policy](<../references/source-policy.md>), and [complexity routing](<../references/complexity-routing.md>).

## Inputs

- Manual stability evidence.
- Workflow purpose.
- Inputs, outputs, cadence, owner, verification, failure modes, and rollback or disable path.
- Write policy and approval requirements.

## Process

1. Confirm manual stability evidence exists.
2. Identify required inputs and stable outputs.
3. Define write policy as read_only, draft_only, or approved_write.
4. Name verification and failure modes.
5. Name owner, cadence, and rollback or disable path.
6. Return candidate_only readiness.

## Outputs

Return an automation candidate packet:

```yaml
automation_candidate:
  name: ""
  purpose: ""
  trigger_or_cadence: ""
  required_inputs: []
  write_policy: "read_only | draft_only | approved_write"
  verification: []
  failure_modes: []
  owner: ""
  rollback_or_disable: ""
  readiness: "candidate_only"
```

## Verification

Check that manual stability evidence exists and failure modes are named. If not, candidate readiness is blocked.

## Failure Modes

- If manual stability evidence is missing, stop and request it.
- If inputs or outputs are unstable, keep workflow manual.
- If external writes are involved, require approved_write policy and explicit approval.
- If owner is missing, block candidate readiness.

## Final Response Contract

Return candidate name, purpose, cadence, inputs, write policy, verification, failure modes, owner, rollback or disable path, readiness, and next lifecycle action.
```

Create `plugins/product-agent-os/skills/automation-promoter/agents/openai.yaml`:

```yaml
interface:
  display_name: "Automation Promoter"
  short_description: "Assesses automation candidates."
  default_prompt: "Use $automation-promoter to evaluate whether this repeated workflow is ready as an automation candidate."
policy:
  allow_implicit_invocation: false
```

- [ ] **Step 3: Run lifecycle skill tests**

Run:

```powershell
python -m unittest tests.product_agent_os.test_lifecycle_skills -v
```

Expected: PASS.

## Task 7: Navigation And Full Verification

**Files:**
- Modify: `mkdocs.yml`

- [ ] **Step 1: Add plan to MkDocs navigation**

Modify `mkdocs.yml` by adding this plan under `Планы реализации`:

```yaml
      - Product-Agent OS lifecycle skills: superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md
```

- [ ] **Step 2: Run all tests**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: all tests PASS.

- [ ] **Step 3: Run docs checks**

Run:

```powershell
python tools\check_docs.py
```

Expected: `OK: documentation structure checks passed`.

- [ ] **Step 4: Run strict MkDocs build**

Run:

```powershell
$env:PYTHONPATH='C:\tmp\codex_docs_mkdocs'; python -m mkdocs build --strict
```

Expected: documentation builds successfully. A Material for MkDocs upstream warning is acceptable if exit code is 0.

- [ ] **Step 5: Run fixture eval**

Run:

```powershell
python plugins\product-agent-os\scripts\run_fixture_eval.py
```

Expected: exit 0 and JSON results for fixture projects.

- [ ] **Step 6: Record commit or changed files**

If the workspace is a git repository, run:

```powershell
git add tests/product_agent_os/test_lifecycle_skills.py plugins/product-agent-os/skills mkdocs.yml docs/superpowers/plans/2026-05-14-product-agent-os-lifecycle-skills.md docs/superpowers/specs/2026-05-14-product-agent-os-lifecycle-skills-design.md
git commit -m "feat: add product agent lifecycle skills"
```

If the workspace is not a git repository, record the changed file list and verification results in the implementation run log for this task.

## Self-Review

Spec coverage:

- Required lifecycle skills are covered by Tasks 3 through 6.
- Shared references are covered by Task 2.
- Required headings, frontmatter, UI metadata, routing coverage, boundary language, and automation candidate-only policy are covered by Task 1 tests.
- Docs navigation and full verification are covered by Task 7.

Known follow-up tracks:

- Track 3: generated project infrastructure templates, `.codex/agents/*.toml`, hooks, workflow packets, eval templates.
- Track 4: production hardening, fixture eval expansion, safe merge integration with templates, source policy checks, automation promotion gates, optional Agents SDK runner.

This plan keeps Track 2 focused on skill packages and avoids hidden writes, external systems, active automations, and global config mutation.
