import sys
from pathlib import Path
# Add the parent directory to sys.path to make the 'app' module discoverable
parent_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(parent_dir))

import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.app import App
from model.user import UserInput
from fastapi import FastAPI
import app.http  # Import the http module to register routes

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
        'psycopg2.extras': MagicMock(),
        'sqlalchemy': MagicMock(),
        'sqlalchemy.orm': MagicMock(),
        'sqlalchemy.sql': MagicMock()
    }):
        yield


@pytest.fixture
def mock_sqlalchemy_session():
    """Фикстура для мокирования сессии SQLAlchemy"""
    mock_session = MagicMock()
    return mock_session

@pytest.fixture
def client():
    """Fixture to create a TestClient for the FastAPI application."""
    # Mock the entire App class to avoid calling its __init__ method which connects to the DB
    with patch('app.app.App') as MockApp:
        # Create an instance of the mock
        mock_app_instance = MockApp.return_value
        
        # Create a real FastAPI instance for the TestClient
        real_fastapi_app = FastAPI()
        # Configure the mock App instance to return the real FastAPI app when its `api` property is accessed
        mock_app_instance.api = real_fastapi_app

        # Create mocks for the attributes that tests might expect
        mock_session_factory = MagicMock()
        mock_user_service = MagicMock()
        
        # Assign mocks to the expected attributes on the mock instance
        mock_app_instance.SessionLocal = mock_session_factory
        mock_app_instance.user_service = mock_user_service
        
        # Example mock returns for the service methods
        mock_user_service.get_users.return_value = [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_user_service.save_user.return_value = {"id": 2, "username": "new_user", "email": "new@example.com"}
        mock_user_service.get_user.return_value = {"id": 1, "username": "test", "email": "test@example.com"}
        mock_user_service.delete_user.return_value = {"success": True, "message": "User with id 1 deleted successfully"}

        # Register routes before creating the TestClient
        app.http.register_routes(mock_app_instance)

        client = TestClient(real_fastapi_app)
        # Attach mocks to client so individual tests can configure them differently if needed
        client._mock_user_service = mock_user_service
        client._mock_session = mock_session_factory # Using the factory mock as the '_mock_session' for consistency
        yield client
