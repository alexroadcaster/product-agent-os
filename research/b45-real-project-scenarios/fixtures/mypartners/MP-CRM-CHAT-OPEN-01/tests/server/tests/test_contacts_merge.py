# tests/test_contacts_merge.py
"""Tests for cross-platform merge endpoints (Plan 4a T3.2, T3.3, T3.4).

Covers:
- GET  /api/contacts/{id}/merge-candidates
- POST /api/contacts/{id}/merge
- POST /api/contacts/{id}/unmerge
"""
from __future__ import annotations

import json

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.api import contacts_routes
from app.db.models import AdvisorFinding, AdvisorRun, Base, Contact, GraphProjectionState
from app.db.session import init_session_factory
from app.main import create_app


@pytest_asyncio.fixture
async def app_client():
    """In-memory DB + FastAPI TestClient wired for merge tests.

    Uses TestClient WITHOUT context manager so the lifespan does NOT run
    and the in-memory engine installed via init_session_factory is preserved
    (same pattern as test_contacts_get_one.py).
    """
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    init_session_factory(engine)

    # Seed contacts:
    # - tg: Telegram canonical
    # - wa: WhatsApp canonical — same avatar as tg (perfect match)
    # - tg2: Second Telegram contact (same network as tg → should NOT be candidate)
    avatar = "https://cdn.beeper.com/avatars/alice.jpg"
    async with maker() as session:
        tg = Contact(
            beeper_contact_id="@alice:tg",
            account_id="acc_tg",
            network="telegram",
            first_name="Alice",
            last_name="Smith",
            avatar_url=avatar,
        )
        wa = Contact(
            beeper_contact_id="@alice:wa",
            account_id="acc_wa",
            network="whatsapp",
            first_name="Alice",
            last_name="Smith",
            avatar_url=avatar,
        )
        tg2 = Contact(
            beeper_contact_id="@bob:tg",
            account_id="acc_tg",
            network="telegram",
            first_name="Bob",
            last_name="Jones",
        )
        session.add_all([tg, wa, tg2])
        await session.commit()

    # No context manager — lifespan NOT triggered, in-memory DB stays active
    app = create_app()
    client = TestClient(app, raise_server_exceptions=True)
    yield client, maker
    await engine.dispose()


# ---------------------------------------------------------------------------
# GET /api/contacts/{id}/merge-candidates  (T3.2)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_merge_candidates_returns_cross_platform(app_client):
    """WhatsApp Alice is returned as candidate for Telegram Alice (same avatar)."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()

    resp = client.get(f"/api/contacts/{tg.id}/merge-candidates?top_k=5")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) == 1
    item = data["items"][0]
    assert item["score"] == 1.0
    assert item["reason"] == "both"  # avatar hash + name match
    assert item["network"] == "whatsapp"


@pytest.mark.asyncio
async def test_get_merge_candidates_excludes_same_network(app_client):
    """tg2 (telegram) must not appear as candidate for tg (also telegram)."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        tg2 = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@bob:tg")
            )
        ).scalar_one()

    resp = client.get(f"/api/contacts/{tg.id}/merge-candidates")
    assert resp.status_code == 200
    ids = {item["contact_id"] for item in resp.json()["items"]}
    assert tg2.id not in ids


@pytest.mark.asyncio
async def test_get_merge_candidates_404_on_unknown(app_client):
    """Unknown contact_id → 404."""
    client, _ = app_client
    resp = client.get("/api/contacts/99999/merge-candidates")
    assert resp.status_code == 404


def _advisor_contact_finding(
    *,
    run_id: int,
    run_key: str,
    finding_id: str,
    target_contact_id: int,
    created_at: int,
) -> AdvisorFinding:
    return AdvisorFinding(
        advisor_run_id=run_id,
        advisor_run_key=run_key,
        finding_id=finding_id,
        finding_type="contact_candidate",
        status="proposed",
        confidence="medium",
        confidence_score=0.62,
        provenance="deterministic_extractor",
        source_category="advisor_run",
        title="Synthetic contact finding",
        summary="Synthetic metadata-only summary.",
        target_contact_id=target_contact_id,
        allowed_actions_json='["link_contact","dismiss"]',
        extractor_version="findings-lifecycle-test-v1",
        taxonomy_version="advisor-findings-taxonomy-v1",
        created_at=created_at,
        updated_at=created_at,
    )


