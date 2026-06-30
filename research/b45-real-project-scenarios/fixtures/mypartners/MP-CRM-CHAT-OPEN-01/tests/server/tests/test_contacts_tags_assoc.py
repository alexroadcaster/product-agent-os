# tests/test_contacts_tags_assoc.py
"""Tests for contact-tag association endpoints (Plan 4a T4.2).

Covers:
- POST /api/contacts/{id}/tags            — attach tag to contact
- DELETE /api/contacts/{id}/tags/{tag_id} — detach tag
- Idempotent re-POST → 200
- 404 on missing contact or tag
- 204 on successful DELETE
"""
from __future__ import annotations

import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Contact, ContactTag, Tag
from app.db.session import init_session_factory
from app.main import create_app


@pytest_asyncio.fixture
async def app_client():
    """In-memory DB seeded with one contact and two tags."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    maker = async_sessionmaker(engine, expire_on_commit=False)
    init_session_factory(engine)

    async with maker() as session:
        contact = Contact(
            beeper_contact_id="@alice:tg",
            account_id="acc1",
            network="telegram",
            first_name="Alice",
        )
        tag_vip = Tag(name="VIP", color="#ca8a04")
        tag_prospect = Tag(name="Prospect", color="#f97316")
        session.add_all([contact, tag_vip, tag_prospect])
        await session.flush()
        # Pre-attach VIP tag
        session.add(ContactTag(contact_id=contact.id, tag_id=tag_vip.id))
        await session.commit()

        # Store IDs for use in tests via app state
        app = create_app()
        app.state.contact_id = contact.id
        app.state.tag_vip_id = tag_vip.id
        app.state.tag_prospect_id = tag_prospect.id

    yield app
    await engine.dispose()


# ---------------------------------------------------------------------------
# POST /api/contacts/{id}/tags — attach tag
# ---------------------------------------------------------------------------


def test_attach_tag_returns_200(app_client):
    client = TestClient(app_client)
    contact_id = app_client.state.contact_id
    prospect_id = app_client.state.tag_prospect_id
    resp = client.post(f"/api/contacts/{contact_id}/tags", json={"tag_id": prospect_id})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "attached"


def test_attach_tag_idempotent(app_client):
    """Re-POST the same tag → 200, no error, no duplicate row."""
    client = TestClient(app_client)
    contact_id = app_client.state.contact_id
    vip_id = app_client.state.tag_vip_id
    # VIP already attached by fixture
    resp = client.post(f"/api/contacts/{contact_id}/tags", json={"tag_id": vip_id})
    assert resp.status_code == 200
    assert resp.json()["status"] == "attached"


def test_attach_tag_contact_404(app_client):
    client = TestClient(app_client)
    vip_id = app_client.state.tag_vip_id
    resp = client.post("/api/contacts/9999/tags", json={"tag_id": vip_id})
    assert resp.status_code == 404


def test_attach_tag_tag_404(app_client):
    client = TestClient(app_client)
    contact_id = app_client.state.contact_id
    resp = client.post(f"/api/contacts/{contact_id}/tags", json={"tag_id": 9999})
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# DELETE /api/contacts/{id}/tags/{tag_id}
# ---------------------------------------------------------------------------


def test_detach_tag_returns_204(app_client):
    client = TestClient(app_client)
    contact_id = app_client.state.contact_id
    vip_id = app_client.state.tag_vip_id
    resp = client.delete(f"/api/contacts/{contact_id}/tags/{vip_id}")
    assert resp.status_code == 204


def test_detach_tag_contact_404(app_client):
    client = TestClient(app_client)
    vip_id = app_client.state.tag_vip_id
    resp = client.delete(f"/api/contacts/9999/tags/{vip_id}")
    assert resp.status_code == 404


def test_detach_tag_tag_not_attached_404(app_client):
    """Delete tag that is not attached to the contact → 404."""
    client = TestClient(app_client)
    contact_id = app_client.state.contact_id
    prospect_id = app_client.state.tag_prospect_id
    # Prospect is NOT attached by fixture
    resp = client.delete(f"/api/contacts/{contact_id}/tags/{prospect_id}")
    assert resp.status_code == 404
