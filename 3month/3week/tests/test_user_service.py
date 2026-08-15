import sys
import os
# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, patch
from service.user import UserService


class TestUserServiceWithSQLAlchemy:
    @patch('service.user.UserSQLAlchemyRepo')  # Заглушка для репозитория
    def test_get_users_success(self, mock_repo_class):
        # Подготовка
        mock_session = MagicMock()
        mock_repo_instance = MagicMock()
        mock_repo_instance.get_users.return_value = [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_repo_class.return_value = mock_repo_instance # При создании экземпляра возвращаем заглушку

        # Создаем экземпляр UserService с фиктивной session_factory
        session_factory = MagicMock(return_value=mock_session)
        user_service = UserService(session_factory=session_factory)

        # Выполнение
        result = user_service.get_users()

        # Проверка
        assert result == [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_repo_instance.get_users.assert_called_once()

    @patch('service.user.UserSQLAlchemyRepo')
    def test_save_user_success(self, mock_repo_class):
        # Подготовка
        mock_session = MagicMock()
        mock_repo_instance = MagicMock()
        expected_result = {"id": 1, "username": "test", "email": "test@example.com"} # Исправлено возвращаемое значение
        mock_repo_instance.save_user.return_value = expected_result
        mock_repo_class.return_value = mock_repo_instance

        session_factory = MagicMock(return_value=mock_session)
        user_service = UserService(session_factory=session_factory)

        # Выполнение
        result = user_service.save_user("test", "test@example.com")

        # Проверка
        assert result == expected_result
        mock_repo_instance.save_user.assert_called_once_with("test", "test@example.com")
        mock_session.commit.assert_called_once()

    @patch('service.user.UserSQLAlchemyRepo')
    def test_get_user_success(self, mock_repo_class):
        # Подготовка
        mock_session = MagicMock()
        mock_repo_instance = MagicMock()
        expected_result = {"id": 1, "username": "test", "email": "test@example.com"}
        mock_repo_instance.get_user.return_value = expected_result
        mock_repo_class.return_value = mock_repo_instance

        session_factory = MagicMock(return_value=mock_session)
        user_service = UserService(session_factory=session_factory)

        # Выполнение
        result = user_service.get_user(1)

        # Проверка
        assert result == expected_result
        mock_repo_instance.get_user.assert_called_once_with(1)

    @patch('service.user.UserSQLAlchemyRepo')
    def test_delete_user_success(self, mock_repo_class):
        # Подготовка
        mock_session = MagicMock()
        mock_repo_instance = MagicMock()
        # Возвращаем True из репозитория, что означает успешное удаление
        mock_repo_instance.delete_user.return_value = True
        mock_repo_class.return_value = mock_repo_instance

        session_factory = MagicMock(return_value=mock_session)
        user_service = UserService(session_factory=session_factory)

        # Выполнение
        result = user_service.delete_user(1)

        # Проверка
        expected_result = {"success": True, "message": "User with id 1 deleted successfully"}
        assert result == expected_result
        mock_repo_instance.delete_user.assert_called_once_with(1)
        mock_session.commit.assert_called_once()