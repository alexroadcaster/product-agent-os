"""Read-only language adapters for project code graph overlays."""

from __future__ import annotations

import ast
import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from product_agent_os.project_graph_observations import build_observation_record


PYTHON_AST_ADAPTER = "python_ast"
UNSUPPORTED_FILE_ADAPTER = "unsupported_file"
MAX_UNRESOLVED_CALLS = 100
MAX_ADAPTER_FILE_BYTES = 1_000_000


@dataclass
class PythonModuleInfo:
    relative_path: str
    module_name: str
    fingerprint: str
    tree: ast.AST
    source_lines: list[str]
    package_name: str | None = None
    symbol_ids: dict[str, str] = field(default_factory=dict)
    import_bindings: dict[str, str] = field(default_factory=dict)


def available_graph_adapters() -> list[str]:
    """Return installed graph adapter names without activating external tools."""

    return [PYTHON_AST_ADAPTER, UNSUPPORTED_FILE_ADAPTER]


def build_language_overlays(
    root: Path,
    manifest_files: list[dict[str, Any]],
    *,
    scan_id: str,
    workspace_id: str,
) -> dict[str, Any]:
    """Build deterministic language overlays from local files only."""

    python_items = [
        item
        for item in manifest_files
        if item.get("language") == "python"
        and not item.get("generated")
        and str(item.get("relative_path"))
        and int(item.get("size_bytes") or 0) <= MAX_ADAPTER_FILE_BYTES
    ]
    modules = _load_python_modules(root, python_items)
    package_nodes, package_edges, package_observations = _build_package_overlay(
        root,
        modules,
        scan_id=scan_id,
        workspace_id=workspace_id,
    )
    symbol_nodes, symbol_edges, symbol_observations = _build_symbol_overlay(modules, scan_id=scan_id)
    import_edges, import_observations = _build_import_overlay(modules, scan_id=scan_id)
    symbol_ids = {symbol_id for module in modules.values() for symbol_id in module.symbol_ids.values()}
    call_edges, test_edges, call_observations, unresolved_calls = _build_call_overlay(
        modules,
        scan_id=scan_id,
        symbol_ids=symbol_ids,
    )
    adapter_summary = _adapter_summary(manifest_files)

    return {
        "nodes": package_nodes + symbol_nodes,
        "edges": package_edges + symbol_edges + import_edges + call_edges + test_edges,
        "observations": package_observations + symbol_observations + import_observations + call_observations,
        "metadata": {
            "adapter_summary": adapter_summary,
            "python_scanner": {
                "adapter": PYTHON_AST_ADAPTER,
                "module_count": len(modules),
                "package_count": len({module.package_name for module in modules.values() if module.package_name}),
                "symbol_count": len(symbol_nodes),
                "import_edge_count": len(import_edges),
                "call_edge_count": len(call_edges),
                "test_edge_count": len(test_edges),
                    "unresolved_calls": _safe_unresolved_calls(unresolved_calls[:MAX_UNRESOLVED_CALLS]),
                "unresolved_call_count": len(unresolved_calls),
                "confidence_policy": "direct local or imported calls only",
            },
        },
    }


def _load_python_modules(root: Path, items: list[dict[str, Any]]) -> dict[str, PythonModuleInfo]:
    modules: dict[str, PythonModuleInfo] = {}
    package_dirs = {
        str(Path(item["relative_path"]).parent).replace("\\", "/")
        for item in items
        if Path(item["relative_path"]).name == "__init__.py"
    }
    for item in sorted(items, key=lambda value: str(value["relative_path"])):
        relative_path = str(item["relative_path"])
        path = root / relative_path
        try:
            text = path.read_text(encoding="utf-8")
            tree = ast.parse(text, filename=relative_path)
        except (OSError, SyntaxError, UnicodeDecodeError):
            continue
        module_name = _module_name_for_path(relative_path)
        package_name = _package_name_for_path(relative_path, package_dirs)
        modules[relative_path] = PythonModuleInfo(
            relative_path=relative_path,
            module_name=module_name,
            package_name=package_name,
            fingerprint=str(item["fingerprint"]),
            tree=tree,
            source_lines=text.splitlines(),
        )

    symbol_ids: set[str] = set()
    for module in modules.values():
        module.symbol_ids.update(_local_symbol_ids(module.tree, module.module_name))
        symbol_ids.update(module.symbol_ids.values())
    module_ids = {f"module:{module.module_name}" for module in modules.values()}
    for module in modules.values():
        module.import_bindings.update(_import_bindings(module.tree, module, symbol_ids, module_ids))
    return modules