# ---------------------------------------------------------------------------
# POST /api/contacts/{id}/merge  (T3.3)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_post_merge_happy_path(app_client):
    """Merge tg into wa → 200, merged_into_id set."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()

    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": wa.id},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "merged"
    assert body["canonical_id"] == wa.id
    assert body["merged_id"] == tg.id

    # Verify DB state
    async with maker() as session:
        tg_after = await session.get(Contact, tg.id)
    assert tg_after.merged_into_id == wa.id


@pytest.mark.asyncio
async def test_post_merge_marks_projection_stale_before_deferred_recompute(
    app_client,
    monkeypatch,
):
    """Merge must invalidate projection metadata even when recompute is deferred."""
    client, maker = app_client

    async def noop_recompute():
        return None

    monkeypatch.setattr(contacts_routes, "_run_recompute_in_new_session", noop_recompute)
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        session.add(
            GraphProjectionState(
                projection_id="relationship_map_default",
                projection_version="graph_projection_v1",
                active_cache_key="graph_projection_v1:nodes=2:edges=1:last=1714608000",
                active_node_count=2,
                active_edge_count=1,
                active_built_at=1714608000,
                status="ready",
                progress_completed=3,
                progress_total=3,
                progress_stage="ready",
                cancel_requested=False,
                rebuild_started_at=1714607999,
                rebuild_finished_at=1714608000,
                created_at=1714607999,
                updated_at=1714608000,
            )
        )
        await session.commit()

    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": wa.id},
    )

    assert resp.status_code == 200
    async with maker() as session:
        state = (await session.execute(select(GraphProjectionState))).scalar_one()
    assert state.status == "stale"
    assert state.progress_stage == "contact_merge"
    assert state.active_cache_key == "graph_projection_v1:nodes=2:edges=1:last=1714608000"
    assert state.cancel_requested is False


@pytest.mark.asyncio
async def test_post_merge_idempotent(app_client):
    """Re-merging source into the same canonical → 200 no-op."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        # Ensure already merged state
        tg.merged_into_id = wa.id
        await session.commit()

    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": wa.id},
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "merged"


@pytest.mark.asyncio
async def test_post_merge_400_self_merge(app_client):
    """Merging contact into itself → 400."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()

    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": tg.id},
    )
    assert resp.status_code == 400
    assert resp.json()["detail"] == "cannot_merge_into_self"


@pytest.mark.asyncio
async def test_post_merge_404_unknown_source(app_client):
    """Source contact_id unknown → 404."""
    client, maker = app_client
    async with maker() as session:
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()

    resp = client.post(
        "/api/contacts/99999/merge",
        json={"into_contact_id": wa.id},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "source_contact_not_found"


@pytest.mark.asyncio
async def test_post_merge_404_unknown_target(app_client):
    """Target contact_id unknown → 404."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()

    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": 99999},
    )
    assert resp.status_code == 404
    assert resp.json()["detail"] == "target_contact_not_found"


@pytest.mark.asyncio
async def test_post_merge_409_chain_conflict(app_client):
    """Source already merged into a different canonical → 409."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        tg2 = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@bob:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        # Merge tg into tg2 first
        tg.merged_into_id = tg2.id
        await session.commit()

    # Now try to merge tg into wa → 409 (already merged into tg2)
    resp = client.post(
        f"/api/contacts/{tg.id}/merge",
        json={"into_contact_id": wa.id},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"] == "source_already_merged_into_other"


# ---------------------------------------------------------------------------
# POST /api/contacts/{id}/unmerge  (T3.4)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_post_unmerge_happy_path(app_client):
    """Unmerge a previously-merged contact → merged_into_id cleared."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        tg.merged_into_id = wa.id
        await session.commit()

    resp = client.post(f"/api/contacts/{tg.id}/unmerge")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "unmerged"
    assert body["id"] == tg.id

    async with maker() as session:
        tg_after = await session.get(Contact, tg.id)
    assert tg_after.merged_into_id is None


