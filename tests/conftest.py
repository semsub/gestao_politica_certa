"""Shared test fixtures — every test gets a fresh in-memory database and a
temporary upload folder so tests are fully isolated and deterministic."""

import os
import tempfile

import pytest

from app import create_app, db as _db, Usuario


@pytest.fixture()
def app(tmp_path):
    """Create an application instance configured for testing.

    Key anti-flakiness measures:
    - In-memory SQLite so each test starts with a blank database.
    - Temporary upload folder cleaned up automatically by pytest.
    - TESTING flag enabled for better error propagation.
    """
    upload_dir = str(tmp_path / "uploads")
    os.makedirs(upload_dir, exist_ok=True)

    test_config = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "UPLOAD_FOLDER": upload_dir,
        "WTF_CSRF_ENABLED": False,
    }

    application = create_app(config=test_config)

    with application.app_context():
        _db.create_all()

        # Seed the master admin user (required by several routes)
        master = Usuario(
            nome="JUNIOR ARAUJO",
            login="junior.araujo21",
            senha=os.environ.get("MASTER_PASSWORD", "admin"),
            nivel="ADM",
        )
        _db.session.add(master)
        _db.session.commit()

    yield application

    # Teardown: drop all tables so the next test starts clean
    with application.app_context():
        _db.session.remove()
        _db.drop_all()


@pytest.fixture()
def client(app):
    """A Flask test client bound to the test app."""
    return app.test_client()


@pytest.fixture()
def db(app):
    """Provide the SQLAlchemy instance inside an app context."""
    with app.app_context():
        yield _db


@pytest.fixture()
def admin_session(client, db):
    """Log in as the master admin (user_id=0) and return the client.

    Using a deterministic session avoids flaky auth-state issues.
    """
    with client.session_transaction() as sess:
        sess["user_id"] = 0
        sess["nivel"] = "ADM"
    return client


@pytest.fixture()
def regular_user(client, db):
    """Create a regular LIDERANCA user, log in, and return (client, user)."""
    user = Usuario(
        nome="Test Leader",
        login="test.leader",
        senha="test123",
        nivel="LIDERANÇA",
        municipio="Belém",
    )
    db.session.add(user)
    db.session.commit()

    user_id = user.id
    with client.session_transaction() as sess:
        sess["user_id"] = user_id
        sess["nivel"] = "LIDERANÇA"
    return client, user
