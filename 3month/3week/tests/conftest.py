import sys
from unittest.mock import MagicMock
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_db_connection():
    """Фикстура для мокирования подключения к базе данных"""
    mock_db = MagicMock()
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


@pytest.fixture(autouse=True)
def mock_psycopg2():
    """Автоматическая фикстура для мокирования psycopg2"""
    with patch.dict('sys.modules', {
        'psycopg2': MagicMock(),
        'psycopg2.extras': MagicMock()
    }):
        yield