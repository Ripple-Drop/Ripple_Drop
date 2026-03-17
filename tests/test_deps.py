from collections.abc import Iterator

from app.api.deps import get_db


class DummySession:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


def test_get_db_yields_session_and_closes(monkeypatch) -> None:
    dummy = DummySession()

    monkeypatch.setattr("app.api.deps.SessionLocal", lambda: dummy)

    gen = get_db()

    assert isinstance(gen, Iterator)

    session = next(gen)
    assert session is dummy
    assert dummy.closed is False

    try:
        next(gen)
    except StopIteration:
        pass

    assert dummy.closed is True