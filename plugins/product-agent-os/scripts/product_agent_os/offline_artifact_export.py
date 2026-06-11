"""Project-scoped export contract for generated offline HTML artifacts."""

from __future__ import annotations

from pathlib import Path, PureWindowsPath
from typing import Any


class OfflineArtifactExportError(RuntimeError):
    pass


def build_html_export_contract(
    workspace: str | Path,
    *,
    artifact_id: str,
    default_relative_path: str,
    requested_path: str | Path | None = None,
    explicit_path_requested: bool = False,
    approval_ref: str = "",
) -> dict[str, Any]:
    """Describe the final user-facing export destination without writing files."""

    workspace_path = Path(workspace).resolve()
    destination, destination_scope = _resolve_destination(
        workspace_path,
        default_relative_path=default_relative_path,
        requested_path=requested_path,
        explicit_path_requested=explicit_path_requested,
    )
    approval_required = []
    if not approval_ref:
        approval_required.append("explicit approval required before writing final HTML export")
    if destination_scope == "explicit_external_path" and not explicit_path_requested:
        approval_required.append("external final destination requires an explicit user-requested path")
    return {
        "artifact_id": str(artifact_id),
        "artifact_type": "offline_html",
        "final_destination_policy": "project_scoped_or_explicit_user_path",
        "workspace": str(workspace_path),
        "default_relative_path": default_relative_path,
        "requested_path": str(requested_path or ""),
        "explicit_path_requested": bool(explicit_path_requested),
        "destination": str(destination),
        "destination_scope": destination_scope,
        "approval_ref": approval_ref,
        "approval_required": approval_required,
        "stage_policy": "external stage allowed only as intermediate build location",
        "write_policy": "approval_required" if approval_required else "ready_to_write",
    }


def write_html_export(
    workspace: str | Path,
    *,
    artifact_id: str,
    default_relative_path: str,
    html_text: str,
    requested_path: str | Path | None = None,
    explicit_path_requested: bool = False,
    approval_ref: str = "",
) -> dict[str, Any]:
    """Write a final HTML artifact only after an explicit export approval is recorded."""

    contract = build_html_export_contract(
        workspace,
        artifact_id=artifact_id,
        default_relative_path=default_relative_path,
        requested_path=requested_path,
        explicit_path_requested=explicit_path_requested,
        approval_ref=approval_ref,
    )
    if contract["approval_required"]:
        raise OfflineArtifactExportError("; ".join(contract["approval_required"]))
    destination = Path(contract["destination"])
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html_text, encoding="utf-8")
    contract["write_policy"] = "written"
    return contract


def _resolve_destination(
    workspace: Path,
    *,
    default_relative_path: str,
    requested_path: str | Path | None,
    explicit_path_requested: bool,
) -> tuple[Path, str]:
    default_path = _safe_relative_path(default_relative_path)
    if requested_path is None or str(requested_path).strip() == "":
        return (workspace / default_path).resolve(), "project_default"

    requested_text = str(requested_path)
    if _unsafe_relative_path(requested_text):
        requested = Path(requested_path).resolve()
        if not explicit_path_requested:
            raise OfflineArtifactExportError("absolute or escaping export path requires explicit_path_requested")
        return requested, "explicit_external_path" if not requested.is_relative_to(workspace) else "explicit_project_path"

    requested = (workspace / Path(requested_text)).resolve()
    if not requested.is_relative_to(workspace):
        raise OfflineArtifactExportError("export path escapes workspace")
    return requested, "explicit_project_path"


def _safe_relative_path(value: str) -> Path:
    if _unsafe_relative_path(value):
        raise OfflineArtifactExportError(f"invalid default export path: {value}")
    return Path(value)


def _unsafe_relative_path(value: str) -> bool:
    if not value:
        return True
    path = Path(value)
    windows_path = PureWindowsPath(value)
    return (
        path.is_absolute()
        or bool(path.drive)
        or bool(path.root)
        or windows_path.is_absolute()
        or bool(windows_path.drive)
        or bool(windows_path.root)
        or ".." in path.parts
    )
