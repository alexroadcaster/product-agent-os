# app/api/contacts_routes.py
"""Contact REST endpoints (Plan 2 list + Plan 4a T2.1-T2.3, T2.5-T2.6, T3.2-T3.4, T4.2).

Routes
------
GET  /api/contacts                               — paginated list with search + tag/weight/merged filters
GET  /api/contacts/{contact_id}                  — single-contact deep view
GET  /api/contacts/{contact_id}/relationship-summary - scoped metadata-only person relationship summary
PATCH /api/contacts/{contact_id}                 — edit first_name / last_name / note_text
GET  /api/contacts/{contact_id}/messages         — paginated message slice
GET  /api/contacts/{contact_id}/chats            — chats where contact participates
GET  /api/contacts/{contact_id}/merge-candidates — cross-platform merge suggestions (T3.2)
POST /api/contacts/{contact_id}/merge            — merge source into canonical (T3.3)
POST /api/contacts/{contact_id}/unmerge          — restore merged contact to canonical (T3.4)
POST /api/contacts/{contact_id}/tags             — attach a tag to a contact (T4.2)
DELETE /api/contacts/{contact_id}/tags/{tag_id}  — detach a tag from a contact (T4.2)

Note: GET /api/contacts/{contact_id}/insights lives in insights_routes.py
(domain consistency — all insight CRUD in one module).
"""
from __future__ import annotations

import logging
import re
import time
from typing import Annotated, Literal
from urllib.parse import quote_plus, urlparse

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Path, Query, Request
from pydantic import BaseModel, Field
from sqlalchemy import String, and_, cast, func, or_, select
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import TimeoutError as SqlAlchemyTimeoutError
from sqlalchemy.ext.asyncio import AsyncSession

from app.advisor.finding_lifecycle import invalidate_findings_for_contact_unmerge
from app.api.openapi_schemas import (
    ERROR_400,
    ERROR_404,
    ERROR_409,
    ERROR_503,
    ContactAdvisorMetadata,
    ContactChannelItem,
    ContactChatOpenResponse,
    ContactChatsResponse,
    ContactDetailResponse,
    ContactDossierResponse,
    ContactFacetsResponse,
    ContactGraphMetadata,
    ContactLocationFacets,
    ContactLocationItem,
    ContactLocationOpenTarget,
    ContactMessagesResponse,
    ContactMutationResponse,
    ContactOpenTarget,
    ContactRelationshipStatePreviewRequest,
    ContactRelationshipStatePreviewResponse,
    ContactRelationshipStatePreviewResult,
    ContactRelationshipStateResponse,
    ContactsResponse,
    ContactTagMutationResponse,
    MergeCandidatesResponse,
    MergeResponse,
    PersonSummaryEvidenceSourceContextResponse,
    PersonSummaryResponse,
    UnmergeResponse,
)
from app.contacts.merge_candidates import MergeCandidate, find_merge_candidates
from app.db.message_visibility import visible_message_conditions
from app.db.models import (
    Chat,
    ChatMember,
    Contact,
    ContactManualChannel,
    ContactManualLocation,
    ContactNote,
    ContactRelationshipState,
    ContactSource,
    ContactTag,
    MemoryFact,
    MemoryFactEvidence,
    Message,
    Relationship,
    SourceExclusion,
    Tag,
)
from app.db.session import get_session
from app.graph.projection_lifecycle import invalidate_projection_for_source_change
from app.people.person_summary import build_person_summary
from app.people.relationship_state import (
    RELATIONSHIP_REASON_CODES,
    RelationshipStatePayload,
    RelationshipTier,
    ensure_relationship_state,
    get_relationship_state_payload,
    relationship_state_payload,
)
from app.privacy.metadata import REASON_CODE_PATTERN, validate_reason_code
from app.rag.source_exclusions import is_source_excluded
from app.tags.service import attach_contact_tag_manual, detach_contact_tag_manual

logger = logging.getLogger(__name__)

router = APIRouter(tags=["contacts"])
_SAFE_HANDLE_RE = re.compile(r"^[A-Za-z0-9_.@+\-]{1,128}$")
_SAFE_TELEGRAM_USERNAME_RE = re.compile(r"^@?[A-Za-z0-9_]{5,32}$")
_SAFE_NETWORK_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")
RelationshipTierQuery = Annotated[
    RelationshipTier | None,
    Query(description="People/CRM classification filter"),
]
PERSON_SUMMARY_SOURCE_CONTEXT_CONTRACT_VERSION = (
    "person-summary-evidence-source-context-v1"
)
_SOURCE_CONTEXT_REDACTED_STATES = {"redacted", "unavailable"}
_PERSON_SOURCE_CONTEXT_WINDOW_BEFORE = 2
_PERSON_SOURCE_CONTEXT_WINDOW_AFTER = 2


# ---------------------------------------------------------------------------
# Background recompute helper (T3.3 / T3.4)
# ---------------------------------------------------------------------------


async def _run_recompute_in_new_session() -> None:
    """Open a fresh AsyncSession and recompute the relationship graph.

    Called via FastAPI BackgroundTasks after merge/unmerge so the HTTP
    response returns immediately while the graph rebuilds asynchronously.
    Any exception is swallowed and logged — a failed recompute must never
    crash or delay the API response.
    """
    from app.db.session import _maker
    from app.graph.recomputer import recompute_relationships

    if _maker is None:
        logger.warning("_run_recompute_in_new_session: session factory not ready, skipping")
        return
    try:
        async with _maker() as session:
            await recompute_relationships(session)
    except Exception as exc:
        logger.warning("Background recompute failed: %s", exc)


# ---------------------------------------------------------------------------
# Pydantic schemas
# ---------------------------------------------------------------------------


class ContactPatch(BaseModel):
    """Mutable fields for PATCH /api/contacts/{id}.

    Immutable fields (beeper_contact_id, account_id, network, merged_into_id)
    are intentionally absent — callers that send them get Pydantic 422.
    """

    first_name: str | None = None
    last_name: str | None = None
    note_text: str | None = None


class ContactManualChannelCreate(BaseModel):
    """Explicit user-entered channel link for a selected contact."""

    label: str | None = Field(default=None, max_length=120)
    network: str = Field(min_length=1, max_length=64)
    profile_url: str = Field(min_length=1, max_length=512)


class ContactManualLocationPatch(BaseModel):
    """Explicit user-entered primary location metadata for a selected contact."""

    city: str | None = Field(default=None, max_length=80)
    country: str | None = Field(default=None, max_length=80)
    location_label: str = Field(min_length=1, max_length=80)
    region: str | None = Field(default=None, max_length=80)
    timezone: str | None = Field(default=None, max_length=80)


class ContactRelationshipStatePatch(BaseModel):
    """Explicit local People classification update.

    This route is a user-action boundary. Advisor/free-form/Worker output must
    not call it without an explicit user request handled by the frontend.
    """

    relationship_tier: Literal["confirmed", "potential", "ambient", "ignored", "self"]
    reason_code: str = Field(
        default="user_updated",
        pattern=REASON_CODE_PATTERN,
        json_schema_extra={"enum": sorted(RELATIONSHIP_REASON_CODES)},
    )
    confidence_score: float | None = None
    confidence_band: Literal["low", "medium", "high"] | None = None
    user_locked: bool = True


# ---------------------------------------------------------------------------
# GET /api/contacts  — list + search (extended in T2.6)
# ---------------------------------------------------------------------------


