"""Fixed stdlib-only bridge. Input paths are supplied solely by the trusted host.

Discovery and task advice consume an owned projection. The task request comes
from the trusted local-service host on stdin and cannot select an executable.
"""

import json
import sys
from pathlib import Path


def main() -> None:
    """Emit a small allowlist, excluding absolute roots and raw file contents."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if sys.version_info < (3, 11):
        raise RuntimeError("unsupported Python version")
    scripts, projection = (Path(value).resolve() for value in sys.argv[1:3])
    sys.path.insert(0, str(scripts))
    from product_agent_os.discovery import analyze_workspace

    if sys.argv[3:] == ["--task-advice"]:
        emit_task_advice(projection)
        return
    if sys.argv[3:]:
        raise ValueError("unsupported mode")

    result = analyze_workspace(projection)
    paths = frozenset(result["detected_files"])
    components = []
    for component in result.get("plugin_components", [])[:20]:
        inventory = component.get("inventory", {})
        manifest = inventory.get("manifest_path")
        package = component.get("package_path")
        if isinstance(manifest, str) and isinstance(package, str) and package != ".":
            manifest = f"{package}/{manifest}"
        if isinstance(manifest, str) and manifest in paths:
            components.append(manifest)
    output = {
        "schemaVersion": "paos_analysis_bridge_v1",
        "pythonVersion": ".".join(str(part) for part in sys.version_info[:3]),
        "stack": result.get("detected_stack", [])[:20],
        "controlPlane": result.get("existing_control_plane", [])[:20],
        "components": components,
    }
    print(json.dumps(output, ensure_ascii=False))


def emit_task_advice(projection: Path) -> None:
    from product_agent_os.discovery import analyze_workspace
    from product_agent_os.methodology_decision import build_methodology_decision
    from product_agent_os.task_routing import build_task_routing, normalize_task_intent

    text = sys.stdin.buffer.read(16 * 1024 + 1)
    if len(text) > 16 * 1024:
        raise ValueError("request too large")
    request = json.loads(text)
    if set(request) != {"task", "scope"} or request["task"] is None:
        raise ValueError("invalid request")
    task, intent = normalize_task_intent(projection, request["task"])
    audit = analyze_workspace(projection, intent_hint=intent)
    route = build_task_routing(projection, audit, task, include_revision_sources=True)
    sources = route.pop("revision_sources")
    decision = build_methodology_decision(projection, audit, task, route, sources, host_scope=request["scope"])
    print(json.dumps({"schemaVersion": "paos_task_advice_bridge_v1", "decision": decision}, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # A traceback could expose owned paths or file contents. The host reports
        # a stable reason code and never forwards arbitrary stderr to the UI.
        sys.exit(1)
