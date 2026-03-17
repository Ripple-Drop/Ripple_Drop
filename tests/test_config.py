import importlib

from app.core.config import Settings


def test_settings_database_url() -> None:
    settings = Settings(
        DATABASE="mysql+pymysql",
        DATABASE_HOST="localhost",
        DATABASE_PORT=3306,
        DATABASE_USER="user",
        DATABASE_PASSWORD="pass",
        DATABASE_NAME="mydb",
    )

    assert (
        settings.DATABASE_URL
        == "mysql+pymysql://user:pass@localhost:3306/mydb"
    )


def test_global_settings_can_be_reloaded_from_env(monkeypatch) -> None:
    monkeypatch.setenv("DATABASE", "mysql+pymysql")
    monkeypatch.setenv("DATABASE_HOST", "127.0.0.1")
    monkeypatch.setenv("DATABASE_PORT", "3307")
    monkeypatch.setenv("DATABASE_USER", "tester")
    monkeypatch.setenv("DATABASE_PASSWORD", "secret")
    monkeypatch.setenv("DATABASE_NAME", "ripple")

    import app.core.config as config_module

    reloaded = importlib.reload(config_module)

    assert reloaded.settings.DATABASE == "mysql+pymysql"
    assert reloaded.settings.DATABASE_HOST == "127.0.0.1"
    assert reloaded.settings.DATABASE_PORT == 3307
    assert reloaded.settings.DATABASE_USER == "tester"
    assert reloaded.settings.DATABASE_PASSWORD == "secret"
    assert reloaded.settings.DATABASE_NAME == "ripple"
    assert (
        reloaded.settings.DATABASE_URL
        == "mysql+pymysql://tester:secret@127.0.0.1:3307/ripple"
    )