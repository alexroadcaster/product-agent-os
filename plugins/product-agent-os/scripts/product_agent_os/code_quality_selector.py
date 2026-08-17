"""Select conservative code-quality profiles from declared project inventory."""

from __future__ import annotations

from dataclasses import dataclass


PRESENT_UNVERIFIED = "present_unverified"
APPLICABLE_MISSING = "applicable_missing"
NOT_APPLICABLE = "not_applicable"
FAMILY_ORDER = (
    "python",
    "javascript_typescript",
    "compiled_systems",
    "enterprise_oop",
)
CATEGORY_ORDER = ("formatter", "linter", "type_checker", "test_runner", "build_tool")
FAMILY_MARKERS = {
    "python": (("pyproject.toml",), ("python",)),
    "javascript_typescript": (("package.json", "tsconfig.json"), ("javascript", "typescript")),
    "compiled_systems": (("cargo.toml", "go.mod"), ("go", "rust")),
    "enterprise_oop": (("pom.xml", ".csproj"), ("java", "csharp")),
}
FAMILY_MARKER_LANGUAGES = {
    "python": (("pyproject.toml", "python"),),
    "javascript_typescript": (
        ("package.json", "javascript"),
        ("tsconfig.json", "typescript"),
    ),
    "compiled_systems": (("cargo.toml", "rust"), ("go.mod", "go")),
    "enterprise_oop": (("pom.xml", "java"), (".csproj", "csharp")),
}
TOOL_TRACERS = {
    "black": ("python", "formatter"),
    "ruff": ("python", "linter"),
    "mypy": ("python", "type_checker"),
    "pytest": ("python", "test_runner"),
    "hatch": ("python", "build_tool"),
    "prettier": ("javascript_typescript", "formatter"),
    "eslint": ("javascript_typescript", "linter"),
    "typescript": ("javascript_typescript", "type_checker"),
    "vitest": ("javascript_typescript", "test_runner"),
    "vite": ("javascript_typescript", "build_tool"),
    "gofmt": ("compiled_systems", "formatter"),
    "golangci-lint": ("compiled_systems", "linter"),
    "go vet": ("compiled_systems", "type_checker"),
    "go test": ("compiled_systems", "test_runner"),
    "go build": ("compiled_systems", "build_tool"),
    "rustfmt": ("compiled_systems", "formatter"),
    "clippy": ("compiled_systems", "linter"),
    "rustc": ("compiled_systems", "type_checker"),
    "cargo test": ("compiled_systems", "test_runner"),
    "cargo build": ("compiled_systems", "build_tool"),
    "google-java-format": ("enterprise_oop", "formatter"),
    "checkstyle": ("enterprise_oop", "linter"),
    "javac": ("enterprise_oop", "type_checker"),
    "junit": ("enterprise_oop", "test_runner"),
    "maven": ("enterprise_oop", "build_tool"),
    "dotnet format": ("enterprise_oop", "formatter"),
    "stylecop": ("enterprise_oop", "linter"),
    "csc": ("enterprise_oop", "type_checker"),
    "dotnet test": ("enterprise_oop", "test_runner"),
    "dotnet build": ("enterprise_oop", "build_tool"),
}
TOOL_LANGUAGES = {
    "black": "python",
    "ruff": "python",
    "mypy": "python",
    "pytest": "python",
    "hatch": "python",
    "typescript": "typescript",
    "gofmt": "go",
    "golangci-lint": "go",
    "go vet": "go",
    "go test": "go",
    "go build": "go",
    "rustfmt": "rust",
    "clippy": "rust",
    "rustc": "rust",
    "cargo test": "rust",
    "cargo build": "rust",
    "google-java-format": "java",
    "checkstyle": "java",
    "javac": "java",
    "junit": "java",
    "maven": "java",
    "dotnet format": "csharp",
    "stylecop": "csharp",
    "csc": "csharp",
    "dotnet test": "csharp",
    "dotnet build": "csharp",
}


@dataclass(frozen=True)
class DeclaredToolSignal:
    """A tool name declared by a project-owned source file."""

    name: str
    source: str


@dataclass(frozen=True)
class ProjectCommandSignal:
    """A project-provided utility command discovered without executing it."""

    name: str
    command: str
    source: str


@dataclass(frozen=True)
class ProjectInventory:
    """The pure input contract for code-quality profile selection."""

    paths: tuple[str, ...]
    declared_tools: tuple[DeclaredToolSignal, ...]
    project_commands: tuple[ProjectCommandSignal, ...]


