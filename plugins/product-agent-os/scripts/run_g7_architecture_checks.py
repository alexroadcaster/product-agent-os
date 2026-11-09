"""Explicit approved synthetic architecture checks; no installs, fixes or baseline writes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import time
from pathlib import Path
from product_agent_os.code_quality_selector import architecture_evidence

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / "tests/fixtures/product_agent_os/g7-architecture"
TOOLS = ROOT / ".docs-tools/g7-architecture-tools"


def digest(value):
    return hashlib.sha256(value).hexdigest()


def run():
    manifest = json.loads((CORPUS / "manifest.json").read_text())
    required_cases = {"python": {"allowed", "direct", "transitive", "cycle"},
                      "javascript": {"allowed", "direct", "transitive", "cycle", "alias", "unresolved"}}
    if {family: set(cases) for family, cases in manifest["expected"].items()} != required_cases:
        raise ValueError("missing or unexpected architecture cases")
    actual = {p.relative_to(CORPUS).as_posix() for p in CORPUS.rglob("*")
              if p.is_file() and p != CORPUS / "manifest.json"
              and not (p.suffix == ".pyc" and "__pycache__" in p.parts and p.relative_to(CORPUS).parts[0] == "python")}
    if actual != set(manifest["exact_files"]):
        raise ValueError("extra or missing architecture fixture files")
    for name, expected in manifest["exact_files"].items():
        if digest((CORPUS / name).read_bytes()) != expected:
            raise ValueError("fixture drift: " + name)
    lint = str(TOOLS / "python/Scripts/lint-imports.exe")
    cruise = str(TOOLS / "javascript/node_modules/dependency-cruiser/bin/dependency-cruiser.mjs")
    versions = {}
    for name, command, expected in [("import-linter", [lint, "--version"], "2.16"),
                                    ("dependency-cruiser", ["node", cruise, "--version"], "18.6.0")]:
        probe = subprocess.run(command, capture_output=True, text=True, timeout=30, check=True)
        if probe.stdout.strip().split()[-1] != expected:
            raise ValueError("unexpected tool version")
        versions[name] = expected
    records = []
    for family, cases in manifest["expected"].items():
        for case, expected in cases.items():
            cwd = CORPUS / family / case
            env = dict(os.environ, PYTHONPATH=str(cwd), NO_COLOR="1", PYTHONDONTWRITEBYTECODE="1")
            command = ([lint, "--config", ".importlinter", "--no-cache", "--no-logo"] if family == "python"
                       else ["node", cruise, "src", "--config", "rules.json", "--no-cache", "--output-type", "json"])
            started = time.monotonic()
            completed = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=60)
            findings = []
            if family == "python":
                output = completed.stdout
                edges = [line.strip().lstrip("- ") for line in output.splitlines() if " -> " in line]
                expected_edges = {"allowed": 0, "direct": 1, "transitive": 2, "cycle": 2}[case]
                matched = (completed.returncode == (0 if case == "allowed" else 1)
                           and "Analyzed 7 files" in output and len(edges) == expected_edges
                           and (("0 broken." in output) if case == "allowed" else ("1 broken." in output)))
                expected_witness = {"allowed": [],
                    "direct": ["sample.domain.service -> sample.infra.db (l.1)"],
                    "transitive": ["sample.domain.service -> sample.bridge (l.1)", "sample.bridge -> sample.infra.db (l.1)"],
                    "cycle": ["sample.domain.other -> sample.domain.service (l.1)", "sample.domain.service -> sample.domain.other (l.1)"]}[case]
                matched = matched and (sorted(edges) == sorted(expected_witness) if case == "cycle" else edges == expected_witness)
                if edges:
                    findings = [dict(rule="independence" if case == "cycle" else "domain-no-infra",
                                     subject="sample.domain", severity="error", path="sample/domain/service.py", witness=edges)]
                coverage = "complete" if matched else "unknown"
                tool = "import-linter"
                config = cwd / ".importlinter"
                summary = dict(edges=edges, recognized=matched)
            else:
                report = json.loads(completed.stdout)
                summary = report["summary"]
                violations = summary["violations"]
                modules = {m["source"] for m in report["modules"]}
                expected_modules = {p.relative_to(cwd).as_posix() for p in (cwd / "src").rglob("*.mjs")}
                unresolved = any(d.get("couldNotResolve") for m in report["modules"] for d in m.get("dependencies", []))
                matched = (completed.returncode == 0 and sorted(v["rule"]["name"] for v in violations) == sorted(expected)
                           and expected_modules <= modules and summary["advisedExitCode"] == (1 if expected else 0)
                           and (unresolved == (case == "unresolved")))
                expected_endpoints = {"direct": ("src/domain/service.mjs", "src/infra/db.mjs"),
                    "transitive": ("src/domain/service.mjs", "src/infra/db.mjs"),
                    "alias": ("src/domain/service.mjs", "src/infra/db.mjs"),
                    "cycle": ("src/domain/other.mjs", "src/domain/service.mjs"),
                    "unresolved": ("src/domain/service.mjs", "#missing")}
                if case != "allowed":
                    matched = matched and len(violations) == 1 and (violations[0]["from"], violations[0]["to"]) == expected_endpoints[case]
                if case == "transitive":
                    matched = matched and [p["name"] for p in violations[0].get("via", [])] == ["src/bridge.mjs", "src/infra/db.mjs"]
                if case == "cycle":
                    matched = matched and {p["name"] for p in violations[0].get("cycle", [])} == {"src/domain/service.mjs", "src/domain/other.mjs"}
                if case == "alias":
                    matched = matched and any(d.get("module") == "#db" and d.get("resolved") == "src/infra/db.mjs"
                        and "aliased-subpath-import" in d.get("dependencyTypes", [])
                        for m in report["modules"] for d in m.get("dependencies", []))
                for v in violations:
                    witness = [p["name"] for p in v.get("via", v.get("cycle", []))] or [v["to"]]
                    findings.append(dict(rule=v["rule"]["name"], subject=v["from"] + " -> " + v["to"],
                                         severity=v["rule"]["severity"], path=v["from"], witness=witness))
                coverage = "unresolved" if unresolved else ("complete" if matched else "unknown")
                tool = "dependency-cruiser"
                config = cwd / "rules.json"
                summary = dict(advised_exit_code=summary["advisedExitCode"], module_count=len(modules),
                               expected_module_count=len(expected_modules), unresolved=unresolved)
            lock = TOOLS / ("python-lock.txt" if family == "python" else "javascript/package-lock.json")
            policy = dict(scope="sample" if family == "python" else "src", exclusions=["node_modules"],
                          resolver="python" if family == "python" else "node imports #db",
                          type_only="included" if family == "python" else "not_applicable: .mjs only",
                          lock_digest=digest(lock.read_bytes()))
            context = dict(tool=tool, version=versions[tool], config_digest=digest(config.read_bytes()),
                           policy_digest=digest(json.dumps(policy, sort_keys=True).encode()),
                           input_digest=digest(json.dumps({k:v for k,v in manifest["exact_files"].items()
                                                          if k.startswith(family + "/" + case + "/")}, sort_keys=True).encode()))
            receipt = dict(context, installed=True, runnable=True, outcome="completed" if matched else "failed",
                           coverage=coverage, findings=findings, controls=[])
            records.append(dict(family=family, case=case, expected_matched=matched, context=context, receipt=receipt,
                                policy=policy, summary=summary, process_exit_code=completed.returncode,
                                output_digest=digest(completed.stdout.encode()), elapsed_seconds=round(time.monotonic()-started, 3),
                                command=["lint-imports" if family == "python" else "node dependency-cruiser", *command[1 if family == "python" else 2:]]))
    for record in records:
        controls = [r for r in records if r["family"] == record["family"] and r["case"] in ("allowed", "direct", "transitive")]
        if {r["case"] for r in controls} == {"allowed", "direct", "transitive"} and all(r["expected_matched"] for r in controls):
            record["receipt"]["controls"] = ["allowed", "forbidden", "transitive"]
        record["projection"] = architecture_evidence(record["context"], (record["receipt"],))
    comparisons = []
    for family in manifest["expected"]:
        baseline = next(r for r in records if r["family"] == family and r["case"] == "direct")["receipt"]
        for case in ("direct", "transitive", "allowed"):
            current = next(r for r in records if r["family"] == family and r["case"] == case)
            comparisons.append(dict(family=family, case=case,
                                    result=architecture_evidence(current["context"], (current["receipt"],), baseline)))
    result = dict(schema_version="g7_architecture_receipt_v1", synthetic_only=True,
                  manifest_digest=digest((CORPUS / "manifest.json").read_bytes()), runner_digest=digest(Path(__file__).read_bytes()),
                  python=platform.python_version(), node=subprocess.check_output(["node", "--version"], text=True).strip(),
                  passed=sum(r["expected_matched"] for r in records), attempted=len(records), records=records,
                  baseline_comparisons=comparisons, limits=["No TypeScript resolver/type-only execution", "No target project/CI/auto-fix"])
    destination = ROOT / "docs/superpowers/specs/paos-aud-g7-architecture-results.json"
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": result["passed"], "attempted": result["attempted"]}))
    return result["passed"] == result["attempted"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-approved-fixtures", action="store_true", required=True)
    parser.parse_args()
    destination = ROOT / "docs/superpowers/specs/paos-aud-g7-architecture-results.json"
    # Invalidate the prior result before any setup probe; failure cannot retain a green receipt.
    destination.write_text(json.dumps({"status": "in_progress", "verified": False}) + "\n")
    try:
        success = run()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        destination.write_text(json.dumps({"status": "setup_error", "verified": False,
                                          "error_type": type(error).__name__}) + "\n")
        print("architecture setup failed:", type(error).__name__)
        success = False
    raise SystemExit(0 if success else 1)