def _build_package_overlay(
    root: Path,
    modules: dict[str, PythonModuleInfo],
    *,
    scan_id: str,
    workspace_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    packages: dict[str, PythonModuleInfo] = {}
    for module in modules.values():
        if Path(module.relative_path).name == "__init__.py":
            packages[module.module_name] = module
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    for package_name, module in sorted(packages.items()):
        package_id = f"package:{package_name}"
        observation = _observation(
            scan_id,
            subject_id=package_id,
            relative_path=module.relative_path,
            start_line=1,
            end_line=max(1, len(module.source_lines) or 1),
            fingerprint=module.fingerprint,
            extractor="python_ast_package",
            confidence="verified",
        )
        observations.append(observation)
        nodes.append(
            _node(
                package_id,
                node_type="package",
                label=package_name,
                language="python",
                path=module.relative_path,
                source_span=_span(module.relative_path, 1, max(1, len(module.source_lines) or 1), module.fingerprint),
                observation_id=observation["id"],
            )
        )
        edge, edge_observation = _edge(
            scan_id,
            edge_type="contains",
            source=workspace_id,
            target=package_id,
            relative_path=module.relative_path,
            line=1,
            fingerprint=module.fingerprint,
            extractor="python_ast_package",
            confidence="verified",
        )
        edges.append(edge)
        observations.append(edge_observation)

    for module in modules.values():
        module_id = f"module:{module.module_name}"
        parent = f"package:{module.package_name}" if module.package_name else f"file:{module.relative_path}"
        if parent.startswith("package:") and parent not in {node["id"] for node in nodes}:
            parent = f"file:{module.relative_path}"
        edge, observation = _edge(
            scan_id,
            edge_type="contains",
            source=parent,
            target=module_id,
            relative_path=module.relative_path,
            line=1,
            fingerprint=module.fingerprint,
            extractor="python_ast_module",
            confidence="verified",
        )
        edges.append(edge)
        observations.append(observation)
    return nodes, edges, observations


def _build_symbol_overlay(
    modules: dict[str, PythonModuleInfo],
    *,
    scan_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    for module in modules.values():
        module_id = f"module:{module.module_name}"
        module_observation = _observation(
            scan_id,
            subject_id=module_id,
            relative_path=module.relative_path,
            start_line=1,
            end_line=max(1, len(module.source_lines) or 1),
            fingerprint=module.fingerprint,
            extractor="python_ast_module",
            confidence="verified",
        )
        observations.append(module_observation)
        nodes.append(
            _node(
                module_id,
                node_type="module",
                label=module.module_name,
                language="python",
                path=module.relative_path,
                source_span=_span(module.relative_path, 1, max(1, len(module.source_lines) or 1), module.fingerprint),
                observation_id=module_observation["id"],
            )
        )
        for item in _iter_symbol_defs(module.tree, module.module_name):
            symbol_id = item["id"]
            observation = _observation(
                scan_id,
                subject_id=symbol_id,
                relative_path=module.relative_path,
                start_line=item["start_line"],
                end_line=item["end_line"],
                fingerprint=module.fingerprint,
                extractor="python_ast_symbol",
                confidence="verified",
            )
            observations.append(observation)
            nodes.append(
                _node(
                    symbol_id,
                    node_type=item["type"],
                    label=item["label"],
                    language="python",
                    path=module.relative_path,
                    source_span=_span(module.relative_path, item["start_line"], item["end_line"], module.fingerprint),
                    observation_id=observation["id"],
                )
            )
            edge, edge_observation = _edge(
                scan_id,
                edge_type="contains",
                source=item["parent_id"] or module_id,
                target=symbol_id,
                relative_path=module.relative_path,
                line=item["start_line"],
                fingerprint=module.fingerprint,
                extractor="python_ast_symbol",
                confidence="verified",
            )
            edges.append(edge)
            observations.append(edge_observation)
    return nodes, edges, observations


def _build_import_overlay(
    modules: dict[str, PythonModuleInfo],
    *,
    scan_id: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    for module in modules.values():
        module_id = f"module:{module.module_name}"
        for binding_name, target_id in sorted(module.import_bindings.items()):
            edge, observation = _edge(
                scan_id,
                edge_type="imports",
                source=module_id,
                target=target_id,
                relative_path=module.relative_path,
                line=_import_line(module.tree, binding_name),
                fingerprint=module.fingerprint,
                extractor="python_ast_import",
                confidence="verified",
            )
            edges.append(edge)
            observations.append(observation)
    return edges, observations


def _build_call_overlay(
    modules: dict[str, PythonModuleInfo],
    *,
    scan_id: str,
    symbol_ids: set[str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    edges: list[dict[str, Any]] = []
    test_edges: list[dict[str, Any]] = []
    observations: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    for module in modules.values():
        local_symbols = module.symbol_ids
        for call in _iter_calls(module.tree, module.module_name):
            target_id = _resolve_call_target(call["call"], module, local_symbols, symbol_ids)
            if not target_id:
                name = _call_name(call["call"])
                if name:
                    unresolved.append(
                        {
                            "name": name,
                            "relative_path": module.relative_path,
                            "line": int(getattr(call["call"], "lineno", 1)),
                            "scope": call["source_id"],
                            "status": "unsupported",
                        }
                    )
                continue
            edge, observation = _edge(
                scan_id,
                edge_type="calls",
                source=call["source_id"],
                target=target_id,
                relative_path=module.relative_path,
                line=int(getattr(call["call"], "lineno", 1)),
                fingerprint=module.fingerprint,
                extractor="python_ast_call",
                confidence="inferred",
            )
            edges.append(edge)
            observations.append(observation)
            if _is_test_source(module.relative_path, call["source_id"]):
                test_edge, test_observation = _edge(
                    scan_id,
                    edge_type="tests",
                    source=call["source_id"],
                    target=target_id,
                    relative_path=module.relative_path,
                    line=int(getattr(call["call"], "lineno", 1)),
                    fingerprint=module.fingerprint,
                    extractor="python_ast_test_link",
                    confidence="inferred",
                )
                test_edges.append(test_edge)
                observations.append(test_observation)
    return edges, test_edges, observations, unresolved


def _iter_symbol_defs(tree: ast.AST, module_name: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.ClassDef):
            class_id = f"class:{module_name}.{node.name}"
            items.append(_symbol_item(class_id, "class", node.name, node, parent_id=f"module:{module_name}"))
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    method_id = f"method:{module_name}.{node.name}.{child.name}"
                    items.append(_symbol_item(method_id, "method", f"{node.name}.{child.name}", child, parent_id=class_id))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_id = f"function:{module_name}.{node.name}"
            items.append(_symbol_item(function_id, "function", node.name, node, parent_id=f"module:{module_name}"))
    return items


def _local_symbol_ids(tree: ast.AST, module_name: str) -> dict[str, str]:
    symbols: dict[str, str] = {}
    for item in _iter_symbol_defs(tree, module_name):
        simple_name = item["id"].split(".")[-1]
        if item["type"] == "method":
            continue
        symbols[simple_name] = item["id"]
    return symbols


def _iter_calls(tree: ast.AST, module_name: str) -> list[dict[str, Any]]:
    calls: list[dict[str, Any]] = []

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = [f"module:{module_name}"]
            self.class_stack: list[str] = []
            self.function_depth = 0

        def visit_ClassDef(self, node: ast.ClassDef) -> None:  # noqa: N802
            self.class_stack.append(node.name)
            self.scope.append(f"class:{module_name}.{node.name}")
            for child in node.body:
                self.visit(child)
            self.scope.pop()
            self.class_stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: N802
            self._visit_function(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:  # noqa: N802
            self._visit_function(node)

        def _visit_function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            if self.function_depth:
                return
            if self.class_stack:
                source_id = f"method:{module_name}.{self.class_stack[-1]}.{node.name}"
            else:
                source_id = f"function:{module_name}.{node.name}"
            self.function_depth += 1
            self.scope.append(source_id)
            for child in node.body:
                self.visit(child)
            self.scope.pop()
            self.function_depth -= 1

        def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
            calls.append({"source_id": self.scope[-1], "call": node})
            self.generic_visit(node)

    Visitor().visit(tree)
    return calls


def _import_bindings(
    tree: ast.AST,
    module: PythonModuleInfo,
    symbol_ids: set[str],
    module_ids: set[str],
) -> dict[str, str]:
    bindings: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_name = alias.name
                target = f"module:{module_name}"
                local_name = alias.asname or module_name.split(".")[0]
                if target in module_ids:
                    bindings[local_name] = target
                elif f"module:{local_name}" in module_ids:
                    bindings[local_name] = f"module:{local_name}"
        elif isinstance(node, ast.ImportFrom):
            imported_module = _resolve_import_from_module(module.module_name, node.module or "", node.level)
            for alias in node.names:
                if alias.name == "*":
                    continue
                local_name = alias.asname or alias.name
                candidates = [
                    f"function:{imported_module}.{alias.name}",
                    f"class:{imported_module}.{alias.name}",
                    f"module:{imported_module}.{alias.name}",
                ]
                for candidate in candidates:
                    if candidate in symbol_ids or candidate in module_ids:
                        bindings[local_name] = candidate
                        break
    return bindings


def _resolve_call_target(
    call: ast.Call,
    module: PythonModuleInfo,
    local_symbols: dict[str, str],
    symbol_ids: set[str],
) -> str:
    func = call.func
    if isinstance(func, ast.Name):
        name = func.id
        return module.import_bindings.get(name) or local_symbols.get(name, "")
    if isinstance(func, ast.Attribute):
        dotted = _attribute_path(func)
        if len(dotted) >= 2:
            owner = dotted[0]
            bound = module.import_bindings.get(owner)
            if bound and bound.startswith("module:"):
                module_parts = bound.removeprefix("module:").split(".")
                suffix_parts = dotted[1:-1]
                if suffix_parts and module_parts[-len(suffix_parts) :] == suffix_parts:
                    suffix_parts = []
                candidate_module = ".".join([*module_parts, *suffix_parts])
                candidate = f"function:{candidate_module}.{dotted[-1]}"
                return candidate if candidate in symbol_ids else ""
    return ""


def _attribute_path(node: ast.AST) -> list[str]:
    parts: list[str] = []
    current: ast.AST = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
        return list(reversed(parts))
    return []


def _adapter_summary(files: list[dict[str, Any]]) -> dict[str, str]:
    summary: dict[str, str] = {}
    for item in files:
        language = str(item.get("language") or "unknown")
        if language == "python":
            summary[language] = PYTHON_AST_ADAPTER
        elif language in {"markdown", "yaml", "json", "sql", "dbml", "toml"}:
            summary.setdefault(language, "structured_overlay")
        else:
            summary[language] = "file_only"
    return dict(sorted(summary.items()))


def _module_name_for_path(relative_path: str) -> str:
    path = Path(relative_path)
    parts = list(path.with_suffix("").parts)
    if parts and parts[-1] == "__init__":
        parts = parts[:-1]
    return ".".join(parts) if parts else path.stem


def _package_name_for_path(relative_path: str, package_dirs: set[str]) -> str | None:
    parent = str(Path(relative_path).parent).replace("\\", "/")
    parts = parent.split("/") if parent and parent != "." else []
    while parts:
        candidate = "/".join(parts)
        if candidate in package_dirs:
            return candidate.replace("/", ".")
        parts.pop()
    return None


def _resolve_import_from_module(current_module: str, module: str, level: int) -> str:
    if level <= 0:
        return module
    current_parts = current_module.split(".")
    base = current_parts[: max(0, len(current_parts) - level)]
    if module:
        base.extend(module.split("."))
    return ".".join(part for part in base if part)


def _import_line(tree: ast.AST, binding_name: str) -> int:
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if (alias.asname or alias.name.split(".")[0]) == binding_name:
                    return int(getattr(node, "lineno", 1))
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if (alias.asname or alias.name) == binding_name:
                    return int(getattr(node, "lineno", 1))
    return 1


def _call_name(call: ast.Call) -> str:
    if isinstance(call.func, ast.Name):
        return call.func.id
    if isinstance(call.func, ast.Attribute):
        dotted = _attribute_path(call.func)
        return ".".join(dotted) if dotted else call.func.attr
    return ""


def _is_test_source(relative_path: str, source_id: str) -> bool:
    path = relative_path.replace("\\", "/")
    return (
        "/tests/" in f"/{path}"
        or "/fixtures/" in f"/{path}"
        or "/eval-fixtures/" in f"/{path}"
        or Path(path).name.startswith("test_")
        or source_id.split(".")[-1].startswith("test_")
    )


def _safe_unresolved_calls(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "name": _safe_call_label(str(item.get("name") or "")),
            "relative_path": str(item.get("relative_path") or ""),
            "line": int(item.get("line") or 1),
            "scope": str(item.get("scope") or ""),
            "status": "unsupported",
        }
        for item in items
    ]


def _safe_call_label(value: str) -> str:
    if not value:
        return "unknown"
    if any(term in value.lower() for term in ["secret", "token", "password", "key"]):
        return "redacted_call"
    return value[:80]


def _symbol_item(symbol_id: str, node_type: str, label: str, node: ast.AST, *, parent_id: str) -> dict[str, Any]:
    return {
        "id": symbol_id,
        "type": node_type,
        "label": label,
        "start_line": int(getattr(node, "lineno", 1)),
        "end_line": int(getattr(node, "end_lineno", getattr(node, "lineno", 1))),
        "parent_id": parent_id,
    }


def _node(
    node_id: str,
    *,
    node_type: str,
    label: str,
    language: str,
    path: str,
    source_span: dict[str, Any],
    observation_id: str,
) -> dict[str, Any]:
    return {
        "id": node_id,
        "type": node_type,
        "label": label,
        "status": "current",
        "language": language,
        "path": path,
        "source_spans": [source_span],
        "observation_ids": [observation_id],
    }


def _span(relative_path: str, start_line: int, end_line: int, fingerprint: str) -> dict[str, Any]:
    return {
        "relative_path": relative_path,
        "start_line": start_line,
        "end_line": max(start_line, end_line),
        "fingerprint": fingerprint,
    }


def _edge(
    scan_id: str,
    *,
    edge_type: str,
    source: str,
    target: str,
    relative_path: str,
    line: int,
    fingerprint: str,
    extractor: str,
    confidence: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    edge_id = _edge_id(edge_type, source, target, relative_path=relative_path, line=line)
    observation = _observation(
        scan_id,
        subject_id=edge_id,
        relative_path=relative_path,
        start_line=max(1, line),
        end_line=max(1, line),
        fingerprint=fingerprint,
        extractor=extractor,
        confidence=confidence,
    )
    return (
        {
            "id": edge_id,
            "type": edge_type,
            "source": source,
            "target": target,
            "confidence": confidence,
            "status": "current",
            "observation_ids": [observation["id"]],
            "fingerprint": fingerprint,
        },
        observation,
    )


def _observation(
    scan_id: str,
    *,
    subject_id: str,
    relative_path: str,
    start_line: int,
    end_line: int,
    fingerprint: str,
    extractor: str,
    confidence: str,
) -> dict[str, Any]:
    return build_observation_record(
        scan_id=scan_id,
        relative_path=relative_path,
        span={"start_line": start_line, "end_line": max(start_line, end_line)},
        fingerprint=fingerprint,
        extractor=extractor,
        confidence=confidence,
        redaction_status="redacted",
        subject_id=subject_id,
    )


def _edge_id(edge_type: str, source: str, target: str, *, relative_path: str, line: int) -> str:
    seed = json.dumps(
        {"type": edge_type, "source": source, "target": target, "relative_path": relative_path, "line": line},
        sort_keys=True,
    )
    return "edge:" + hashlib.sha256(seed.encode("utf-8")).hexdigest()[:24]
