# tests/test_contacts_insights.py
"""Tests for GET /api/contacts/{contact_id}/insights — past insights (Plan 4a T2.4)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import AiInsight, Base, Contact
from app.db.session import init_session_factory
from app.main import create_app


@pytest_asyncio.fixture
async def app_with_db():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    init_session_factory(engine)

    async with maker() as session:
        contact = Contact(
            beeper_contact_id="@ivan:telegram",
            account_id="acc1",
            network="telegram",
            first_name="Иван",
        )
        session.add(contact)
        await session.flush()

        # Insert two insights of different kinds
        session.add(
            AiInsight(
                contact_id=contact.id,
                kind="conversation_analysis",
                subtype=None,
                content="analysis content",
                tokens_in=100,
                tokens_out=200,
                created_at=1714608000,
            )
        )
        session.add(
            AiInsight(
                contact_id=contact.id,
                kind="contact_profile",
                subtype="quarterly_growth_audit",
                content="profile content",
                tokens_in=50,
                tokens_out=100,
                created_at=1714608100,
            )
        )
        await session.commit()

    yield create_app(), contact.id
    await engine.dispose()


def test_get_insights_happy_path(app_with_db):
    """Returns all insights for a contact sorted by created_at DESC."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/insights")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) == 2
    assert data["limit"] == 20
    # Sorted by created_at DESC — newest first
    assert data["items"][0]["created_at"] > data["items"][1]["created_at"]


def test_get_insights_filter_by_kind(app_with_db):
    """kind query param filters to matching insights only."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/insights?kind=contact_profile")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["kind"] == "contact_profile"
    assert items[0]["subtype"] == "quarterly_growth_audit"


def test_get_insights_limit(app_with_db):
    """limit param restricts returned items."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/insights?limit=1")
    assert resp.status_code == 200
    assert len(resp.json()["items"]) == 1


def test_get_insights_404_unknown(app_with_db):
    """Unknown contact id returns 404."""
    app, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts/99999/insights")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "contact_not_found"
