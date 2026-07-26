import pytest
from unittest.mock import MagicMock
from service.user import UserService


class TestUserService:
    def test_get_users_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_repo = MagicMock()
        mock_repo.get_users.return_value = [{"id": 1, "username": "test", "email": "test@example.com"}]
        
        user_service = UserService(mock_db)
        user_service.repo = mock_repo

        # Выполнение
        result = user_service.get_users()

        # Проверка
        assert result == [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_repo.get_users.assert_called_once()

    def test_save_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_repo = MagicMock()
        expected_result = {"success": True, "user_id": 1, "username": "test", "email": "test@example.com"}
        mock_repo.save_user.return_value = expected_result
        
        user_service = UserService(mock_db)
        user_service.repo = mock_repo

        # Выполнение
        result = user_service.save_user("test", "test@example.com")

        # Проверка
        assert result == expected_result
        mock_repo.save_user.assert_called_once_with("test", "test@example.com")

    def test_get_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_repo = MagicMock()
        expected_result = [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_repo.get_user.return_value = expected_result
        
        user_service = UserService(mock_db)
        user_service.repo = mock_repo

        # Выполнение
        result = user_service.get_user(1)

        # Проверка
        assert result == expected_result
        mock_repo.get_user.assert_called_once_with(1)

    def test_delete_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_repo = MagicMock()
        expected_result = {"success": True, "message": "User with id 1 deleted successfully"}
        mock_repo.delete_user.return_value = expected_result
        
        user_service = UserService(mock_db)
        user_service.repo = mock_repo

        # Выполнение
        result = user_service.delete_user(1)

        # Проверка
        assert result == expected_result
        mock_repo.delete_user.assert_called_once_with(1)