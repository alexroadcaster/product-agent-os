# tests/test_contacts_get_one.py
"""Tests for GET /api/contacts/{contact_id} — single-contact deep view (Plan 4a T2.1)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Contact, ContactNote, ContactTag, Tag
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
        # Canonical contact
        canonical = Contact(
            beeper_contact_id="@ivan:telegram",
            account_id="acc_tg",
            network="telegram",
            username="ivan",
            first_name="Иван",
            last_name=None,
        )
        session.add(canonical)
        await session.flush()

        # Tag
        tag = Tag(name="client", color="#ca8a04")
        session.add(tag)
        await session.flush()

        ct = ContactTag(contact_id=canonical.id, tag_id=tag.id)
        session.add(ct)

        # Note
        note = ContactNote(
            contact_id=canonical.id, note_text="VIP", updated_at=1714608000
        )
        session.add(note)

        # Merged-source contact pointing to canonical
        merged = Contact(
            beeper_contact_id="@ivan:whatsapp",
            account_id="acc_wa",
            network="whatsapp",
            first_name="Иван",
            merged_into_id=canonical.id,
        )
        session.add(merged)
        await session.commit()

    yield create_app(), canonical.id, merged.id
    await engine.dispose()


def test_get_contact_deep_view(app_with_db):
    """Happy path: canonical contact returns tags, note and merged_sources."""
    app, canonical_id, _ = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{canonical_id}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == canonical_id
    assert data["first_name"] == "Иван"
    assert data["network"] == "telegram"
    assert data["is_merged"] is False
    assert len(data["tags"]) == 1
    assert data["tags"][0]["name"] == "client"
    assert data["note"]["note_text"] == "VIP"
    assert data["note"]["updated_at"] == 1714608000
    # merged_sources contains the whatsapp duplicate
    assert len(data["merged_sources"]) == 1
    assert data["merged_sources"][0]["network"] == "whatsapp"
    # networks includes both platforms
    assert "telegram" in data["networks"]
    assert "whatsapp" in data["networks"]


def test_get_contact_merged_source_redirects_to_canonical(app_with_db):
    """Hitting a merged-source id transparently returns the canonical contact."""
    app, canonical_id, merged_id = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{merged_id}")
    assert resp.status_code == 200
    data = resp.json()
    # Returns canonical
    assert data["id"] == canonical_id


def test_get_contact_404_unknown(app_with_db):
    """Unknown id returns 404 with detail contact_not_found."""
    app, _, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts/99999")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "contact_not_found"