@dataclass(frozen=True)
class ToolEvidence:
    """Unverified evidence connecting a declared tool to a profile category."""

    name: str
    status: str
    sources: tuple[str, ...]
    proposed_commands: tuple[str, ...]


@dataclass(frozen=True)
class CategoryProfile:
    """The conservative state of one quality category for a stack family."""

    category: str
    status: str
    tools: tuple[ToolEvidence, ...]
    reason: str


@dataclass(frozen=True)
class StackProfile:
    """A detected stack family and its applicable quality categories."""

    family: str
    languages: tuple[str, ...]
    status: str
    marker_evidence: tuple[str, ...]
    categories: tuple[CategoryProfile, ...]


@dataclass(frozen=True)
class ProjectUtilityProfile:
    """A discovered project utility kept inert until a later execution gate."""

    name: str
    status: str
    source: str
    proposed_command: str


@dataclass(frozen=True)
class CodeQualityProfile:
    """The complete, unverified selection result for a project inventory."""

    schema_version: str
    inventory_status: str
    stack_profiles: tuple[StackProfile, ...]
    project_utilities: tuple[ProjectUtilityProfile, ...]
    gaps: tuple[str, ...]
    evidence_ceiling: str


def select_code_quality_profile(inventory: ProjectInventory) -> CodeQualityProfile:
    """Build a deterministic profile without reading files or running tools."""
    _validate_inventory_types(inventory)
    _validate_inventory_values(inventory)
    if not inventory.paths and not inventory.declared_tools and not inventory.project_commands:
        return CodeQualityProfile(
            schema_version="code_quality_profile_v1",
            inventory_status=NOT_APPLICABLE,
            stack_profiles=tuple(_not_applicable_stack(family) for family in FAMILY_ORDER),
            project_utilities=(),
            gaps=("no_stack_or_tool_signals",),
            evidence_ceiling="declared inventory only; no tool execution or verification",
        )
    paths = {_normalize_path(path) for path in inventory.paths}
    declared_tools = _normalized_tools(inventory.declared_tools)
    active_families = {
        family
        for family in FAMILY_ORDER
        if _marker_evidence(family, paths)
        or any(
            TOOL_TRACERS.get(tool.name, (None, None))[0] == family
            for tool in declared_tools
        )
    }
    utilities = _project_utilities(inventory.project_commands)
    if not active_families:
        inventory_status = PRESENT_UNVERIFIED if utilities else APPLICABLE_MISSING
        return CodeQualityProfile(
            schema_version="code_quality_profile_v1",
            inventory_status=inventory_status,
            stack_profiles=tuple(_not_applicable_stack(family) for family in FAMILY_ORDER),
            project_utilities=utilities,
            gaps=_unknown_gaps(paths, declared_tools),
            evidence_ceiling="declared inventory only; no tool execution or verification",
        )
    stack_profiles = tuple(
        _stack_profile(family, paths, declared_tools)
        if family in active_families
        else _not_applicable_stack(family)
        for family in FAMILY_ORDER
    )
    gaps = tuple(
        f"{stack.family}:{category.category}"
        for stack in stack_profiles
        for category in stack.categories
        if category.status == APPLICABLE_MISSING
    ) + _compiled_language_gaps(paths, declared_tools) + _enterprise_language_gaps(
        paths, declared_tools
    )
    return CodeQualityProfile(
        schema_version="code_quality_profile_v1",
        inventory_status=PRESENT_UNVERIFIED,
        stack_profiles=stack_profiles,
        project_utilities=utilities,
        gaps=gaps,
        evidence_ceiling="declared inventory only; no tool execution or verification",
    )


def code_quality_profile_as_dict(profile: CodeQualityProfile) -> dict[str, object]:
    """Serialize a profile using the stable public schema field order."""
    return {
        "schema_version": profile.schema_version,
        "inventory_status": profile.inventory_status,
        "stack_profiles": [
            {
                "family": stack.family,
                "languages": list(stack.languages),
                "status": stack.status,
                "marker_evidence": list(stack.marker_evidence),
                "categories": [
                    {
                        "category": category.category,
                        "status": category.status,
                        "tools": [
                            {
                                "name": tool.name,
                                "status": tool.status,
                                "sources": list(tool.sources),
                                "proposed_commands": list(tool.proposed_commands),
                            }
                            for tool in category.tools
                        ],
                        "reason": category.reason,
                    }
                    for category in stack.categories
                ],
            }
            for stack in profile.stack_profiles
        ],
        "project_utilities": [
            {
                "name": utility.name,
                "status": utility.status,
                "source": utility.source,
                "proposed_command": utility.proposed_command,
            }
            for utility in profile.project_utilities
        ],
        "gaps": list(profile.gaps),
        "evidence_ceiling": profile.evidence_ceiling,
    }