@router.get("/api/contacts", response_model=ContactsResponse)
async def list_contacts(
    q: str | None = Query(None, description="Substring search across first_name/last_name/username"),
    network: str | None = Query(None, description="Exact network filter (telegram, whatsapp, ...)"),
    relationship_tier: RelationshipTierQuery = None,
    tag_id: int | None = Query(None, description="Filter to contacts having this tag"),
    min_weight: float | None = Query(None, ge=0.0, description="Min Relationship.weight threshold"),
    include_merged: bool = Query(False, description="Include merged-duplicate rows (default false → canonical only)"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),  # noqa: B008
):
    """Return contacts with optional search, network, tag, weight and merged filters.

    By default only canonical rows (``merged_into_id IS NULL``) are returned.
    Pass ``include_merged=true`` to see all rows.

    Args:
        q: Optional substring; matches case-insensitively against first_name / last_name / username.
        network: Optional exact-match filter.
        tag_id: Optional tag id; restricts to contacts that have that tag.
        min_weight: Optional lower-bound on ``Relationship.weight`` — contact must appear
            in at least one relationship with weight >= this value.
        include_merged: If ``False`` (default) only canonical rows are returned.
        limit: Page size 1-200, default 50.
        offset: Pagination offset, default 0.
        session: Async DB session injected via FastAPI ``Depends``.

    Returns:
        ``{"items": [...], "total": int, "limit": int, "offset": int}``
    """
    base = select(Contact)

    if q:
        pattern = f"%{q}%"
        base = base.where(
            Contact.first_name.ilike(pattern)
            | Contact.last_name.ilike(pattern)
            | Contact.username.ilike(pattern)
        )

    if network:
        base = base.where(Contact.network == network)

    if relationship_tier is not None:
        base = base.join(
            ContactRelationshipState,
            ContactRelationshipState.contact_id == Contact.id,
        ).where(ContactRelationshipState.relationship_tier == relationship_tier)

    if not include_merged:
        base = base.where(Contact.merged_into_id.is_(None))

    if tag_id is not None:
        base = base.join(ContactTag, ContactTag.contact_id == Contact.id).where(
            ContactTag.tag_id == tag_id,
            ContactTag.archived_at.is_(None),
            ContactTag.removed_at.is_(None),
        )

    if min_weight is not None:
        # contacts appearing in any Relationship row with weight >= threshold
        sub_a = select(Relationship.contact_a_id).where(
            Relationship.weight >= min_weight
        )
        sub_b = select(Relationship.contact_b_id).where(
            Relationship.weight >= min_weight
        )
        base = base.where(
            Contact.id.in_(sub_a.union(sub_b))
        )

    count_q = select(func.count()).select_from(base.subquery())
    total = (await session.execute(count_q)).scalar_one()

    results = (
        await session.execute(base.order_by(Contact.first_name).limit(limit).offset(offset))
    ).scalars().all()
    states_by_contact_id = await _load_relationship_state_map(
        session,
        [c.id for c in results],
    )

    return {
        "items": [
            {
                "id": c.id,
                "beeper_contact_id": c.beeper_contact_id,
                "account_id": c.account_id,
                "network": c.network,
                "username": c.username,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "is_deleted": c.is_deleted,
                "merged_into_id": c.merged_into_id,
                **_contact_projection_fields(c, states_by_contact_id.get(c.id)),
            }
            for c in results
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


# ---------------------------------------------------------------------------
# GET /api/contacts/{contact_id}  — single-contact deep view (T2.1)
# ---------------------------------------------------------------------------


@router.get("/api/contacts/facets", response_model=ContactFacetsResponse)
async def get_contact_facets(
    q: str | None = Query(
        None,
        description="Substring search across first_name/last_name/username",
    ),
    network: str | None = Query(None, description="Exact network filter"),
    relationship_tier: RelationshipTierQuery = None,
    relationship_state_source: Literal["sync", "user", "system", "migration"] | None = Query(
        None,
        description="People/CRM classification source filter",
    ),
    user_locked: bool | None = Query(None, description="Relationship state lock filter"),
    tag_id: int | None = Query(None, description="Filter to contacts having this tag"),
    min_weight: float | None = Query(
        None,
        ge=0.0,
        description="Min Relationship.weight threshold",
    ),
    include_merged: bool = Query(False, description="Include merged duplicate rows"),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactFacetsResponse:
    """Return sanitized People facets without raw messages, chat titles, or payloads."""

    base = select(Contact, ContactRelationshipState).outerjoin(
        ContactRelationshipState,
        ContactRelationshipState.contact_id == Contact.id,
    )
    if q:
        pattern = f"%{q}%"
        base = base.where(
            Contact.first_name.ilike(pattern)
            | Contact.last_name.ilike(pattern)
            | Contact.username.ilike(pattern)
        )
    if network:
        base = base.where(Contact.network == network)
    if not include_merged:
        base = base.where(Contact.merged_into_id.is_(None))
    if tag_id is not None:
        base = base.join(ContactTag, ContactTag.contact_id == Contact.id).where(
            ContactTag.tag_id == tag_id,
            ContactTag.archived_at.is_(None),
            ContactTag.removed_at.is_(None),
        )
    if min_weight is not None:
        sub_a = select(Relationship.contact_a_id).where(
            Relationship.weight >= min_weight
        )
        sub_b = select(Relationship.contact_b_id).where(
            Relationship.weight >= min_weight
        )
        base = base.where(Contact.id.in_(sub_a.union(sub_b)))

    rows = (await session.execute(base)).all()
    filtered: list[tuple[Contact, ContactRelationshipState | None]] = []
    for contact, state in rows:
        fields = _relationship_state_fields(contact, state)
        if relationship_tier is not None and fields["relationship_tier"] != relationship_tier:
            continue
        if (
            relationship_state_source is not None
            and fields["relationship_state_source"] != relationship_state_source
        ):
            continue
        if (
            user_locked is not None
            and bool(fields["relationship_state_user_locked"]) != user_locked
        ):
            continue
        filtered.append((contact, state))

    contact_ids = [contact.id for contact, _state in filtered]
    source_type_counts: dict[str, int] = {}
    if contact_ids:
        source_rows = (
            await session.execute(
                select(ContactSource.source_type, func.count())
                .where(
                    ContactSource.contact_id.in_(contact_ids),
                    ContactSource.is_active.is_(True),
                )
                .group_by(ContactSource.source_type)
            )
        ).all()
        source_type_counts = {source_type: count for source_type, count in source_rows}

    tier_counts: dict[str, int] = {}
    source_counts: dict[str, int] = {}
    network_counts: dict[str, int] = {}
    channel_counts: dict[str, int] = {}
    for contact, state in filtered:
        fields = _relationship_state_fields(contact, state)
        tier = str(fields["relationship_tier"])
        source = str(fields["relationship_state_source"])
        tier_counts[tier] = tier_counts.get(tier, 0) + 1
        source_counts[source] = source_counts.get(source, 0) + 1
        network_counts[contact.network] = network_counts.get(contact.network, 0) + 1
        channel_counts[contact.network] = channel_counts.get(contact.network, 0) + 1

    return ContactFacetsResponse(
        total=len(filtered),
        tiers=_count_items(tier_counts),
        relationship_state_sources=_count_items(source_counts),
        networks=_count_items(network_counts),
        source_types=_count_items(source_type_counts),
        channels=_count_items(channel_counts),
        locations=ContactLocationFacets(
            known=0,
            unknown=len(filtered),
            manual=0,
            user_verified=0,
        ),
    )


@router.post(
    "/api/contacts/relationship-state/preview",
    response_model=ContactRelationshipStatePreviewResponse,
)
async def preview_contact_relationship_state(
    body: ContactRelationshipStatePreviewRequest,
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactRelationshipStatePreviewResponse:
    """Preview People tier changes without mutating tiers, audit, or graph state."""

    results: list[ContactRelationshipStatePreviewResult] = []
    for item in body.items:
        try:
            reason_code = validate_reason_code(
                item.reason_code,
                allowed=RELATIONSHIP_REASON_CODES,
                error_code="invalid_reason_code",
            )
        except ValueError as exc:
            raise HTTPException(422, str(exc)) from exc

        contact = await session.get(Contact, item.contact_id)
        if contact is None:
            results.append(
                ContactRelationshipStatePreviewResult(
                    contact_id=item.contact_id,
                    status="not_found",
                    proposed_tier=item.relationship_tier,
                    reason_code=reason_code,
                    blocked_reason="contact_not_found",
                )
            )
            continue

        current = await get_relationship_state_payload(session, contact)
        blocked_reason: str | None = None
        if contact.is_self and item.relationship_tier != "self":
            blocked_reason = "self_contact_tier_locked"
        elif not contact.is_self and item.relationship_tier == "self":
            blocked_reason = "cannot_mark_non_self_contact_as_self"

        results.append(
            ContactRelationshipStatePreviewResult(
                contact_id=contact.id,
                status="blocked" if blocked_reason else "allowed",
                current_tier=current.relationship_tier,
                proposed_tier=item.relationship_tier,
                would_update=(
                    blocked_reason is None
                    and (
                        current.relationship_tier != item.relationship_tier
                        or current.reason_code != reason_code
                        or current.confidence_score != item.confidence_score
                        or current.confidence_band != item.confidence_band
                        or current.user_locked != item.user_locked
                    )
                ),
                reason_code=reason_code,
                blocked_reason=blocked_reason,
            )
        )

    return ContactRelationshipStatePreviewResponse(items=results)


@router.get(
    "/api/contacts/{contact_id}/relationship-summary",
    response_model=PersonSummaryResponse,
    responses={404: ERROR_404},
)
async def get_contact_person_summary(
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return scoped metadata-only person relationship summary.

    The projection is intentionally narrower than ``/api/graph`` and contact
    detail: it aggregates relationship tier, source state, graph counters,
    sanitized tags, and accepted memory summaries without returning raw
    messages, source text, chat titles, Worker payloads, or graph nodes/edges.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    if contact.merged_into_id is not None:
        canonical = await session.get(Contact, contact.merged_into_id)
        if canonical is not None:
            contact = canonical

    return await build_person_summary(
        session,
        contact,
        requested_contact_id=contact_id,
    )


@router.get(
    "/api/contacts/{contact_id}/relationship-summary/evidence/{evidence_ref_id}/source-context",
    response_model=PersonSummaryEvidenceSourceContextResponse,
    responses={404: ERROR_404},
    summary="Restore local source context for a clicked People card evidence ref",
)
async def get_contact_person_summary_source_context(
    contact_id: int = Path(..., ge=1),
    evidence_ref_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Restore bounded local source context after an explicit People UI click."""

    contact = await _load_canonical_contact(session, contact_id)
    evidence = await _load_person_summary_evidence_ref(
        session,
        contact_id=contact.id,
        evidence_ref_id=evidence_ref_id,
    )
    if evidence is None:
        raise HTTPException(404, "evidence_ref_not_found")

    item = await _person_summary_source_context_item(session, evidence)
    return {
        "contract_version": PERSON_SUMMARY_SOURCE_CONTEXT_CONTRACT_VERSION,
        "contact_id": contact.id,
        "evidence_ref_id": evidence_ref_id,
        "items": [item],
        "count": 1,
    }


async def _load_canonical_contact(session: AsyncSession, contact_id: int) -> Contact:
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")
    if contact.merged_into_id is None:
        return contact
    canonical = await session.get(Contact, contact.merged_into_id)
    return canonical or contact


async def _load_person_summary_evidence_ref(
    session: AsyncSession,
    *,
    contact_id: int,
    evidence_ref_id: int,
) -> MemoryFactEvidence | None:
    return (
        await session.execute(
            select(MemoryFactEvidence)
            .join(MemoryFact, MemoryFact.id == MemoryFactEvidence.memory_fact_id)
            .where(
                MemoryFactEvidence.id == evidence_ref_id,
                MemoryFact.subject_type == "contact",
                MemoryFact.subject_contact_id == contact_id,
                MemoryFact.status == "accepted",
                MemoryFact.invalidated_at.is_(None),
                MemoryFact.archived_at.is_(None),
            )
        )
    ).scalar_one_or_none()


async def _person_summary_source_context_item(
    session: AsyncSession,
    evidence: MemoryFactEvidence,
) -> dict[str, object]:
    base: dict[str, object] = {
        "evidence_ref_id": evidence.id,
        "source_type": _person_summary_source_type(evidence.source_type),
        "rank": evidence.rank,
        "redaction_state": evidence.redaction_state,
        "restore_status": "unavailable",
        "source_text": None,
        "message_ids": [],
        "message_count": 0,
        "rag_card_id": None,
    }
    if evidence.redaction_state in _SOURCE_CONTEXT_REDACTED_STATES:
        return {**base, "restore_status": evidence.redaction_state}
    if evidence.source_type != "message":
        return base

    message_id = _parse_message_source_id(evidence.source_id)
    if message_id is None:
        return {**base, "restore_status": "not_found"}

    anchor = await session.get(Message, message_id)
    if anchor is None:
        return {**base, "restore_status": "not_found"}
    if await is_source_excluded(session, "message", anchor.id):
        return {**base, "restore_status": "excluded"}
    if _message_is_unavailable(anchor):
        return {**base, "restore_status": "deleted"}

    rows = await _message_context_window(session, anchor)
    if not rows:
        return {**base, "restore_status": "deleted"}
    return {
        **base,
        "restore_status": "restored",
        "source_text": "\n".join(_format_source_context_line(row) for row in rows),
        "message_ids": [row.id for row in rows],
        "message_count": len(rows),
    }


async def _message_context_window(
    session: AsyncSession,
    anchor: Message,
) -> list[Message]:
    before_rows = (
        (
            await session.execute(
                select(Message)
                .where(
                    Message.chat_id == anchor.chat_id,
                    *_visible_non_excluded_message_conditions(),
                    or_(
                        Message.timestamp < anchor.timestamp,
                        and_(
                            Message.timestamp == anchor.timestamp,
                            Message.id < anchor.id,
                        ),
                    ),
                )
                .order_by(Message.timestamp.desc(), Message.id.desc())
                .limit(_PERSON_SOURCE_CONTEXT_WINDOW_BEFORE)
            )
        )
        .scalars()
        .all()
    )
    after_rows = (
        (
            await session.execute(
                select(Message)
                .where(
                    Message.chat_id == anchor.chat_id,
                    *_visible_non_excluded_message_conditions(),
                    or_(
                        Message.timestamp > anchor.timestamp,
                        and_(
                            Message.timestamp == anchor.timestamp,
                            Message.id > anchor.id,
                        ),
                    ),
                )
                .order_by(Message.timestamp.asc(), Message.id.asc())
                .limit(_PERSON_SOURCE_CONTEXT_WINDOW_AFTER)
            )
        )
        .scalars()
        .all()
    )
    return [*reversed(before_rows), anchor, *after_rows]


def _visible_non_excluded_message_conditions():
    return (
        *visible_message_conditions(),
        ~cast(Message.id, String).in_(
            select(SourceExclusion.source_id).where(
                SourceExclusion.source_type == "message",
                SourceExclusion.status == "active",
            )
        ),
    )


def _message_is_unavailable(message: Message) -> bool:
    return message.deleted_at is not None or message.is_tombstoned or message.text is None


def _person_summary_source_type(source_type: str) -> str:
    if source_type == "message":
        return "message_window"
    if source_type == "card":
        return "rag_card"
    return "user_supplied"


def _parse_message_source_id(value: str) -> int | None:
    cleaned = value.removeprefix("message:").strip()
    try:
        parsed = int(cleaned)
    except ValueError:
        return None
    return parsed if parsed > 0 else None


def _format_source_context_line(message: Message) -> str:
    sender = "You" if message.is_sender else message.sender_name or message.sender_beeper_id
    return f"{sender}: {message.text or ''}"


@router.get(
    "/api/contacts/{contact_id}",
    response_model=ContactDetailResponse,
    responses={404: ERROR_404},
)
async def get_contact(
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return full contact view + tags + note + merged sources.

    Transparently dispatches to canonical if ``contact_id`` is a merged-source row
    (one-hop walk via ``merged_into_id``).

    Args:
        contact_id: Primary key of the Contact row; must be >= 1.
        session: Injected async DB session.

    Returns:
        Full contact dict including ``networks``, ``tags``, ``note``,
        ``merged_sources``.

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    contact = await _load_contact_detail_contact(session, contact_id)
    return await _contact_detail_payload(session, contact)


async def _load_contact_detail_contact(
    session: AsyncSession,
    contact_id: int,
) -> Contact:
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    if contact.merged_into_id is None:
        return contact

    canonical = await session.get(Contact, contact.merged_into_id)
    return canonical or contact


async def _contact_detail_payload(session: AsyncSession, contact: Contact) -> dict:
    # All rows that belong to this canonical entity
    sources_q = select(Contact).where(
        (Contact.id == contact.id) | (Contact.merged_into_id == contact.id)
    )
    sources = (await session.execute(sources_q)).scalars().all()
    networks = sorted({s.network for s in sources})
    merged_sources = [
        {"id": s.id, "network": s.network, "beeper_contact_id": s.beeper_contact_id}
        for s in sources
        if s.id != contact.id
    ]

    # Tags
    tag_rows = (
        await session.execute(
            select(Tag)
            .join(ContactTag, ContactTag.tag_id == Tag.id)
            .where(
                ContactTag.contact_id == contact.id,
                ContactTag.archived_at.is_(None),
                ContactTag.removed_at.is_(None),
            )
        )
    ).scalars().all()

    # Note (PK = contact_id)
    note = await session.get(ContactNote, contact.id)
    relationship_state = await get_relationship_state_payload(session, contact)
    manual_channels, manual_locations = await _load_manual_contact_metadata(
        session,
        contact.id,
    )
    channels = _contact_channels(contact, manual_channels)
    locations = [_manual_location_item(location) for location in manual_locations]
    primary_location = locations[0] if locations else None

    return {
        "id": contact.id,
        "beeper_contact_id": contact.beeper_contact_id,
        "account_id": contact.account_id,
        "network": contact.network,
        "username": contact.username,
        "first_name": contact.first_name,
        "last_name": contact.last_name,
        "phone_number": contact.phone_number,
        "avatar_url": contact.avatar_url,
        "is_deleted": contact.is_deleted,
        **_relationship_state_response_fields(relationship_state),
        "channels": channels,
        "primary_location": primary_location,
        "graph_metadata": _graph_metadata(
            relationship_tier=relationship_state.relationship_tier,
            primary_location=primary_location,
        ),
        "advisor_metadata": _advisor_metadata(
            channels=channels,
            primary_location=primary_location,
        ),
        "is_self": contact.is_self,
        "is_merged": contact.merged_into_id is not None,
        "merged_into_id": contact.merged_into_id,
        "networks": networks,
        "tags": [{"id": t.id, "name": t.name, "color": t.color} for t in tag_rows],
        "note": (
            {"note_text": note.note_text, "updated_at": note.updated_at}
            if note is not None
            else None
        ),
        "merged_sources": merged_sources,
        "locations": locations,
    }


# ---------------------------------------------------------------------------
# PATCH /api/contacts/{contact_id}  — names + note edit (T2.2)
# ---------------------------------------------------------------------------


@router.patch(
    "/api/contacts/{contact_id}",
    response_model=ContactMutationResponse,
    responses={404: ERROR_404},
)
async def patch_contact(
    body: Annotated[
        ContactPatch,
        Body(
            openapi_examples={
                "note": {
                    "summary": "Update the local note for a contact",
                    "value": {"note_text": "Prefers concise investor updates."},
                },
                "name": {
                    "summary": "Update display name fields",
                    "value": {"first_name": "Alice", "last_name": "Ivanova"},
                },
            }
        ),
    ],
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Update mutable contact fields: first_name, last_name, note_text.

    Immutable fields (beeper_contact_id, account_id, network, merged_into_id)
    are not accepted by the schema.

    Args:
        body: Partial update payload.
        contact_id: Primary key, must be >= 1.
        session: Injected async DB session.

    Returns:
        ``{"status": "ok", "id": contact_id}``

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    if body.first_name is not None:
        contact.first_name = body.first_name
    if body.last_name is not None:
        contact.last_name = body.last_name

    if body.note_text is not None:
        note = await session.get(ContactNote, contact.id)
        now = int(time.time())
        if note is None:
            session.add(
                ContactNote(
                    contact_id=contact.id,
                    note_text=body.note_text,
                    updated_at=now,
                )
            )
        else:
            note.note_text = body.note_text
            note.updated_at = now

    await session.commit()
    return {"status": "ok", "id": contact.id}


@router.post(
    "/api/contacts/{contact_id}/channels",
    response_model=ContactChannelItem,
    responses={404: ERROR_404},
)
async def post_contact_channel(
    body: ContactManualChannelCreate,
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactChannelItem:
    """Create a manual contact channel for an explicit user-open action."""

    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")
    if contact.merged_into_id is not None:
        canonical = await session.get(Contact, contact.merged_into_id)
        if canonical is not None:
            contact = canonical

    network = _normalize_manual_network(body.network)
    profile_url = _normalize_manual_profile_url(body.profile_url)
    label = (body.label or f"{_network_channel_label(network)} profile").strip()
    if not label:
        label = f"{_network_channel_label(network)} profile"

    now = int(time.time())
    row = ContactManualChannel(
        contact_id=contact.id,
        network=network,
        label=label,
        profile_url=profile_url,
        is_primary=False,
        created_at=now,
        updated_at=now,
    )
    session.add(row)
    await session.commit()
    await session.refresh(row)
    return _manual_channel_item(row)


@router.get(
    "/api/contacts/{contact_id}/dossier",
    response_model=ContactDossierResponse,
    responses={404: ERROR_404, 503: ERROR_503},
)
async def get_contact_dossier(
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return the initial contact dossier payload for canonical People routes.

    This route keeps the first CRM dossier render on one local FastAPI request:
    contact metadata, scoped graph summary, and chat metadata are assembled in
    one session without raw message bodies or full graph hydration.
    """

    try:
        contact = await _load_contact_detail_contact(session, contact_id)
        return {
            "contact": await _contact_detail_payload(session, contact),
            "chats": await _contact_chats_payload(session, contact),
            "relationship_summary": await build_person_summary(
                session,
                contact,
                requested_contact_id=contact_id,
            ),
        }
    except SqlAlchemyTimeoutError as exc:
        raise HTTPException(503, "contact_dossier_unavailable") from exc


@router.patch(
    "/api/contacts/{contact_id}/location",
    response_model=ContactLocationItem,
    responses={404: ERROR_404},
)
async def patch_contact_location(
    body: ContactManualLocationPatch,
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactLocationItem:
    """Upsert an explicit manual primary location for a selected contact."""

    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")
    if contact.merged_into_id is not None:
        canonical = await session.get(Contact, contact.merged_into_id)
        if canonical is not None:
            contact = canonical

    location_label = body.location_label.strip()
    if not location_label:
        raise HTTPException(422, "invalid_location_label")

    now = int(time.time())
    existing = (
        await session.execute(
            select(ContactManualLocation)
            .where(
                ContactManualLocation.contact_id == contact.id,
                ContactManualLocation.archived_at.is_(None),
                ContactManualLocation.is_primary.is_(True),
            )
            .order_by(ContactManualLocation.updated_at.desc())
            .limit(1)
        )
    ).scalar_one_or_none()
    if existing is None:
        existing = ContactManualLocation(
            contact_id=contact.id,
            location_label=location_label,
            city=_clean_optional_text(body.city),
            region=_clean_optional_text(body.region),
            country=_clean_optional_text(body.country),
            timezone=_clean_optional_text(body.timezone),
            is_primary=True,
            created_at=now,
            updated_at=now,
        )
        session.add(existing)
    else:
        existing.location_label = location_label
        existing.city = _clean_optional_text(body.city)
        existing.region = _clean_optional_text(body.region)
        existing.country = _clean_optional_text(body.country)
        existing.timezone = _clean_optional_text(body.timezone)
        existing.updated_at = now

    await session.commit()
    await session.refresh(existing)
    return _manual_location_item(existing)


@router.patch(
    "/api/contacts/{contact_id}/relationship-state",
    response_model=ContactRelationshipStateResponse,
    responses={404: ERROR_404, 409: ERROR_409},
)
async def patch_contact_relationship_state(
    body: Annotated[
        ContactRelationshipStatePatch,
        Body(
            openapi_examples={
                "promote": {
                    "summary": "Promote a review-needed person into confirmed People",
                    "value": {
                        "relationship_tier": "confirmed",
                        "reason_code": "user_promoted",
                        "user_locked": True,
                    },
                },
                "hide": {
                    "summary": "Hide an ambient or potential person from default People",
                    "value": {
                        "relationship_tier": "ignored",
                        "reason_code": "user_hidden",
                        "user_locked": True,
                    },
                },
            }
        ),
    ],
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactRelationshipStateResponse:
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")
    if contact.is_self and body.relationship_tier != "self":
        raise HTTPException(409, "self_contact_tier_locked")
    if not contact.is_self and body.relationship_tier == "self":
        raise HTTPException(409, "cannot_mark_non_self_contact_as_self")

    try:
        row = await ensure_relationship_state(
            session,
            contact,
            relationship_tier=body.relationship_tier,
            classification_source="user",
            reason_code=body.reason_code,
            confidence_score=body.confidence_score,
            confidence_band=body.confidence_band,
            user_locked=body.user_locked,
            invalidate_projection=True,
        )
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    await session.commit()
    return _relationship_state_response(row)


# ---------------------------------------------------------------------------
# GET /api/contacts/{contact_id}/messages  — paginated slice (T2.3)
# ---------------------------------------------------------------------------


@router.get(
    "/api/contacts/{contact_id}/messages",
    response_model=ContactMessagesResponse,
    responses={404: ERROR_404},
)
async def get_contact_messages(
    contact_id: int = Path(..., ge=1),
    limit: int = Query(50, ge=1, le=200),
    from_ts: int | None = Query(None, description="Inclusive lower timestamp bound"),
    to_ts: int | None = Query(None, description="Inclusive upper timestamp bound"),
    chat_id: int | None = Query(None, description="Narrow to a single chat"),
    sender: Literal["all", "me"] = Query(
        "all",
        description="Use sender=me to return only local-user outbound messages",
    ),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return paginated messages for chats where the contact participates.

    ``next_cursor`` equals the smallest ``timestamp`` in the result set and
    can be used as ``to_ts`` on the next call to load older messages.

    Args:
        contact_id: Primary key of the contact; must be >= 1.
        limit: Page size 1-200, default 50.
        from_ts: Inclusive lower timestamp bound.
        to_ts: Inclusive upper timestamp bound.
        chat_id: If supplied, restrict to this chat only.
        sender: If ``me``, return only messages authored by the local user.
        session: Injected async DB session.

    Returns:
        ``{"items": [...], "limit": int, "next_cursor": int | null}``

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    # Chats where contact is a member
    chat_ids_q = select(ChatMember.chat_id).where(ChatMember.contact_id == contact.id)
    chat_ids = (await session.execute(chat_ids_q)).scalars().all()

    msg_q = select(Message).where(
        Message.chat_id.in_(chat_ids),
        *visible_message_conditions(),
    )

    if chat_id is not None:
        msg_q = msg_q.where(Message.chat_id == chat_id)
    if sender == "me":
        msg_q = msg_q.where(Message.is_sender.is_(True))
    if from_ts is not None:
        msg_q = msg_q.where(Message.timestamp >= from_ts)
    if to_ts is not None:
        msg_q = msg_q.where(Message.timestamp <= to_ts)

    msg_q = msg_q.order_by(Message.timestamp.desc(), Message.id.desc()).limit(limit)
    messages = (await session.execute(msg_q)).scalars().all()
    reply_targets = await _visible_reply_targets(session, messages, chat_ids)

    next_cursor: int | None = min((m.timestamp for m in messages), default=None)

    return {
        "items": [
            {
                "id": m.id,
                "chat_id": m.chat_id,
                "sender_beeper_id": m.sender_beeper_id,
                "sender_name": m.sender_name,
                "text": m.text,
                "timestamp": m.timestamp,
                "is_sender": m.is_sender,
                "network": m.network,
                "reply_to_message_id": m.reply_to_message_id,
                "reply_to_missing": _reply_context_missing(m, reply_targets),
                "reply_to_message": _contact_message_reply_payload(
                    reply_targets.get(m.reply_to_message_id)
                    if m.reply_to_message_id is not None
                    else None
                ),
            }
            for m in messages
        ],
        "limit": limit,
        "next_cursor": next_cursor,
    }


async def _visible_reply_targets(
    session: AsyncSession,
    messages: list[Message],
    chat_ids: list[int],
) -> dict[int, Message]:
    reply_ids = sorted(
        {
            message.reply_to_message_id
            for message in messages
            if message.reply_to_message_id is not None
        }
    )
    if not reply_ids:
        return {}
    rows = (
        (
            await session.execute(
                select(Message).where(
                    Message.id.in_(reply_ids),
                    Message.chat_id.in_(chat_ids),
                    *visible_message_conditions(),
                )
            )
        )
        .scalars()
        .all()
    )
    return {row.id: row for row in rows}


def _reply_context_missing(
    message: Message,
    reply_targets: dict[int, Message],
) -> bool:
    if message.reply_to_message_id is not None:
        return message.reply_to_message_id not in reply_targets
    return bool(message.reply_to_beeper_message_id)


def _contact_message_reply_payload(message: Message | None) -> dict[str, object] | None:
    if message is None:
        return None
    return {
        "id": message.id,
        "chat_id": message.chat_id,
        "sender_beeper_id": message.sender_beeper_id,
        "sender_name": message.sender_name,
        "text": message.text,
        "timestamp": message.timestamp,
        "is_sender": message.is_sender,
        "network": message.network,
    }


# ---------------------------------------------------------------------------
# GET /api/contacts/{contact_id}/chats  — chats for contact (T2.5)
# ---------------------------------------------------------------------------


@router.get(
    "/api/contacts/{contact_id}/chats",
    response_model=ContactChatsResponse,
    responses={404: ERROR_404},
)
async def get_contact_chats(
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return chats where the contact is a member, sorted by last_activity_ts DESC.

    Args:
        contact_id: Primary key of the contact; must be >= 1.
        session: Injected async DB session.

    Returns:
        ``{"items": [...]}``

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    return await _contact_chats_payload(session, contact)


@router.post(
    "/api/contacts/{contact_id}/chats/{chat_id}/open",
    response_model=ContactChatOpenResponse,
    responses={404: ERROR_404},
)
async def open_contact_chat(
    request: Request,
    contact_id: int = Path(..., ge=1),
    chat_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> ContactChatOpenResponse:
    """Open a Beeper chat only after verifying contact membership locally."""
    chat = (
        await session.execute(
            select(Chat)
            .join(ChatMember, ChatMember.chat_id == Chat.id)
            .where(Chat.id == chat_id, ChatMember.contact_id == contact_id)
        )
    ).scalar_one_or_none()
    if chat is None:
        raise HTTPException(404, "chat_not_found")

    beeper_client = getattr(request.app.state, "beeper_client", None)
    if beeper_client is None:
        raise HTTPException(503, "beeper_reauth_required")

    try:
        focused = await beeper_client.focus_chat(chat.beeper_chat_id)
    except Exception as exc:
        logger.warning("Beeper chat focus failed for local chat %s", chat.id)
        raise HTTPException(503, "beeper_focus_unavailable") from exc
    if not focused:
        raise HTTPException(503, "beeper_focus_unavailable")

    return ContactChatOpenResponse(
        contact_id=contact_id,
        chat_id=chat_id,
        method="beeper_focus",
        status="opened",
    )


async def _contact_chats_payload(session: AsyncSession, contact: Contact) -> dict:
    contact_chat_ids_q = select(ChatMember.chat_id).where(
        ChatMember.contact_id == contact.id
    )
    local_user_messages_q = (
        select(Message.chat_id, func.count(Message.id).label("local_user_message_count"))
        .where(
            Message.chat_id.in_(contact_chat_ids_q),
            Message.is_sender.is_(True),
            *visible_message_conditions(),
        )
        .group_by(Message.chat_id)
        .subquery()
    )
    chats_q = (
        select(
            Chat,
            func.coalesce(local_user_messages_q.c.local_user_message_count, 0).label(
                "local_user_message_count"
            ),
        )
        .join(ChatMember, ChatMember.chat_id == Chat.id)
        .outerjoin(local_user_messages_q, local_user_messages_q.c.chat_id == Chat.id)
        .where(ChatMember.contact_id == contact.id)
        .order_by(Chat.last_activity_ts.desc())
    )
    chat_rows = (await session.execute(chats_q)).all()

    return {
        "items": [
            {
                "id": c.id,
                "beeper_chat_id": c.beeper_chat_id,
                "title": c.title,
                "type": c.type,
                "network": c.network,
                "participants_count": c.participants_count,
                "last_activity_ts": c.last_activity_ts,
                "local_user_message_count": int(local_user_message_count or 0),
                "has_local_user_messages": bool(local_user_message_count),
                "open_target": _chat_open_target(c),
            }
            for c, local_user_message_count in chat_rows
        ]
    }


# ---------------------------------------------------------------------------
# Pydantic schemas for merge endpoints (T3.3)
# ---------------------------------------------------------------------------


class MergeRequest(BaseModel):
    """Request body for POST /api/contacts/{contact_id}/merge."""

    into_contact_id: int


class TagAttachRequest(BaseModel):
    """Request body for POST /api/contacts/{contact_id}/tags."""

    tag_id: int


# ---------------------------------------------------------------------------
# GET /api/contacts/{contact_id}/merge-candidates  (T3.2)
# ---------------------------------------------------------------------------


@router.get(
    "/api/contacts/{contact_id}/merge-candidates",
    response_model=MergeCandidatesResponse,
    responses={404: ERROR_404},
)
async def get_merge_candidates(
    contact_id: int = Path(..., ge=1),
    top_k: int = Query(5, ge=1, le=20),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Return top-K cross-platform merge candidates for a contact.

    Only contacts from a **different** network are suggested. Candidates are
    ranked by a composite score: SHA-256 avatar-URL hash equality (score 1.0)
    or rapidfuzz Levenshtein distance on full name (distance ≤ 3).

    Args:
        contact_id: PK of the contact; must be >= 1.
        top_k: Maximum candidates to return (1-20, default 5).
        session: Injected async DB session.

    Returns:
        ``{"items": [{contact_id, score, reason, first_name, last_name,
        network, username, avatar_url}, ...]}``

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    target = await session.get(Contact, contact_id)
    if target is None:
        raise HTTPException(404, "contact_not_found")

    candidates: list[MergeCandidate] = await find_merge_candidates(
        session, contact_id=contact_id, top_k=top_k
    )

    items = []
    for mc in candidates:
        c = await session.get(Contact, mc.contact_id)
        if c is None:
            continue
        items.append(
            {
                "contact_id": c.id,
                "score": mc.score,
                "reason": mc.reason,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "network": c.network,
                "username": c.username,
                "avatar_url": c.avatar_url,
            }
        )
    return {"items": items}


# ---------------------------------------------------------------------------
# POST /api/contacts/{contact_id}/merge  (T3.3)
# ---------------------------------------------------------------------------


@router.post(
    "/api/contacts/{contact_id}/merge",
    response_model=MergeResponse,
    responses={400: ERROR_400, 404: ERROR_404, 409: ERROR_409},
)
async def post_merge(
    body: Annotated[
        MergeRequest,
        Body(
            openapi_examples={
                "merge_source": {
                    "summary": "Merge a duplicate source contact into a canonical contact",
                    "value": {"into_contact_id": 1},
                }
            }
        ),
    ],
    background_tasks: BackgroundTasks,
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Merge ``contact_id`` (source) into ``body.into_contact_id`` (canonical).

    Sets ``source.merged_into_id = canonical.id`` and schedules a background
    graph recompute.  The operation is idempotent: if the source is already
    merged into the requested canonical, returns 200 without any DB change.

    Args:
        body: ``{"into_contact_id": int}``
        background_tasks: FastAPI background task queue — recompute runs here.
        contact_id: PK of the *source* contact (the one that becomes merged).
        session: Injected async DB session.

    Returns:
        ``{"status": "merged", "canonical_id": int, "merged_id": int}``

    Raises:
        HTTPException 400: ``cannot_merge_into_self`` or ``target_already_merged``.
        HTTPException 404: ``source_contact_not_found`` or ``target_contact_not_found``.
        HTTPException 409: ``source_already_merged_into_other``.
    """
    if body.into_contact_id == contact_id:
        raise HTTPException(400, "cannot_merge_into_self")

    src = await session.get(Contact, contact_id)
    if src is None:
        raise HTTPException(404, "source_contact_not_found")

    dst = await session.get(Contact, body.into_contact_id)
    if dst is None:
        raise HTTPException(404, "target_contact_not_found")

    if dst.merged_into_id is not None:
        raise HTTPException(400, "target_already_merged")

    # Idempotent: already merged into the same canonical
    if src.merged_into_id == dst.id:
        return {"status": "merged", "canonical_id": dst.id, "merged_id": src.id}

    # Conflict: source is already merged into a *different* canonical
    if src.merged_into_id is not None and src.merged_into_id != dst.id:
        raise HTTPException(409, "source_already_merged_into_other")

    src.merged_into_id = dst.id
    await invalidate_projection_for_source_change(
        session,
        reason="contact_merge",
    )
    await session.commit()
    background_tasks.add_task(_run_recompute_in_new_session)
    return {"status": "merged", "canonical_id": dst.id, "merged_id": src.id}


# ---------------------------------------------------------------------------
# POST /api/contacts/{contact_id}/unmerge  (T3.4)
# ---------------------------------------------------------------------------


@router.post(
    "/api/contacts/{contact_id}/unmerge",
    response_model=UnmergeResponse,
    responses={404: ERROR_404},
)
async def post_unmerge(
    background_tasks: BackgroundTasks,
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Clear ``merged_into_id`` for ``contact_id``, restoring it as canonical.

    Idempotent: if the contact has no ``merged_into_id`` (already canonical),
    returns 200 no-op without any DB change or recompute.

    Post-unmerge behaviour (ADR-0023):
    - ``AiInsight`` rows keyed on ``contact_id`` survive (stable integer PK).
    - ``ContactNote`` / ``ContactTag`` survive per-contact PK — no data loss.
    - Graph is rebuilt via :func:`recompute_relationships` in background.

    Args:
        background_tasks: FastAPI background task queue — recompute runs here.
        contact_id: PK of the contact to unmerge.
        session: Injected async DB session.

    Returns:
        ``{"status": "unmerged", "id": int}``

    Raises:
        HTTPException 404: when ``contact_id`` is unknown.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    if contact.merged_into_id is None:
        return {"status": "unmerged", "id": contact.id}  # idempotent no-op

    previous_canonical_id = contact.merged_into_id
    contact.merged_into_id = None
    await invalidate_findings_for_contact_unmerge(
        session,
        contact_id=contact.id,
        previous_canonical_contact_id=previous_canonical_id,
        now=int(time.time()),
    )
    await invalidate_projection_for_source_change(
        session,
        reason="contact_unmerge",
    )
    await session.commit()
    background_tasks.add_task(_run_recompute_in_new_session)
    return {"status": "unmerged", "id": contact.id}


# ---------------------------------------------------------------------------
# POST /api/contacts/{contact_id}/tags  (T4.2)
# ---------------------------------------------------------------------------


@router.post(
    "/api/contacts/{contact_id}/tags",
    response_model=ContactTagMutationResponse,
    responses={404: ERROR_404},
)
async def attach_tag_to_contact(
    body: Annotated[
        TagAttachRequest,
        Body(
            openapi_examples={
                "attach_tag": {
                    "summary": "Attach an existing tag to a contact",
                    "value": {"tag_id": 8},
                }
            }
        ),
    ],
    contact_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> dict:
    """Attach a tag to a contact. Idempotent — re-POST returns 200 without error.

    Args:
        body: ``{"tag_id": int}``
        contact_id: Primary key of the contact; must be >= 1.
        session: Injected async DB session.

    Returns:
        ``{"status": "attached", "contact_id": int, "tag_id": int}``

    Raises:
        HTTPException 404: ``contact_not_found`` or ``tag_not_found``.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    try:
        await attach_contact_tag_manual(
            session,
            contact_id=contact_id,
            tag_id=body.tag_id,
        )
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(409, str(exc)) from exc
    await session.commit()

    return {"status": "attached", "contact_id": contact_id, "tag_id": body.tag_id}


# ---------------------------------------------------------------------------
# DELETE /api/contacts/{contact_id}/tags/{tag_id}  (T4.2)
# ---------------------------------------------------------------------------


@router.delete(
    "/api/contacts/{contact_id}/tags/{tag_id}",
    status_code=204,
    responses={404: ERROR_404},
)
async def detach_tag_from_contact(
    contact_id: int = Path(..., ge=1),
    tag_id: int = Path(..., ge=1),
    session: AsyncSession = Depends(get_session),  # noqa: B008
) -> None:
    """Detach a tag from a contact.

    Args:
        contact_id: Primary key of the contact; must be >= 1.
        tag_id: Primary key of the tag; must be >= 1.
        session: Injected async DB session.

    Returns:
        HTTP 204 No Content on success.

    Raises:
        HTTPException 404: ``contact_not_found`` if contact does not exist.
        HTTPException 404: ``tag_not_attached`` if the association row is missing.
    """
    contact = await session.get(Contact, contact_id)
    if contact is None:
        raise HTTPException(404, "contact_not_found")

    try:
        await detach_contact_tag_manual(session, contact_id=contact_id, tag_id=tag_id)
    except LookupError as exc:
        raise HTTPException(404, str(exc)) from exc
    await session.commit()


async def _load_relationship_state_map(
    session: AsyncSession,
    contact_ids: list[int],
) -> dict[int, ContactRelationshipState]:
    if not contact_ids:
        return {}
    rows = (
        await session.execute(
            select(ContactRelationshipState).where(
                ContactRelationshipState.contact_id.in_(contact_ids)
            )
        )
    ).scalars().all()
    return {row.contact_id: row for row in rows}


def _relationship_state_fields(
    contact: Contact,
    row: ContactRelationshipState | None,
) -> dict[str, object]:
    if row is None:
        tier = "self" if contact.is_self else "ambient"
        return {
            "relationship_tier": tier,
            "relationship_state_source": "system",
            "relationship_state_reason": "derived_default",
            "relationship_state_user_locked": False,
        }
    return {
        "relationship_tier": row.relationship_tier,
        "relationship_state_source": row.classification_source,
        "relationship_state_reason": row.reason_code,
        "relationship_state_user_locked": bool(row.user_locked),
    }


def _relationship_state_response_fields(
    payload: RelationshipStatePayload,
) -> dict[str, object]:
    return {
        "relationship_tier": payload.relationship_tier,
        "relationship_state_source": payload.classification_source,
        "relationship_state_reason": payload.reason_code,
        "relationship_state_user_locked": payload.user_locked,
    }


def _relationship_state_response(
    row: ContactRelationshipState,
) -> ContactRelationshipStateResponse:
    payload = relationship_state_payload(row)
    return ContactRelationshipStateResponse(
        contact_id=payload.contact_id,
        relationship_tier=payload.relationship_tier,
        classification_source=payload.classification_source,
        reason_code=payload.reason_code,
        confidence_score=payload.confidence_score,
        confidence_band=payload.confidence_band,
        user_locked=payload.user_locked,
        created_at=payload.created_at,
        updated_at=payload.updated_at,
    )


def _contact_projection_fields(
    contact: Contact,
    row: ContactRelationshipState | None,
) -> dict[str, object]:
    fields = _relationship_state_fields(contact, row)
    channels = _contact_channels(contact)
    primary_location = None
    return {
        **fields,
        "channels": channels,
        "primary_location": primary_location,
        "graph_metadata": _graph_metadata(
            relationship_tier=str(fields["relationship_tier"]),
            primary_location=primary_location,
        ),
        "advisor_metadata": _advisor_metadata(
            channels=channels,
            primary_location=primary_location,
        ),
    }


def _contact_channels(
    contact: Contact,
    manual_channels: list[ContactManualChannel] | None = None,
) -> list[ContactChannelItem]:
    """Project explicit-action channels from structured contact fields only."""

    channels: list[ContactChannelItem] = [
        ContactChannelItem(
            channel_type="network",
            network=contact.network,
            label=_network_channel_label(contact.network),
            is_primary=contact.username is None and contact.phone_number is None,
            open_target=ContactOpenTarget(
                method="unsupported",
                status="unsupported",
                value=None,
            ),
        )
    ]

    if contact.username:
        channels.append(
            ContactChannelItem(
                channel_type="profile",
                network=contact.network,
                label=f"{_network_channel_label(contact.network)} profile",
                is_primary=True,
                open_target=_profile_open_target(contact.network, contact.username),
            )
        )

    if contact.phone_number:
        channels.append(
            ContactChannelItem(
                channel_type="phone",
                network="phone",
                label="Phone",
                is_primary=False,
                open_target=_copy_open_target(contact.phone_number),
            )
        )

    for manual_channel in manual_channels or []:
        channels.append(_manual_channel_item(manual_channel))

    return channels


async def _load_manual_contact_metadata(
    session: AsyncSession,
    contact_id: int,
) -> tuple[list[ContactManualChannel], list[ContactManualLocation]]:
    try:
        manual_channels = (
            await session.execute(
                select(ContactManualChannel)
                .where(
                    ContactManualChannel.contact_id == contact_id,
                    ContactManualChannel.archived_at.is_(None),
                )
                .order_by(
                    ContactManualChannel.is_primary.desc(),
                    ContactManualChannel.updated_at.desc(),
                )
            )
        ).scalars().all()
        manual_locations = (
            await session.execute(
                select(ContactManualLocation)
                .where(
                    ContactManualLocation.contact_id == contact_id,
                    ContactManualLocation.archived_at.is_(None),
                )
                .order_by(
                    ContactManualLocation.is_primary.desc(),
                    ContactManualLocation.updated_at.desc(),
                )
            )
        ).scalars().all()
    except OperationalError as exc:
        if not _is_missing_manual_metadata_table_error(exc):
            raise
        logger.warning(
            "contact_manual_metadata_tables_missing",
            extra={"contact_id": contact_id},
        )
        return [], []
    return list(manual_channels), list(manual_locations)


def _is_missing_manual_metadata_table_error(exc: OperationalError) -> bool:
    message = str(getattr(exc, "orig", exc)).lower()
    return "no such table" in message and (
        "contact_manual_channels" in message
        or "contact_manual_locations" in message
    )


def _chat_open_target(chat: Chat) -> ContactOpenTarget:
    normalized = chat.beeper_chat_id.strip()
    if not normalized or len(normalized) > 512:
        return ContactOpenTarget(method="unsupported", status="unsupported", value=None)
    return ContactOpenTarget(method="beeper_chat", status="available", value=normalized)


def _profile_open_target(network: str, handle: str) -> ContactOpenTarget:
    normalized = handle.strip()
    if not _SAFE_HANDLE_RE.fullmatch(normalized):
        return ContactOpenTarget(method="unsupported", status="unsupported", value=None)

    if network == "telegram" and _SAFE_TELEGRAM_USERNAME_RE.fullmatch(normalized):
        username = normalized.removeprefix("@")
        return ContactOpenTarget(
            method="url",
            status="available",
            value=f"https://t.me/{username}",
        )

    return ContactOpenTarget(method="copy", status="available", value=normalized)


def _copy_open_target(value: str) -> ContactOpenTarget:
    normalized = value.strip()
    if not normalized or not _SAFE_HANDLE_RE.fullmatch(normalized):
        return ContactOpenTarget(method="unsupported", status="unsupported", value=None)
    return ContactOpenTarget(method="copy", status="available", value=normalized)


def _manual_channel_item(row: ContactManualChannel) -> ContactChannelItem:
    return ContactChannelItem(
        channel_type="profile",
        network=row.network,
        label=row.label,
        is_primary=row.is_primary,
        open_target=ContactOpenTarget(method="url", status="available", value=row.profile_url),
    )


def _manual_location_item(row: ContactManualLocation) -> ContactLocationItem:
    label = row.location_label.strip()
    query = ", ".join(
        value
        for value in [label, row.city, row.region, row.country]
        if value is not None and value.strip()
    )
    maps_url = (
        f"https://www.google.com/maps/search/?api=1&query={quote_plus(query)}"
        if query
        else None
    )
    return ContactLocationItem(
        location_id=f"manual:{row.id}",
        location_label=label,
        city=row.city,
        region=row.region,
        country=row.country,
        timezone=row.timezone,
        source="manual",
        confidence_score=None,
        is_primary=row.is_primary,
        is_manual=True,
        user_verified=True,
        archived=False,
        open_target=ContactLocationOpenTarget(
            method="maps_search" if maps_url else "unsupported",
            status="available" if maps_url else "unavailable",
            value=maps_url,
        ),
    )


def _normalize_manual_network(value: str) -> str:
    normalized = value.strip().lower().replace(" ", "_")
    if not _SAFE_NETWORK_RE.fullmatch(normalized):
        raise HTTPException(422, "unsupported_contact_channel_network")
    return normalized


def _normalize_manual_profile_url(value: str) -> str:
    normalized = value.strip()
    parsed = urlparse(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise HTTPException(422, "unsupported_contact_channel_url")
    return normalized


def _clean_optional_text(value: str | None) -> str | None:
    cleaned = value.strip() if value is not None else ""
    return cleaned or None


def _network_channel_label(network: str) -> str:
    if not network:
        return "Network"
    return network.replace("_", " ").title()


def _graph_metadata(
    *,
    relationship_tier: str,
    primary_location: ContactLocationItem | None,
) -> ContactGraphMetadata:
    return ContactGraphMetadata(
        relationship_tier=_safe_relationship_tier(relationship_tier),
        default_visibility=_graph_default_visibility(relationship_tier),
        location_status="available" if primary_location is not None else "unknown",
        graph_filter_writes_allowed=False,
    )


def _advisor_metadata(
    *,
    channels: list[ContactChannelItem],
    primary_location: ContactLocationItem | None,
) -> ContactAdvisorMetadata:
    return ContactAdvisorMetadata(
        metadata_only=True,
        tier_read_allowed=True,
        channel_metadata_allowed=any(
            channel.open_target.status == "available" for channel in channels
        ),
        location_metadata_allowed=primary_location is not None,
        auto_promotion_allowed=False,
        worker_write_authority=False,
    )


def _graph_default_visibility(
    relationship_tier: str,
) -> Literal["default_visible", "available_filter", "hidden_by_default", "hidden"]:
    if relationship_tier in {"confirmed", "self"}:
        return "default_visible"
    if relationship_tier == "potential":
        return "available_filter"
    if relationship_tier == "ignored":
        return "hidden"
    return "hidden_by_default"


def _safe_relationship_tier(
    relationship_tier: str,
) -> Literal["confirmed", "potential", "ambient", "ignored", "self"]:
    if relationship_tier in {"confirmed", "potential", "ambient", "ignored", "self"}:
        return relationship_tier  # type: ignore[return-value]
    return "ambient"


def _count_items(counts: dict[str, int]) -> list[dict[str, object]]:
    return [
        {"value": value, "count": count}
        for value, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    ]
