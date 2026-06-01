from app.worker import run


def test_run():
    assert run() == "ok"
