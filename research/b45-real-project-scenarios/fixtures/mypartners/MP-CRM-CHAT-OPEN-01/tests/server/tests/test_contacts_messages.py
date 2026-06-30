# tests/test_contacts_messages.py
"""Tests for GET /api/contacts/{contact_id}/messages — paginated slice (Plan 4a T2.3)."""
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.db.models import Base, Chat, ChatMember, Contact, Message
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

        chat = Chat(
            beeper_chat_id="!chat1:telegram",
            account_id="acc1",
            network="telegram",
            type="single",
            title="Личный чат",
            last_activity_ts=1714608010,
        )
        session.add(chat)
        await session.flush()

        cm = ChatMember(chat_id=chat.id, contact_id=contact.id)
        session.add(cm)

        first_message = Message(
            beeper_message_id="msg0",
            chat_id=chat.id,
            sender_beeper_id="@ivan:telegram",
            sender_name="Ivan",
            text="hello 0",
            timestamp=1714608000,
            network="telegram",
            account_id="acc1",
            is_sender=False,
        )
        session.add(first_message)
        await session.flush()
        session.add_all(
            [
                Message(
                    beeper_message_id="msg1",
                    chat_id=chat.id,
                    sender_beeper_id="@me:telegram",
                    sender_name="Me",
                    text="hello 1",
                    timestamp=1714608005,
                    network="telegram",
                    account_id="acc1",
                    is_sender=True,
                    reply_to_message_id=first_message.id,
                    reply_to_beeper_message_id=first_message.beeper_message_id,
                ),
                Message(
                    beeper_message_id="msg2",
                    chat_id=chat.id,
                    sender_beeper_id="@ivan:telegram",
                    text="hello 2",
                    timestamp=1714608010,
                    network="telegram",
                    account_id="acc1",
                    is_sender=False,
                    reply_to_beeper_message_id="missing-source-message",
                ),
            ]
        )
        session.add_all(
            [
                Message(
                    beeper_message_id="msg-deleted",
                    chat_id=chat.id,
                    sender_beeper_id="@ivan:telegram",
                    text="deleted private text",
                    timestamp=1714608015,
                    network="telegram",
                    account_id="acc1",
                    is_sender=False,
                    deleted_at=1714608020,
                ),
                Message(
                    beeper_message_id="msg-tombstone",
                    chat_id=chat.id,
                    sender_beeper_id="@ivan:telegram",
                    text="tombstoned private text",
                    timestamp=1714608020,
                    network="telegram",
                    account_id="acc1",
                    is_sender=False,
                    is_tombstoned=True,
                ),
            ]
        )

        await session.commit()

    yield create_app(), contact.id, chat.id
    await engine.dispose()


def test_get_messages_happy_path(app_with_db):
    """Returns messages for a contact with default limit."""
    app, cid, _ = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert len(data["items"]) == 3
    assert data["limit"] == 50


def test_get_messages_limit(app_with_db):
    """limit param restricts returned items."""
    app, cid, _ = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages?limit=2")
    assert resp.status_code == 200
    assert len(resp.json()["items"]) == 2


def test_get_messages_chat_id_filter(app_with_db):
    """chat_id filter narrows to a single chat."""
    app, cid, chat_id = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages?chat_id={chat_id}")
    assert resp.status_code == 200
    assert len(resp.json()["items"]) == 3


def test_get_messages_sender_me_filter(app_with_db):
    """sender=me returns only local-user outbound messages."""
    app, cid, chat_id = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages?chat_id={chat_id}&sender=me")

    assert resp.status_code == 200
    items = resp.json()["items"]
    assert [item["text"] for item in items] == ["hello 1"]
    assert all(item["is_sender"] is True for item in items)


def test_get_messages_includes_reply_context(app_with_db):
    """Reply target is restored when the linked local message is visible."""
    app, cid, chat_id = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages?chat_id={chat_id}")

    assert resp.status_code == 200
    items = resp.json()["items"]
    reply = next(item for item in items if item["text"] == "hello 1")
    assert reply["reply_to_missing"] is False
    assert reply["reply_to_message"] == {
        "chat_id": chat_id,
        "id": reply["reply_to_message_id"],
        "is_sender": False,
        "network": "telegram",
        "sender_beeper_id": "@ivan:telegram",
        "sender_name": "Ivan",
        "text": "hello 0",
        "timestamp": 1714608000,
    }
    unresolved = next(item for item in items if item["text"] == "hello 2")
    assert unresolved["reply_to_missing"] is True
    assert unresolved["reply_to_message"] is None


def test_get_messages_ts_bounds(app_with_db):
    """from_ts and to_ts filter by timestamp range."""
    app, cid, _ = app_with_db
    client = TestClient(app)
    resp = client.get(
        f"/api/contacts/{cid}/messages?from_ts=1714608005&to_ts=1714608010"
    )
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert len(items) == 2
    assert all(1714608005 <= item["timestamp"] <= 1714608010 for item in items)


def test_get_messages_next_cursor(app_with_db):
    """next_cursor equals the smallest timestamp in the result set."""
    app, cid, _ = app_with_db
    client = TestClient(app)
    resp = client.get(f"/api/contacts/{cid}/messages?limit=2")
    data = resp.json()
    # next_cursor should be the smallest ts in the returned page
    returned_ts = [item["timestamp"] for item in data["items"]]
    assert data["next_cursor"] == min(returned_ts)


def test_get_messages_404_unknown_contact(app_with_db):
    """Unknown contact id returns 404."""
    app, _, _ = app_with_db
    client = TestClient(app)
    resp = client.get("/api/contacts/99999/messages")
    assert resp.status_code == 404
    assert resp.json()["detail"] == "contact_not_found"
