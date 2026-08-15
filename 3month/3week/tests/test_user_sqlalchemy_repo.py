import sys
import os
# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, Mock
from repo.users_sqlalchemy import UserSQLAlchemyRepo
from model.user import User


class TestUserSQLAlchemyRepo:
    def test_get_users_success(self):
        # Подготовка
        mock_session = MagicMock()
        mock_user1 = User(id=1, username="test1", email="test1@example.com")
        mock_user2 = User(id=2, username="test2", email="test2@example.com")
        mock_session.execute.return_value.scalars().all.return_value = [mock_user1, mock_user2]
        
        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.get_users()

        # Проверка
        expected_result = [
            {"id": 1, "username": "test1", "email": "test1@example.com"},
            {"id": 2, "username": "test2", "email": "test2@example.com"}
        ]
        assert result == expected_result
        mock_session.execute.assert_called_once()

    def test_get_user_found(self):
        # Подготовка
        mock_session = MagicMock()
        mock_user = User(id=1, username="test", email="test@example.com")
        mock_session.execute.return_value.scalar_one_or_none.return_value = mock_user
        
        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.get_user(1)

        # Проверка
        expected_result = {"id": 1, "username": "test", "email": "test@example.com"}
        assert result == expected_result
        mock_session.execute.assert_called_once()

    def test_get_user_not_found(self):
        # Подготовка
        mock_session = MagicMock()
        mock_session.execute.return_value.scalar_one_or_none.return_value = None
        
        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.get_user(1)

        # Проверка
        assert result == {}
        mock_session.execute.assert_called_once()

    def test_save_user_success(self):
        # Подготовка
        mock_session = MagicMock()
        # Создаем мок-объект User, который будет добавлен в сессию
        mock_user = Mock(spec=User)
        mock_user.id = 123 # Предполагаем, что flush() присвоит id
        mock_user.username = "test"
        mock_user.email = "test@example.com"

        # Изменяем поведение session.add и session.flush
        # session.add сохранит ссылку на объект
        added_obj = None
        def side_effect_add(obj):
            nonlocal added_obj
            added_obj = obj
        mock_session.add.side_effect = side_effect_add
        # session.flush "присвоит" id мок-объекту
        def side_effect_flush():
            if added_obj is not None:
                # Пример: присваиваем id, как это делает SQLAlchemy
                # В тесте мы просто устанавливаем его вручную
                added_obj.id = mock_user.id
        mock_session.flush.side_effect = side_effect_flush

        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.save_user("test", "test@example.com")

        # Проверка
        # Проверяем, что объект User был создан и добавлен в сессию
        mock_session.add.assert_called_once()
        mock_session.flush.assert_called_once()
        # Не проверяем commit/rollback, так как repo сам их не вызывает
        # Проверяем, что возвращаемое значение имеет правильную структуру
        # Теперь мы можем получить id из мок-объекта, который был добавлен
        assert "id" in result
        assert isinstance(result["id"], int)
        assert result["username"] == "test"
        assert result["email"] == "test@example.com"

    def test_delete_user_success(self):
        # Подготовка
        mock_session = MagicMock()
        # Для успешного удаления rowcount должен быть > 0
        # Мы можем заставить delete_user возвращать True, изменив поведение execute
        mock_result_proxy = MagicMock()
        mock_result_proxy.rowcount = 1  # Один ряд удален
        mock_session.execute.return_value = mock_result_proxy
        
        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.delete_user(1)

        # Проверка
        # Метод delete_user возвращает bool. True, если что-то удалено.
        assert result is True # Убедиться, что метод вернул True
        mock_session.execute.assert_called_once()

    def test_delete_user_not_found(self):
        # Подготовка
        mock_session = MagicMock()
        mock_result_proxy = MagicMock()
        mock_result_proxy.rowcount = 0  # Ни одного ряда не удалено
        mock_session.execute.return_value = mock_result_proxy
        
        user_repo = UserSQLAlchemyRepo(mock_session)

        # Выполнение
        result = user_repo.delete_user(1)

        # Проверка
        # Метод delete_user возвращает bool. False, если ничего не удалено.
        assert result is False # Убедиться, что метод вернул False
        mock_session.execute.assert_called_once()
        # rollback не вызывается внутри repo, а в сервисе. Тест на repo не проверяет работу сервиса.