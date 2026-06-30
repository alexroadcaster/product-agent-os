"""Cross-platform merge candidate scoring (Plan 4a T3.1).

Algorithm — two signals combined:

1. **Avatar hash equality**: SHA-256 of avatar_url (Beeper avatar URLs are
   stable per-account). Equal hash → score 1.0. Cheap O(N) scan.
2. **Display name fuzzy match**: rapidfuzz Levenshtein distance on
   ``first_name + " " + last_name`` (lowercased, trimmed).
   distance ≤ 3 → score linearly maps 1 - distance/4. So distance 0 → 1.0,
   1 → 0.75, 2 → 0.5, 3 → 0.25, 4+ → not a candidate.

Final score: max(avatar_score, name_score). Top-K returned.

Excludes:
- The query contact itself
- Any contact with non-NULL merged_into_id (already a source — don't re-merge)
- Any contact in the same network (cross-platform requirement — only suggest
  candidates with a different network)
"""
from __future__ import annotations

import asyncio
import hashlib
from dataclasses import dataclass

from rapidfuzz.distance import Levenshtein
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Contact


@dataclass
class MergeCandidate:
    """A single cross-platform merge suggestion.

    Attributes:
        contact_id: Primary key of the candidate Contact row.
        score: Confidence score in [0.0, 1.0]. 1.0 = identical avatar hash.
        reason: Human-readable signal that drove the score.
            One of ``"avatar_hash"``, ``"name_fuzzy"``, ``"both"``.
    """

    contact_id: int
    score: float
    reason: str  # "avatar_hash" | "name_fuzzy" | "both"


def _avatar_hash(url: str | None) -> str | None:
    """Return SHA-256 hex digest of ``url``, or ``None`` if url is falsy."""
    if not url:
        return None
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def _full_name(c: Contact) -> str:
    """Build lowercased trimmed full-name string from ORM row."""
    return " ".join(p for p in [c.first_name, c.last_name] if p).strip().lower()


async def find_merge_candidates(
    session: AsyncSession, *, contact_id: int, top_k: int = 5
) -> list[MergeCandidate]:
    """Return top-K cross-platform merge candidates for ``contact_id``.

    Only returns contacts from a **different** network (cross-platform filter).
    Contacts that are already merged (``merged_into_id IS NOT NULL``) are
    excluded from both the query-side and the candidate pool.

    Levenshtein scoring runs in a worker thread via :func:`asyncio.to_thread`
    to avoid blocking the event loop on large contact sets.

    Args:
        session: Open async DB session.
        contact_id: PK of the Contact to find candidates for.
        top_k: Maximum number of candidates to return (1-20, default 5).

    Returns:
        List of :class:`MergeCandidate` sorted by score descending.
        Empty list if ``contact_id`` is unknown or already merged.
    """
    target = await session.get(Contact, contact_id)
    if target is None or target.merged_into_id is not None:
        return []

    others = (
        await session.execute(
            select(Contact).where(
                (Contact.id != target.id)
                & (Contact.merged_into_id.is_(None))
                & (Contact.network != target.network)  # cross-platform only
            )
        )
    ).scalars().all()

    target_hash = _avatar_hash(target.avatar_url)
    target_name = _full_name(target)

    return await asyncio.to_thread(
        _score_candidates, target_hash, target_name, list(others), top_k
    )


def _score_candidates(
    target_hash: str | None,
    target_name: str,
    others: list[Contact],
    top_k: int,
) -> list[MergeCandidate]:
    """Pure-sync scoring loop run in a worker thread.

    Args:
        target_hash: SHA-256 hex of target's avatar_url, or None.
        target_name: Lowercased full name of the target contact.
        others: All cross-platform unmerged candidates.
        top_k: Maximum results to return.

    Returns:
        Sorted (desc by score) list, truncated to ``top_k``.
    """
    scored: list[MergeCandidate] = []
    for c in others:
        candidate_hash = _avatar_hash(c.avatar_url)
        avatar_score = (
            1.0 if (target_hash is not None and candidate_hash == target_hash) else 0.0
        )

        candidate_name = _full_name(c)
        if not target_name or not candidate_name:
            name_score = 0.0
        else:
            distance = Levenshtein.distance(target_name, candidate_name)
            name_score = max(0.0, 1.0 - distance / 4.0) if distance <= 3 else 0.0

        score = max(avatar_score, name_score)
        if score <= 0.0:
            continue

        if avatar_score == 1.0 and name_score > 0.0:
            reason = "both"
        elif avatar_score == 1.0:
            reason = "avatar_hash"
        else:
            reason = "name_fuzzy"

        scored.append(MergeCandidate(c.id, score, reason))

    scored.sort(key=lambda mc: -mc.score)
    return scored[:top_k]
