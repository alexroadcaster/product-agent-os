# tests/test_contacts_list_extended.py
"""Tests for extended GET /api/contacts with tag_id, min_weight, include_merged (Plan 4a T2.6)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Contact, ContactTag, Relationship, Tag
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
        # Three canonical contacts
        alice = Contact(
            beeper_contact_id="@alice:telegram",
            account_id="acc1",
            network="telegram",
            first_name="Alice",
        )
        bob = Contact(
            beeper_contact_id="@bob:whatsapp",
            account_id="acc2",
            network="whatsapp",
            first_name="Bob",
        )
        carol = Contact(
            beeper_contact_id="@carol:telegram",
            account_id="acc1",
            network="telegram",
            first_name="Carol",
        )
        session.add_all([alice, bob, carol])
        await session.flush()

        # Merged duplicate of alice (should be hidden by default)
        merged_alice = Contact(
            beeper_contact_id="@alice:whatsapp",
            account_id="acc2",
            network="whatsapp",
            first_name="Alice",
            merged_into_id=alice.id,
        )
        session.add(merged_alice)

        # Tag "vip" on alice
        tag_vip = Tag(name="vip", color="#ca8a04")
        session.add(tag_vip)
        await session.flush()
        session.add(ContactTag(contact_id=alice.id, tag_id=tag_vip.id))

        # Relationship between alice and bob with high weight
        session.add(
            Relationship(
                contact_a_id=alice.id,
                contact_b_id=bob.id,
                weight=0.8,
            )
        )
        await session.commit()

    yield create_app(), alice.id, bob.id, carol.id, tag_vip.id
    await engine.dispose()


def test_list_canonical_only_default(app_with_db):
    """Default listing excludes merged duplicates (include_merged=False)."""
    app, alice_id, bob_id, carol_id, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts")
    assert resp.status_code == 200
    ids = [c["id"] for c in resp.json()["items"]]
    # Three canonical contacts, merged alice duplicate excluded
    assert len(ids) == 3
    assert alice_id in ids
    assert bob_id in ids
    assert carol_id in ids


def test_list_include_merged(app_with_db):
    """include_merged=true returns all rows including merged duplicates."""
    app, _, _, _, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts?include_merged=true")
    assert resp.status_code == 200
    assert resp.json()["total"] == 4


def test_list_filter_by_tag_id(app_with_db):
    """tag_id filter returns only contacts with that tag."""
    app, alice_id, _, _, tag_vip_id = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts?tag_id={tag_vip_id}")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == alice_id


def test_list_filter_by_min_weight(app_with_db):
    """min_weight filter returns only contacts appearing in relationships >= threshold."""
    app, alice_id, bob_id, carol_id, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts?min_weight=0.5")
    assert resp.status_code == 200
    ids = [c["id"] for c in resp.json()["items"]]
    # Alice and Bob are in a relationship with weight 0.8
    assert alice_id in ids
    assert bob_id in ids
    # Carol has no relationships
    assert carol_id not in ids


def test_list_existing_search_still_works(app_with_db):
    """Existing q/network filters still function after T2.6 changes."""
    app, alice_id, _, _, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts?q=Alice")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) == 1
    assert items[0]["id"] == alice_id
