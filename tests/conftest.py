import pytest
from fastapi.testclient import TestClient

from src import storage
from src.main import app


@pytest.fixture(autouse=True)
def isolated_storage(monkeypatch, tmp_path):
    monkeypatch.setattr(storage, "DATA_FILE", tmp_path / "expenses.json")


@pytest.fixture
def client():
    return TestClient(app)