"""Fixed stdlib-only bridge. Input paths are supplied solely by the trusted host.

Only discovery over an owned projection is allowed here. First-run orchestration
also executes a script matrix and is deliberately outside this boundary.
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
    scripts, projection = (Path(value).resolve() for value in sys.argv[1:])
    sys.path.insert(0, str(scripts))
    from product_agent_os.discovery import analyze_workspace

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


if __name__ == "__main__":
    try:
        main()
    except Exception:
        # A traceback could expose owned paths or file contents. The host reports
        # a stable reason code and never forwards arbitrary stderr to the UI.
        sys.exit(1)