@pytest.mark.asyncio
async def test_post_unmerge_invalidates_advisor_findings_for_previous_canonical_scope(
    app_client,
):
    """Unmerge invalidates contact-scoped Advisor findings in the same transaction."""
    client, maker = app_client
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        tg.merged_into_id = wa.id
        run = AdvisorRun(
            run_id="advisor-run-unmerge",
            status="succeeded",
            input_mode="explicit_command",
            command_id="memory",
            selected_chat_ids_json="[]",
            selected_contact_ids_json=json.dumps([tg.id]),
            resolved_contact_ids_json=json.dumps([wa.id]),
            inferred_contact_ids_json="[]",
            selected_chat_count=0,
            selected_contact_count=1,
            resolved_contact_count=1,
            inferred_contact_count=0,
            message_count=20,
            message_window_before=2,
            message_window_after=2,
            token_budget=1000,
            scope_status="resolved",
            retrieval_status="ok",
            retrieval_cards_count=0,
            retrieval_messages_count=0,
            started_at=1770200000,
            finished_at=1770200001,
            created_at=1770200000,
            updated_at=1770200001,
        )
        session.add(run)
        await session.flush()
        session.add_all(
            [
                _advisor_contact_finding(
                    run_id=run.id,
                    run_key=run.run_id,
                    finding_id="finding-unmerge-source",
                    target_contact_id=tg.id,
                    created_at=1770200100,
                ),
                _advisor_contact_finding(
                    run_id=run.id,
                    run_key=run.run_id,
                    finding_id="finding-unmerge-canonical",
                    target_contact_id=wa.id,
                    created_at=1770200101,
                ),
            ]
        )
        await session.commit()

    resp = client.post(f"/api/contacts/{tg.id}/unmerge")

    assert resp.status_code == 200
    async with maker() as session:
        rows = {
            row.finding_id: row
            for row in (
                await session.execute(
                    select(AdvisorFinding).where(
                        AdvisorFinding.finding_id.in_(
                            ["finding-unmerge-source", "finding-unmerge-canonical"]
                        )
                    )
                )
            )
            .scalars()
            .all()
        }

    assert rows["finding-unmerge-source"].status == "invalidated"
    assert rows["finding-unmerge-source"].invalidation_reason == "contact_unmerged"
    assert rows["finding-unmerge-source"].invalidated_at is not None
    assert rows["finding-unmerge-canonical"].status == "invalidated"
    assert rows["finding-unmerge-canonical"].invalidation_reason == "contact_unmerged"
    assert rows["finding-unmerge-canonical"].invalidated_at is not None


@pytest.mark.asyncio
async def test_post_unmerge_marks_projection_stale_before_deferred_recompute(
    app_client,
    monkeypatch,
):
    """Unmerge must invalidate projection metadata even when recompute is deferred."""
    client, maker = app_client

    async def noop_recompute():
        return None

    monkeypatch.setattr(contacts_routes, "_run_recompute_in_new_session", noop_recompute)
    async with maker() as session:
        tg = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:tg")
            )
        ).scalar_one()
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()
        tg.merged_into_id = wa.id
        session.add(
            GraphProjectionState(
                projection_id="relationship_map_default",
                projection_version="graph_projection_v1",
                active_cache_key="graph_projection_v1:nodes=2:edges=1:last=1714608000",
                active_node_count=2,
                active_edge_count=1,
                active_built_at=1714608000,
                status="ready",
                progress_completed=3,
                progress_total=3,
                progress_stage="ready",
                cancel_requested=False,
                rebuild_started_at=1714607999,
                rebuild_finished_at=1714608000,
                created_at=1714607999,
                updated_at=1714608000,
            )
        )
        await session.commit()

    resp = client.post(f"/api/contacts/{tg.id}/unmerge")

    assert resp.status_code == 200
    async with maker() as session:
        state = (await session.execute(select(GraphProjectionState))).scalar_one()
    assert state.status == "stale"
    assert state.progress_stage == "contact_unmerge"
    assert state.active_cache_key == "graph_projection_v1:nodes=2:edges=1:last=1714608000"
    assert state.cancel_requested is False


@pytest.mark.asyncio
async def test_post_unmerge_idempotent_already_canonical(app_client):
    """Unmerging a contact that has no merged_into_id → 200 no-op."""
    client, maker = app_client
    async with maker() as session:
        wa = (
            await session.execute(
                select(Contact).where(Contact.beeper_contact_id == "@alice:wa")
            )
        ).scalar_one()

    resp = client.post(f"/api/contacts/{wa.id}/unmerge")
    assert resp.status_code == 200
    assert resp.json()["status"] == "unmerged"


@pytest.mark.asyncio
async def test_post_unmerge_404_unknown(app_client):
    """Unknown contact_id → 404."""
    client, _ = app_client
    resp = client.post("/api/contacts/99999/unmerge")
    assert resp.status_code == 404
