"""Reviewed lossless byte moves with a local recovery journal.

No semantic deletion/summarization, background execution or multi-file ACID claim.
The caller supplies reviewed byte ranges and owns approval/exclusive access to
the workspace; the lock coordinates this tool, not arbitrary external editors.
"""
from __future__ import annotations

import base64
import difflib
import json
import os
import re
import tomllib
from pathlib import Path, PurePosixPath
from typing import Any, Callable
from urllib.parse import quote

from product_agent_os.stage_manifest import content_digest, canonical_json
from product_agent_os.control_plane_documents import is_detailed_planning_matrix

JOURNAL_ROOT = '.codex/product-agent-os/compaction'
LOCK = JOURNAL_ROOT + '/writer.lock'


def _pointer(root: Path, source: str, destination: str, anchors: dict[str, str] | None = None) -> bytes:
    link = os.path.relpath(root / destination, (root / source).parent).replace('\\', '/')
    lines = [f'\n[Preserved source block]({quote(link)})\n']
    for old, new in (anchors or {}).items():
        if not all(isinstance(value, str) and re.fullmatch(r'[\w-]+', value) for value in (old, new)):
            raise ValueError('invalid anchor migration')
        lines.append(f'<a id="{old}"></a>\n[Moved section]({quote(link)}#{quote(new)})\n')
    return ''.join(lines).encode('utf-8')


def _authority(root: Path, paths: list[str]) -> None:
    """Optional M1 handshake: unknown/frozen/SQL projections are never file writers.

    M1 must declare every task projection before cutover. This local handshake
    does not claim compatibility with an unimplemented service/domain adapter.
    """
    config = _path(root, '.codex/config.toml')
    data = tomllib.loads(config.read_text(encoding='utf-8')) if config.is_file() else {}
    policy = data.get('product_agent_os', {}).get('documents', {})
    mode = policy.get('authority', 'files')
    projections = policy.get('task_projections', [])
    if mode not in {'files', 'sql', 'frozen'} or not isinstance(projections, list):
        raise ValueError('unknown document authority')
    if mode != 'files' and (mode == 'frozen' or any(p in projections for p in paths)):
        raise ValueError('document authority forbids file mutation')


def _path(root: Path, relative: str) -> Path:
    """Reject aliases and redirected paths before any read or write."""
    if not isinstance(relative, str) or not relative or '\\' in relative or ':' in relative:
        raise ValueError('invalid relative path')
    parts = PurePosixPath(relative).parts
    if PurePosixPath(relative).as_posix() != relative:
        raise ValueError('noncanonical path alias')
    if relative.startswith('/') or '..' in parts or '.' in relative.split('/'):
        raise ValueError('path escapes workspace')
    path = root
    for part in parts:
        if part.endswith((' ', '.')):
            raise ValueError('ambiguous Windows path')
        path = path / part
        if path.is_symlink() or path.is_junction():
            raise ValueError('redirected path forbidden')
        if path.is_file() and path.stat().st_nlink > 1:
            raise ValueError('hardlink forbidden')
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path escapes workspace')
    if path.exists() and not path.is_file():
        raise ValueError('regular file required')
    return path


def _budget(root: Path, name: str, limit: int, content: bytes) -> int | None:
    """Never relax a stricter project policy, including after proposal review."""
    if type(limit) is not int or not 0 < limit <= 40000:
        raise ValueError('invalid document budget')
    config = _path(root, '.codex/config.toml')
    data = tomllib.loads(config.read_text(encoding='utf-8')) if config.is_file() else {}
    limits = data.get('product_agent_os', {}).get('documents', {}).get('limits', {})
    if not isinstance(limits, dict):
        raise ValueError('invalid project budgets')
    value = limits.get(name, limit)
    if type(value) is not int or value < 1:
        raise ValueError('invalid project budget')
    if name not in limits and is_detailed_planning_matrix(name, content.decode('utf-8')):
        return None  # Size exception is not authority to move or summarize data.
    return min(limit, value)


def _exceeds_budget(root: Path, name: str, content: bytes, limit: int) -> bool:
    budget = _budget(root, name, limit, content)
    return budget is not None and len(content) > budget


