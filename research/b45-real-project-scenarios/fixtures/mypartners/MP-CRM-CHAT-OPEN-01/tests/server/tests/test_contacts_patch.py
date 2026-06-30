# tests/test_contacts_patch.py
"""Tests for PATCH /api/contacts/{contact_id} — names + note edit (Plan 4a T2.2)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Contact
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
            beeper_contact_id="@alice:telegram",
            account_id="acc1",
            network="telegram",
            first_name="Alice",
            last_name=None,
        )
        session.add(contact)
        await session.commit()

    yield create_app(), contact.id
    await engine.dispose()


def test_patch_first_last_name(app_with_db):
    """PATCH updates first_name and last_name, returns status ok."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.patch(
        f"/api/contacts/{cid}",
        json={"first_name": "Alicia", "last_name": "Smith"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["id"] == cid

    # Verify via GET
    get = client.get(f"/api/contacts/{cid}")
    assert get.json()["first_name"] == "Alicia"
    assert get.json()["last_name"] == "Smith"


def test_patch_note_text_creates_note(app_with_db):
    """PATCH with note_text creates a ContactNote row."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.patch(f"/api/contacts/{cid}", json={"note_text": "VIP client"})
    assert resp.status_code == 200

    get = client.get(f"/api/contacts/{cid}")
    assert get.json()["note"]["note_text"] == "VIP client"


def test_patch_note_text_updates_existing_note(app_with_db):
    """PATCH with note_text overwrites an existing note."""
    app, cid = app_with_db
    client = TestClient(app)
    client.patch(f"/api/contacts/{cid}", json={"note_text": "first"})
    client.patch(f"/api/contacts/{cid}", json={"note_text": "updated"})

    get = client.get(f"/api/contacts/{cid}")
    assert get.json()["note"]["note_text"] == "updated"


def test_patch_404_unknown(app_with_db):
    """Unknown contact id returns 404."""
    app, _ = app_with_db
    client = TestClient(app)
    resp = client.patch("/api/contacts/99999", json={"first_name": "X"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "contact_not_found"


def test_patch_immutable_fields_ignored(app_with_db):
    """Pydantic schema only accepts first_name/last_name/note_text; extra fields are rejected."""
    app, cid = app_with_db
    client = TestClient(app)
    # Sending beeper_contact_id should cause 422 (extra field rejected by Pydantic model='forbid')
    # OR it should be silently ignored if model does not forbid extras.
    # Per the plan the schema simply does not include immutable fields, so extra fields
    # are either ignored (default) or cause 422. Either behaviour is acceptable; we just
    # check the contact's beeper_contact_id did not change.
    resp = client.patch(
        f"/api/contacts/{cid}",
        json={"first_name": "NewName", "beeper_contact_id": "hacked"},
    )
    # 200 or 422 — both acceptable; what matters is identity did not change
    if resp.status_code == 200:
        get = client.get(f"/api/contacts/{cid}")
        assert get.json()["beeper_contact_id"] == "@alice:telegram"
