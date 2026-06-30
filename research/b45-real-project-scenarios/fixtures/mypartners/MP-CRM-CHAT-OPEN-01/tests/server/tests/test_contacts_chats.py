# tests/test_contacts_chats.py
"""Tests for GET /api/contacts/{contact_id}/chats — chat list for contact (Plan 4a T2.5)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Chat, ChatMember, Contact, Message
from app.db.session import init_session_factory
from app.main import create_app


class FakeBeeperClient:
    def __init__(self):
        self.focused_chat_ids = []

    async def focus_chat(self, chat_id: str) -> bool:
        self.focused_chat_ids.append(chat_id)
        return True


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

        chat1 = Chat(
            beeper_chat_id="!chat1:telegram",
            account_id="acc1",
            network="telegram",
            type="single",
            title="Personal chat Ivan",
            participants_count=2,
            last_activity_ts=1714608000,
        )
        chat2 = Chat(
            beeper_chat_id="!chat2:telegram",
            account_id="acc1",
            network="telegram",
            type="group",
            title="Группа",
            participants_count=5,
            last_activity_ts=1714608100,
        )
        session.add(chat1)
        session.add(chat2)
        await session.flush()

        session.add(ChatMember(chat_id=chat1.id, contact_id=contact.id))
        session.add(ChatMember(chat_id=chat2.id, contact_id=contact.id))
        session.add_all(
            [
                Message(
                    beeper_message_id="msg-outbound",
                    chat_id=chat1.id,
                    sender_beeper_id="@me:telegram",
                    sender_name="Me",
                    text="outbound",
                    timestamp=1714608001,
                    network="telegram",
                    account_id="acc1",
                    is_sender=True,
                ),
                Message(
                    beeper_message_id="msg-inbound",
                    chat_id=chat2.id,
                    sender_beeper_id="@ivan:telegram",
                    sender_name="Ivan",
                    text="inbound only",
                    timestamp=1714608101,
                    network="telegram",
                    account_id="acc1",
                    is_sender=False,
                ),
                Message(
                    beeper_message_id="msg-deleted-outbound",
                    chat_id=chat2.id,
                    sender_beeper_id="@me:telegram",
                    sender_name="Me",
                    text="deleted outbound",
                    timestamp=1714608102,
                    network="telegram",
                    account_id="acc1",
                    is_sender=True,
                    deleted_at=1714608103,
                ),
            ]
        )
        await session.commit()

    yield create_app(), contact.id
    await engine.dispose()


def test_get_chats_happy_path(app_with_db):
    """Returns chats where contact is a member, sorted by last_activity_ts DESC."""
    app, cid = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/chats")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) == 2
    # Sorted DESC — newer chat first
    assert data["items"][0]["last_activity_ts"] >= data["items"][1]["last_activity_ts"]
    # Shape check
    first = data["items"][0]
    assert "id" in first
    assert "beeper_chat_id" in first
    assert "title" in first
    assert "type" in first
    assert "network" in first
    assert "participants_count" in first
    assert "last_activity_ts" in first
    assert "local_user_message_count" in first
    assert "has_local_user_messages" in first
    assert "open_target" in first
    by_beeper_chat_id = {item["beeper_chat_id"]: item for item in data["items"]}
    direct = by_beeper_chat_id["!chat1:telegram"]
    read_only = by_beeper_chat_id["!chat2:telegram"]
    assert direct["local_user_message_count"] == 1
    assert direct["has_local_user_messages"] is True
    assert direct["open_target"] == {
        "method": "beeper_chat",
        "status": "available",
        "value": "!chat1:telegram",
    }
    assert read_only["local_user_message_count"] == 0
    assert read_only["has_local_user_messages"] is False


def test_get_chats_404_unknown(app_with_db):
    """Unknown contact id returns 404."""
    app, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts/99999/chats")
    assert resp.status_code == 404


def test_open_contact_chat_focuses_beeper_after_membership_check(app_with_db):
    app, cid = app_with_db
    fake_beeper = FakeBeeperClient()
    app.state.beeper_client = fake_beeper
    client = TestClient(app)

    chats = client.get(f"/api/contacts/{cid}/chats").json()["items"]
    chat_id = next(item["id"] for item in chats if item["beeper_chat_id"] == "!chat1:telegram")

    resp = client.post(f"/api/contacts/{cid}/chats/{chat_id}/open")

    assert resp.status_code == 200
    assert resp.json() == {
        "chat_id": chat_id,
        "contact_id": cid,
        "method": "beeper_focus",
        "status": "opened",
    }
    assert fake_beeper.focused_chat_ids == ["!chat1:telegram"]


def test_open_contact_chat_rejects_unknown_membership(app_with_db):
    app, cid = app_with_db
    app.state.beeper_client = FakeBeeperClient()
    client = TestClient(app)

    resp = client.post(f"/api/contacts/{cid}/chats/99999/open")

    assert resp.status_code == 404
    assert resp.json()["detail"] == "chat_not_found"
