import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import db as db_module

_fd, _path = tempfile.mkstemp()
os.close(_fd)
db_module.DB_PATH = _path
db_module.init_db()

import app as app_module  # noqa: E402  (must import after DB_PATH is patched)

app_module.app.config.update(TESTING=True)


@pytest.fixture
def app():
    db_module.init_db()
    yield app_module.app
    conn = db_module.get_db()
    conn.execute("DELETE FROM expenses")
    conn.execute("DELETE FROM users")
    conn.commit()
    conn.close()


@pytest.fixture
def client(app):
    return app.test_client()