def _raw(path: Path) -> bytes | None:
    return path.read_bytes() if path.exists() else None


def _encode(raw: bytes | None) -> str | None:
    return base64.b64encode(raw).decode('ascii') if raw is not None else None


def _decode(value: str | None) -> bytes | None:
    return base64.b64decode(value, validate=True) if value is not None else None


def _digest(plan: dict[str, Any]) -> str:
    return content_digest(canonical_json({k: v for k, v in plan.items() if k != 'digest'}))


def propose(root: Path, moves: list[dict[str, Any]], *, hard_limit: int = 40000) -> dict[str, Any]:
    """Return a read-only proposal and exact recovery bytes, including dirty data.

    Only explicitly classified history/evidence/active-detail ranges can move.
    The owner must keep current gates and short pointers in the source document.
    Proposal data is sensitive like its source: never publish it as public logs.
    """
    root = root.resolve()
    if type(hard_limit) is not int or not 0 < hard_limit <= 40000 or not moves:
        raise ValueError('invalid budget or empty moves')
    _authority(root, [m[k] for m in moves for k in ('source', 'destination')])
    before: dict[str, bytes | None] = {}
    ranges: dict[str, list[tuple[int, int, str]]] = {}
    aliases: dict[str, str] = {}
    for move in moves:
        if move.get('classification') not in {'history', 'evidence', 'active_detail'}:
            raise ValueError('unknown classification requires owner review')
        if not move.get('owner') or not move.get('reason'):
            raise ValueError('owner and retention reason required')
        source, destination = move['source'], move['destination']
        for name in (source, destination):
            if Path(name).suffix.lower() not in {'.md', '.markdown'} or name.split('/')[0].casefold() in {'.git', '.aws', '.ssh'}:
                raise ValueError('compaction is restricted to project Markdown documents')
            if name.startswith(JOURNAL_ROOT + '/'):
                raise ValueError('journal cannot be compacted')
            prior = aliases.setdefault(name.casefold(), name)
            if prior != name:
                raise ValueError('case alias conflict')
            if name not in before:
                before[name] = _raw(_path(root, name))
        raw = before[source]
        start, end = move['start'], move['end']
        if raw is None or type(start) is not int or type(end) is not int or not 0 <= start < end <= len(raw):
            raise ValueError('invalid source byte range')
        # Validate complete UTF-8 boundaries, not character approximations.
        raw[:start].decode('utf-8'); raw[start:end].decode('utf-8'); raw[end:].decode('utf-8')
        ranges.setdefault(source, []).append((start, end, destination))
    destinations = {move['destination'] for move in moves}
    if destinations.intersection(ranges):
        raise ValueError('source/destination overlap')
    after = {name: raw or b'' for name, raw in before.items()}
    mapping = []
    for source in sorted(ranges):
        parts = ranges[source]
        raw = before[source]
        cursor, retained = 0, []
        for start, end, destination in sorted(parts):
            if start < cursor:
                raise ValueError('overlapping source ranges')
            retained.append(raw[cursor:start])
            # A source-local pointer preserves discoverability; destinations are
            # never renamed implicitly. More detailed anchor routing is separate.
            move = next(m for m in moves if m['source'] == source and m['start'] == start and m['end'] == end)
            retained.append(_pointer(root, source, destination, move.get('anchors')))
            destination_start = len(after[destination])
            after[destination] += raw[start:end]
            mapping.append({'source': source, 'start': start, 'end': end,
                            'destination': destination, 'destination_start': destination_start,
                            'digest': content_digest(raw[start:end])})
            cursor = end
        retained.append(raw[cursor:])
        after[source] = b''.join(retained)
        if _exceeds_budget(root, source, after[source], hard_limit):
            raise ValueError('proposal still exceeds active document budget')
    files = []
    for name in sorted(before):
        old, new = before[name], after[name]
        new.decode('utf-8')
        files.append({'path': name, 'before': _encode(old), 'after': _encode(new),
                      'before_digest': content_digest(old) if old is not None else None,
                      'after_digest': content_digest(new), 'before_bytes': len(old or b''), 'after_bytes': len(new),
                      'diff': ''.join(difflib.unified_diff((old or b'').decode('utf-8').splitlines(True),
                                                         new.decode('utf-8').splitlines(True), name, name))})
    plan = {'schema_version': 1, 'workspace_digest': content_digest(os.path.normcase(str(root))),
            'hard_limit_bytes': hard_limit, 'moves': moves, 'preservation_map': mapping, 'files': files}
    plan['digest'] = _digest(plan)
    _validate(root, plan)
    return plan


