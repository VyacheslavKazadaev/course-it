import pytest
from unittest.mock import MagicMock
from repo.db import PostgreSQLConnection


@pytest.fixture
def mock_db_connection():
    """Фикстура для мокирования подключения к базе данных"""
    mock_db = MagicMock(spec=PostgreSQLConnection)
    mock_db.connect.return_value = True
    return mock_db


@pytest.fixture
def sample_user_data():
    """Фикстура с образцом данных пользователя"""
    return {
        "id": 1,
        "username": "test_user",
        "email": "test@example.com"
    }