def _stack_profile(
    family: str,
    paths: set[str],
    declared_tools: tuple[DeclaredToolSignal, ...],
) -> StackProfile:
    marker_evidence = _marker_evidence(family, paths)
    categories = tuple(
        _category_profile(family, category, declared_tools) for category in CATEGORY_ORDER
    )
    return StackProfile(
        family=family,
        languages=_detected_languages(family, marker_evidence, declared_tools),
        status=PRESENT_UNVERIFIED,
        marker_evidence=marker_evidence,
        categories=categories,
    )


def _not_applicable_stack(family: str) -> StackProfile:
    """Represent a known family that the empty inventory cannot assess."""
    _, languages = FAMILY_MARKERS[family]
    categories = tuple(
        CategoryProfile(category, NOT_APPLICABLE, (), "no inventory signals")
        for category in CATEGORY_ORDER
    )
    return StackProfile(
        family=family,
        languages=languages,
        status=NOT_APPLICABLE,
        marker_evidence=(),
        categories=categories,
    )


def _category_profile(
    family: str, category: str, declared_tools: tuple[DeclaredToolSignal, ...]
) -> CategoryProfile:
    matches = tuple(
        ToolEvidence(
            name=tool.name,
            status=PRESENT_UNVERIFIED,
            sources=(tool.source,),
            proposed_commands=(),
        )
        for tool in declared_tools
        if TOOL_TRACERS.get(tool.name) == (family, category)
    )
    if matches:
        return CategoryProfile(category, PRESENT_UNVERIFIED, matches, "declared tool evidence")
    return CategoryProfile(category, APPLICABLE_MISSING, (), "no declared tool evidence")


def _marker_evidence(family: str, paths: set[str]) -> tuple[str, ...]:
    markers, _ = FAMILY_MARKERS[family]
    return tuple(
        path
        for path in sorted(paths)
        if any(_matches_marker(path, marker) for marker in markers)
    )


def _matches_marker(path: str, marker: str) -> bool:
    """Match a marker as a filename, allowing only the declared suffix markers."""
    basename = path.rsplit("/", 1)[-1]
    return basename.endswith(marker) if marker.startswith(".") else basename == marker


def _detected_languages(
    family: str,
    marker_evidence: tuple[str, ...],
    declared_tools: tuple[DeclaredToolSignal, ...],
) -> tuple[str, ...]:
    """Return only languages supported by concrete marker or tool evidence."""
    _, languages = FAMILY_MARKERS[family]
    detected = {
        language
        for marker, language in FAMILY_MARKER_LANGUAGES[family]
        if any(_matches_marker(path, marker) for path in marker_evidence)
    }
    detected.update(
        TOOL_LANGUAGES[tool.name]
        for tool in declared_tools
        if TOOL_TRACERS.get(tool.name, (None, None))[0] == family
        and tool.name in TOOL_LANGUAGES
    )
    return tuple(language for language in languages if language in detected)


def _project_utilities(
    commands: tuple[ProjectCommandSignal, ...]
) -> tuple[ProjectUtilityProfile, ...]:
    """Keep declared project utilities even when no stack can be classified."""
    return tuple(
        ProjectUtilityProfile(
            name=command.name.strip().lower(),
            status=PRESENT_UNVERIFIED,
            source=command.source.strip(),
            proposed_command=command.command.strip(),
        )
        for command in _normalized_commands(commands)
    )


def _normalized_tools(
    tools: tuple[DeclaredToolSignal, ...]
) -> tuple[DeclaredToolSignal, ...]:
    normalized = {
        (tool.name.strip().lower(), _normalize_path(tool.source)) for tool in tools
    }
    return tuple(
        DeclaredToolSignal(name=name, source=source)
        for name, source in sorted(normalized)
    )


