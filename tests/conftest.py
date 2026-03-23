import os
import tempfile
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as flask_app


@pytest.fixture
def client(tmp_path):
    """每个测试使用独立的临时数据库，互不干扰。"""
    db_file = tmp_path / "test.db"
    flask_app.DB_PATH = str(db_file)
    flask_app.init_db()

    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client