def _validate(root: Path, plan: dict[str, Any]) -> None:
    """Verify recovery bytes and replay the preservation map before side effects."""
    if plan.get('schema_version') != 1 or plan.get('digest') != _digest(plan):
        raise ValueError('invalid proposal digest/schema')
    if plan.get('workspace_digest') != content_digest(os.path.normcase(str(root.resolve()))):
        raise ValueError('wrong workspace')
    names = set()
    files = {}
    for item in plan['files']:
        name = item['path']
        if Path(name).suffix.lower() not in {'.md', '.markdown'} or name.split('/')[0].casefold() in {'.git', '.aws', '.ssh'}:
            raise ValueError('compaction is restricted to project Markdown documents')
        _path(root, name)
        if name.casefold() in names or name.startswith(JOURNAL_ROOT + '/'):
            raise ValueError('duplicate/reserved path')
        names.add(name.casefold())
        before, after = _decode(item['before']), _decode(item['after'])
        if after is None or item['after_digest'] != content_digest(after):
            raise ValueError('corrupt after bytes')
        if item['before_digest'] != (content_digest(before) if before is not None else None):
            raise ValueError('corrupt recovery bytes')
        expected_diff = ''.join(difflib.unified_diff((before or b'').decode('utf-8').splitlines(True),
                                                     after.decode('utf-8').splitlines(True), name, name))
        if (item.get('before_bytes') != len(before or b'') or item.get('after_bytes') != len(after)
                or item.get('diff') != expected_diff):
            raise ValueError('preservation preview mismatch')
        files[name] = (before, after)
    for mapping in plan['preservation_map']:
        original = files[mapping['source']][0][mapping['start']:mapping['end']]
        offset = mapping['destination_start']
        restored = files[mapping['destination']][1][offset:offset + len(original)]
        if original != restored or content_digest(original) != mapping['digest']:
            raise ValueError('preservation map mismatch')
    # Prove conservation of *all* original bytes, including unmoved gates and
    # prior destination content. A valid hash alone cannot prove a lossless plan.
    expected = {name: old or b'' for name, (old, _) in files.items()}
    sources = {move['source'] for move in plan['moves']}
    destinations = {move['destination'] for move in plan['moves']}
    if sources & destinations or set(files) != sources | destinations:
        raise ValueError('preservation source/destination mismatch')
    for source in sorted(sources):
        original = files[source][0]
        cursor, pieces = 0, []
        source_moves = sorted((m for m in plan['moves'] if m['source'] == source), key=lambda m: m['start'])
        for move in source_moves:
            start, end, destination = move['start'], move['end'], move['destination']
            if (original is None or type(start) is not int or type(end) is not int
                    or not cursor <= start < end <= len(original)
                    or move.get('classification') not in {'history', 'evidence', 'active_detail'}
                    or not move.get('owner') or not move.get('reason')):
                raise ValueError('preservation range invalid')
            pieces.append(original[cursor:start])
            pieces.append(_pointer(root, source, destination, move.get('anchors')))
            expected[destination] += original[start:end]
            cursor = end
        pieces.append(original[cursor:])
        expected[source] = b''.join(pieces)
        if _exceeds_budget(root, source, expected[source], plan['hard_limit_bytes']):
            raise ValueError('preservation budget exceeded')
    for move in plan['moves']:
        if move['classification'] == 'active_detail' and _exceeds_budget(root, move['destination'], expected[move['destination']], plan['hard_limit_bytes']):
            raise ValueError('active destination budget exceeded')
    if any(expected[name] != after for name, (_, after) in files.items()):
        raise ValueError('preservation of original content failed')


