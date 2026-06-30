# tests/test_contacts_routes.py
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
        session.add_all([
            Contact(beeper_contact_id="@alice:local-telegram.localhost",
                    account_id="local-telegram_ba_abc", network="telegram",
                    first_name="Alice", username="alice"),
            Contact(beeper_contact_id="@bob:local-whatsapp.localhost",
                    account_id="local-whatsapp_ba_def", network="whatsapp",
                    first_name="Bob"),
        ])
        await session.commit()

    yield create_app()
    await engine.dispose()


def test_get_all_contacts(app_with_db):
    client = TestClient(app_with_db)
    resp = client.get("/api/contacts")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 2


def test_filter_by_network(app_with_db):
    client = TestClient(app_with_db)
    resp = client.get("/api/contacts?network=telegram")
    assert resp.status_code == 200
    items = resp.json()["items"]
    assert all(c["network"] == "telegram" for c in items)
    assert len(items) == 1


def test_pagination(app_with_db):
    client = TestClient(app_with_db)
    resp = client.get("/api/contacts?limit=1&offset=0")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert data["total"] == 2
