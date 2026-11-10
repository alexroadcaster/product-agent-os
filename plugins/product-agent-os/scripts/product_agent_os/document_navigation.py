"""Read-only navigation, reference provenance and lossless task-plan split design.

No index is a task-status authority. Existing project filenames remain canonical;
domain paths below are suggestions only when their explicit trigger applies.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

from product_agent_os.control_plane_compaction import _path

DOMAINS = {
    'architecture': ('docs/architecture', 'architect', 'boundary or topology change'),
    'decisions': ('docs/decisions', 'decision owner', 'durable trade-off'),
    'api': ('docs/api', 'API owner', 'public API contract'),
    'data': ('docs/data', 'data owner', 'schema or migration'),
    'operations': ('docs/operations', 'operator', 'operated service or recovery'),
    'verification': ('docs/evidence', 'tester', 'required reproducible evidence'),
    'history': ('docs/history', 'document owner', 'closed cycle details'),
}


def documentation_inventory(root: Path, *, signals: dict[str, bool]) -> dict[str, Any]:
    """Reuse known entrypoints, then propose only explicitly applicable domains."""
    index = next((p for p in ('docs/index.md', 'docs/README.md', 'docs/control-plane/index.md')
                  if _path(root, p).is_file()), None)
    aliases = {'decisions': ('docs/adr',), 'operations': ('docs/runbooks', 'docs/ops'),
               'verification': ('docs/testing',), 'history': ('docs/archive',)}
    domains = {}
    for key, (path, owner, trigger) in DOMAINS.items():
        if signals.get(key) is not True:
            continue
        existing = next((name for name in (path, *aliases.get(key, ()))
                         if (root / name).is_dir() and not (root / name).is_symlink()
                         and not (root / name).is_junction()), None)
        domains[key] = {'suggested_path': existing or path, 'canonical_source': existing,
                        'owner': owner, 'trigger': trigger}
    sources = [name for name in ('REQUIREMENTS.md', 'PLAN.md', 'TEST.md', 'EVALS.md', 'RUNLOG.md')
               if _path(root, name).is_file()]
    return {'index': index, 'index_action': 'reuse' if index else 'proposal_needed',
            'needed_domains': domains, 'write_policy': 'read_only',
            'current_source_links': sources,
            'authority': 'navigation_not_task_state'}


def _headings(text: str) -> list[tuple[int, str]]:
    """GFM-style IDs for supported plain Markdown; preserve explicit HTML anchors."""
    headings, counts, offset = [], {}, 0
    fence = None
    for line in text.splitlines(keepends=True):
        stripped = line.lstrip()
        marker = re.match(r'(`{3,}|~{3,})', stripped)
        if marker:
            if fence is None:
                fence = marker[1][0]
            elif marker[1][0] == fence:
                fence = None
        elif fence is None:
            match = re.match(r'^#{1,6}\s+(.+?)\s*#*\s*$', line.rstrip())
            if match:
                slug = re.sub(r'[^\w\- ]', '', match[1].lower()).replace(' ', '-')
                count = counts.get(slug, 0)
                counts[slug] = count + 1
                headings.append((offset, slug + (f'-{count}' if count else '')))
            for anchor in re.findall(r'<a\s+id="([\w-]+)"\s*>', line):
                headings.append((offset, anchor))
        offset += len(line.encode('utf-8'))
    return headings


def task_plan_moves(root: Path, source: str, directory: str, *, limit: int = 40000) -> list[dict[str, Any]]:
    """Split at complete task cards; oversized single cards require manual review.

    Source IDs/dependencies stay in exact card bytes. Source anchor stubs route
    old links to new local anchors. This is a proposal, never an automatic split.
    """
    raw = _path(root, source).read_bytes()
    text = raw.decode('utf-8')
    starts = [len(text[:m.start()].encode('utf-8')) for m in re.finditer(r'^### Task `[^`]+`\s*$', text, re.M)]
    if not starts or not 0 < limit <= 40000:
        raise ValueError('no supported task cards or invalid byte budget')
    chunks = []
    chunk_start, chunk_end = starts[0], starts[0]
    for start, end in zip(starts, starts[1:] + [len(raw)]):
        if end - start > limit:
            raise ValueError('single task card exceeds budget; manual decomposition required')
        if end - chunk_start > limit and chunk_end > chunk_start:
            chunks.append((chunk_start, chunk_end))
            chunk_start = start
        chunk_end = end
    chunks.append((chunk_start, chunk_end))
    original_headings = _headings(text)
    moves = []
    for index, (start, end) in enumerate(chunks, 1):
        destination = f'{directory}/part-{index:03}.md'
        if _path(root, destination).exists():
            raise ValueError('split destination already exists; reuse requires explicit mapping')
        old_ids = [slug for offset, slug in original_headings if start <= offset < end]
        new_ids = [slug for _, slug in _headings(raw[start:end].decode('utf-8'))]
        if len(old_ids) != len(new_ids):
            raise ValueError('unsupported heading/fence split; manual anchor mapping required')
        moves.append({'source': source, 'start': start, 'end': end, 'destination': destination,
                      'classification': 'active_detail', 'owner': 'task-plan owner',
                      'reason': 'bounded task groups with original IDs and dependency edges',
                      'anchors': dict(zip(old_ids, new_ids))})
    return moves


def split_source_references(plan: dict[str, Any], source_reference: dict[str, Any]) -> list[dict[str, Any]]:
    """Propose revision pins for the existing PLAN selector, not a status registry.

    The owner replaces only the matching source reference after reviewed apply.
    All other sources/prefix scopes stay unchanged. This helper never writes.
    """
    from product_agent_os.control_plane_compaction import _decode
    source = source_reference['path']
    candidates = {source} | {m['destination'] for m in plan['moves'] if m['source'] == source}
    references = []
    for item in plan['files']:
        if item['path'] in candidates and re.search(rb'^### Task `[^`]+`', _decode(item['after']), re.M):
            ref = dict(source_reference)
            ref.update(path=item['path'], revision=item['after_digest'])
            references.append(ref)
    if not references or len(references) > 32:
        raise ValueError('split requires a bounded nonempty task source set')
    return references


def check_local_links(root: Path, paths: list[str], *, contents: dict[str, bytes] | None = None) -> list[str]:
    """Check local Markdown links/anchors without network or repository inference."""
    errors = []
    contents = contents or {}
    for name in paths:
        path = _path(root, name)
        text = contents[name].decode('utf-8') if name in contents else path.read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^)]+)\)', text):
            target = target.strip('<>')
            parts = urlsplit(target)
            if parts.scheme in {'http', 'https', 'mailto'}:
                continue
            if parts.scheme or parts.netloc:
                errors.append(f'{name}: unsupported link')
                continue
            candidate = path.parent / unquote(parts.path) if parts.path else path
            try:
                relative = candidate.resolve().relative_to(root.resolve()).as_posix()
                linked = _path(root, relative)
                if relative not in contents and not linked.is_file():
                    raise ValueError('missing link')
                linked_text = contents[relative].decode('utf-8') if relative in contents else linked.read_text(encoding='utf-8')
                if parts.fragment and unquote(parts.fragment) not in {slug for _, slug in _headings(linked_text)}:
                    raise ValueError('missing anchor')
            except (OSError, ValueError, UnicodeError):
                errors.append(f'{name}: unresolved {target}')
    return errors


def check_reference(root: Path, record: dict[str, Any], *, repositories: dict[str, Path] | None = None) -> dict[str, str]:
    """Check explicit source identity; missing evidence is never an implicit pass."""
    kind = record.get('kind')
    if record.get('profile') and (record['profile'] != 'offline_bundle' or not record.get('source_digest')):
        return {'status': 'unknown'}
    if kind == 'cross_repository':
        repository = record.get('repository')
        if (repository not in (repositories or {}) or not record.get('source_digest')
                or not record.get('revision') or not record.get('claim_boundary')):
            return {'status': 'unknown'}
        root = repositories[repository]
    elif kind not in {'mirror', 'required_evidence', 'optional_evidence'}:
        return {'status': 'unknown'}
    try:
        path = _path(root, record['path'])
        if not path.is_file():
            return {'status': 'unavailable_optional' if kind == 'optional_evidence' else 'missing'}
        raw = path.read_bytes()
        if kind == 'mirror':
            if path.name.lower() in {'agents.md', 'agents.override.md'}:
                return {'status': 'conflict', 'reason': 'instruction mirror changes discovery scope'}
            source = _path(root, record['source']).read_bytes()
            if hashlib.sha256(source).hexdigest() != record.get('source_digest') or raw != source:
                return {'status': 'stale'}
        elif record.get('source_digest') and hashlib.sha256(raw).hexdigest() != record['source_digest']:
            return {'status': 'stale'}
        if not raw.strip():
            return {'status': 'missing'}
    except (OSError, ValueError, KeyError, TypeError):
        return {'status': 'unknown'}
    result = {'status': 'verified', 'claim_ceiling': 'artifact_integrity_only'}
    if kind == 'mirror':
        result.update(source=record['source'], revision='sha256:' + record['source_digest'])
    return result


def duplicate_blocks(root: Path, paths: list[str]) -> list[dict[str, Any]]:
    """Exact paragraph duplicates are review hints, never a deletion instruction."""
    findings = []
    for name in paths:
        text = _path(root, name).read_text(encoding='utf-8')
        seen: dict[str, list[int]] = {}
        for position, block in enumerate(re.split(r'\n\s*\n', text), 1):
            block = block.strip()
            if len(block) >= 24 and not block.startswith(('#', '```', '|', '<!--')):
                digest = hashlib.sha256(block.encode('utf-8')).hexdigest()
                seen.setdefault(digest, []).append(position)
        for digest, positions in seen.items():
            if len(positions) > 1:
                findings.append({'path': name, 'block_digest': digest, 'paragraphs': positions,
                                 'action': 'owner_review_only; semantic dedup requires review'})
    return findings