def _write(path: Path, raw: bytes) -> None:
    """Atomic replacement of one file; a journal coordinates multi-file recovery."""
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.paos-pending')
    # Never overwrite a pre-existing pending file from another operation.
    with temporary.open('xb') as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    try:
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def apply(root: Path, plan: dict[str, Any], *, approved_digest: str,
          after_write: Callable[[int], None] | None = None) -> dict[str, str]:
    """Apply an explicitly approved plan; caller must exclude external writers."""
    root = root.resolve()
    _validate(root, plan)
    _authority(root, [f['path'] for f in plan['files']])
    if approved_digest != plan['digest']:
        raise ValueError('exact proposal approval required')
    from product_agent_os.document_navigation import check_local_links
    overlay = {f['path']: _decode(f['after']) for f in plan['files']}
    if check_local_links(root, list(overlay), contents=overlay):
        raise ValueError('proposal contains unresolved local links')
    journal = JOURNAL_ROOT + '/' + plan['digest'].split(':')[1] + '.json'
    journal_path = _path(root, journal)
    if all(_raw(_path(root, f['path'])) == _decode(f['after']) for f in plan['files']):
        if not journal_path.is_file():
            raise ValueError('matching output without recovery journal')
        if json.loads(journal_path.read_text(encoding='utf-8')) != plan:
            raise ValueError('recovery journal mismatch')
        return {'status': 'already_applied', 'journal': journal}
    for item in plan['files']:
        if _raw(_path(root, item['path'])) != _decode(item['before']):
            raise ValueError('source/destination conflict')
    lock = _path(root, LOCK)
    lock.parent.mkdir(parents=True, exist_ok=True)
    with lock.open('xb') as handle:
        handle.write(plan['digest'].encode())
    try:
        _write(journal_path, canonical_json(plan).encode('utf-8'))
        for index, item in enumerate(plan['files'], 1):
            path = _path(root, item['path'])
            if _raw(path) != _decode(item['before']):
                raise ValueError('concurrent writer conflict')
            _write(path, _decode(item['after']))
            if after_write:
                after_write(index)
        if not all(_raw(_path(root, f['path'])) == _decode(f['after']) for f in plan['files']):
            raise ValueError('post-write verification conflict')
    except Exception:
        # Recovery refuses any bytes other than before/after; it never rolls
        # back a later user edit. The journal remains for explicit intervention.
        _restore(root, plan)
        raise
    finally:
        lock.unlink()
    return {'status': 'applied', 'journal': journal}


def _restore(root: Path, plan: dict[str, Any]) -> None:
    for item in plan['files']:
        if _raw(_path(root, item['path'])) not in (_decode(item['before']), _decode(item['after'])):
            raise ValueError('rollback conflict; preserve later user changes')
    for item in reversed(plan['files']):
        path = _path(root, item['path'])
        before = _decode(item['before'])
        if _raw(path) not in (before, _decode(item['after'])):
            raise ValueError('rollback concurrent writer conflict')
        if _raw(path) == before:
            continue
        if before is None:
            path.unlink()  # Only a verified file created by this exact transaction.
        else:
            _write(path, before)


def rollback(root: Path, journal: str, *, abandoned_lock_digest: str | None = None) -> dict[str, str]:
    """Explicit recovery; never removes evidence journals or foreign edits.

    After a process crash an operator may confirm no writer is alive and supply
    the exact abandoned lock digest. It is never cleared by age or automatically.
    """
    root = root.resolve()
    if not journal.startswith(JOURNAL_ROOT + '/') or not journal.endswith('.json'):
        raise ValueError('invalid recovery journal')
    plan = json.loads(_path(root, journal).read_text(encoding='utf-8'))
    _validate(root, plan)
    _authority(root, [f['path'] for f in plan['files']])
    lock = _path(root, LOCK)
    if abandoned_lock_digest is not None:
        if abandoned_lock_digest != plan['digest'] or lock.read_text(encoding='utf-8') != abandoned_lock_digest:
            raise ValueError('abandoned lock identity mismatch')
        lock.unlink()
    with lock.open('xb') as handle:
        handle.write(plan['digest'].encode())
    try:
        _restore(root, plan)
    finally:
        lock.unlink()
    return {'status': 'restored', 'journal': journal}
