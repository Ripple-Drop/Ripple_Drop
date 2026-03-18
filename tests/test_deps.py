from collections.abc import Iterator
from contextlib import suppress

from app.api.deps import get_db
from pytest import MonkeyPatch


class DummySession:
    def __init__(self) -> None:
        self.closed = False

    def close(self) -> None:
        self.closed = True


def test_get_db_yields_session_and_closes(monkeypatch: MonkeyPatch) -> None:
    dummy = DummySession()

    monkeypatch.setattr("app.api.deps.SessionLocal", lambda: dummy)

    gen = get_db()

    assert isinstance(gen, Iterator)

    session = next(gen)
    assert session is dummy
    assert dummy.closed is False

    with suppress(StopIteration):
        next(gen)