def _validate_inventory_types(inventory: ProjectInventory) -> None:
    """Reject malformed inventory containers and nested field types early."""
    if not isinstance(inventory, ProjectInventory):
        raise TypeError("inventory must be a ProjectInventory")
    if not all(
        isinstance(value, tuple)
        for value in (
            inventory.paths,
            inventory.declared_tools,
            inventory.project_commands,
        )
    ):
        raise TypeError("inventory fields must be tuples")
    if not all(isinstance(path, str) for path in inventory.paths):
        raise TypeError("inventory paths must contain strings")
    if not all(
        isinstance(tool, DeclaredToolSignal)
        and isinstance(tool.name, str)
        and isinstance(tool.source, str)
        for tool in inventory.declared_tools
    ):
        raise TypeError("declared tools must contain string signals")
    if not all(
        isinstance(command, ProjectCommandSignal)
        and isinstance(command.name, str)
        and isinstance(command.command, str)
        and isinstance(command.source, str)
        for command in inventory.project_commands
    ):
        raise TypeError("project commands must contain string signals")


def _validate_inventory_values(inventory: ProjectInventory) -> None:
    """Reject malformed relative paths, empty signals, and command conflicts."""
    for path in inventory.paths:
        _validate_relative_path(path, "inventory path")
    for tool in inventory.declared_tools:
        if not tool.name.strip():
            raise ValueError("declared tool name must not be empty")
        _validate_relative_path(tool.source, "declared tool source")
    command_values: dict[tuple[str, str], str] = {}
    for command in inventory.project_commands:
        if not command.name.strip() or not command.command.strip():
            raise ValueError("project command name and command must not be empty")
        _validate_relative_path(command.source, "project command source")
        key = (command.name.strip().lower(), _normalize_path(command.source))
        previous = command_values.setdefault(key, command.command.strip())
        if previous != command.command.strip():
            raise ValueError("conflicting project commands share a name and source")


def _validate_relative_path(path: str, label: str) -> None:
    """Require a non-empty normalized relative path without parent traversal."""
    normalized = path.strip().replace("\\", "/")
    if not normalized or "\0" in normalized:
        raise ValueError(f"{label} must be a non-empty path without NUL")
    if normalized.startswith("/") or (
        len(normalized) >= 3
        and normalized[0].isalpha()
        and normalized[1] == ":"
        and normalized[2] == "/"
    ):
        raise ValueError(f"{label} must be relative")
    if ".." in normalized.split("/"):
        raise ValueError(f"{label} must not contain parent traversal")


def _normalized_commands(
    commands: tuple[ProjectCommandSignal, ...]
) -> tuple[ProjectCommandSignal, ...]:
    """Deduplicate identical commands while preserving their submitted display source."""
    normalized: dict[tuple[str, str, str], ProjectCommandSignal] = {}
    for command in commands:
        name = command.name.strip().lower()
        source = _normalize_path(command.source)
        proposed_command = command.command.strip()
        normalized.setdefault(
            (name, proposed_command, source),
            ProjectCommandSignal(name, proposed_command, command.source.strip()),
        )
    return tuple(command for _, command in sorted(normalized.items()))


def _unknown_gaps(
    paths: set[str], declared_tools: tuple[DeclaredToolSignal, ...]
) -> tuple[str, ...]:
    """Describe unmapped inventory signals without assigning them a stack category."""
    return tuple(
        [f"unknown_path:{path}" for path in sorted(paths)]
        + [f"unmapped_tool:{tool.name}" for tool in declared_tools]
    )


def _compiled_language_gaps(
    paths: set[str], declared_tools: tuple[DeclaredToolSignal, ...]
) -> tuple[str, ...]:
    """Report missing categories for each detected Go or Rust language."""
    active_languages = _detected_languages(
        "compiled_systems", _marker_evidence("compiled_systems", paths), declared_tools
    )
    return tuple(
        f"compiled_systems:{language}:{category}"
        for language in active_languages
        for category in CATEGORY_ORDER
        if not any(
            TOOL_TRACERS.get(tool.name) == ("compiled_systems", category)
            and TOOL_LANGUAGES.get(tool.name) == language
            for tool in declared_tools
        )
    )


def _enterprise_language_gaps(
    paths: set[str], declared_tools: tuple[DeclaredToolSignal, ...]
) -> tuple[str, ...]:
    """Report missing categories for each detected Java or C# language."""
    active_languages = _detected_languages(
        "enterprise_oop", _marker_evidence("enterprise_oop", paths), declared_tools
    )
    return tuple(
        f"enterprise_oop:{language}:{category}"
        for language in active_languages
        for category in CATEGORY_ORDER
        if not any(
            TOOL_TRACERS.get(tool.name) == ("enterprise_oop", category)
            and TOOL_LANGUAGES.get(tool.name) == language
            for tool in declared_tools
        )
    )


def _normalize_path(path: str) -> str:
    """Normalize a relative inventory path without accessing the filesystem."""
    return path.strip().replace("\\", "/").lower()
