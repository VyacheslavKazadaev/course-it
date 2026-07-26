import pytest
from unittest.mock import MagicMock
from repo.users import UserRepo


class TestUserRepo:
    def test_get_users_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        expected_users = [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_db.execute_query.return_value = expected_users
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.get_users()

        # Проверка
        assert result == expected_users
        mock_db.connect.assert_called_once()
        mock_db.execute_query.assert_called_once_with("SELECT * FROM users")
        mock_db.close.assert_called_once()

    def test_get_users_connection_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = False
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.get_users()

        # Проверка
        assert result == {"error": "Database connection failed"}
        mock_db.connect.assert_called_once()
        mock_db.execute_query.assert_not_called()
        mock_db.close.assert_not_called()  # close не должен вызываться при ошибке подключения

    def test_get_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        expected_user = [{"id": 1, "username": "test", "email": "test@example.com"}]
        mock_db.execute_query.return_value = expected_user
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.get_user(1)

        # Проверка
        assert result == expected_user
        mock_db.connect.assert_called_once()
        mock_db.execute_query.assert_called_once_with("SELECT * FROM users WHERE id = %s", (1,))
        mock_db.close.assert_called_once()

    def test_get_user_connection_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = False
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.get_user(1)

        # Проверка
        assert result == {"error": "Database connection failed"}
        mock_db.connect.assert_called_once()
        mock_db.execute_query.assert_not_called()
        mock_db.close.assert_not_called()

    def test_save_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        mock_db.execute_command.return_value = 1  # ID нового пользователя
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.save_user("test", "test@example.com")

        # Проверка
        expected_result = {"success": True, "user_id": 1, "username": "test", "email": "test@example.com"}
        assert result == expected_result
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_called_once_with(
            "INSERT INTO users (username, email) VALUES (%s, %s)", 
            ("test", "test@example.com"), 
            True
        )
        mock_db.close.assert_called_once()

    def test_save_user_connection_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = False
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.save_user("test", "test@example.com")

        # Проверка
        assert result == {"error": "Database connection failed"}
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_not_called()
        mock_db.close.assert_not_called()

    def test_save_user_insert_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        mock_db.execute_command.return_value = None  # Ошибка вставки
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.save_user("test", "test@example.com")

        # Проверка
        assert result == {"error": "Failed to insert user"}
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_called_once_with(
            "INSERT INTO users (username, email) VALUES (%s, %s)", 
            ("test", "test@example.com"), 
            True
        )
        mock_db.close.assert_called_once()

    def test_delete_user_success(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        mock_db.execute_command.return_value = True  # Успешное удаление
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.delete_user(1)

        # Проверка
        expected_result = {"success": True, "message": "User with id 1 deleted successfully"}
        assert result == expected_result
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_called_once_with("DELETE FROM users WHERE id = %s", (1,))
        mock_db.close.assert_called_once()

    def test_delete_user_connection_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = False
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.delete_user(1)

        # Проверка
        assert result == {"error": "Database connection failed"}
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_not_called()
        mock_db.close.assert_not_called()

    def test_delete_user_failed(self):
        # Подготовка
        mock_db = MagicMock()
        mock_db.connect.return_value = True
        mock_db.execute_command.return_value = False  # Ошибка удаления
        
        user_repo = UserRepo(mock_db)

        # Выполнение
        result = user_repo.delete_user(1)

        # Проверка
        assert result == {"error": "Failed to delete user with id 1"}
        mock_db.connect.assert_called_once()
        mock_db.execute_command.assert_called_once_with("DELETE FROM users WHERE id = %s", (1,))
        mock_db.close.assert_called_once()