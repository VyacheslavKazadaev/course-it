import sys
import os
# Добавляем родительскую директорию в путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import MagicMock, patch
from repo.db import PostgreSQLConnection


class TestPostgreSQLConnection:
    @pytest.fixture
    def mock_db_connection(self):
        """Фикстура для создания экземпляра PostgreSQLConnection с замокированным psycopg2"""
        with patch('repo.db.psycopg2'):
            db = PostgreSQLConnection(host='localhost', database='testdb', user='testuser', password='testpass')
            yield db

    def test_connect_success(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_db_connection.connection = mock_connection
        
        # Выполнение
        result = mock_db_connection.connect()

        # Проверка
        assert result is True
        assert mock_db_connection.connection is not None

    def test_connect_failure(self):
        # Подготовка
        with patch('repo.db.psycopg2.connect') as mock_connect:
            mock_connect.side_effect = Exception("Connection failed")
            
            db = PostgreSQLConnection(host='invalid_host', database='testdb', user='testuser', password='testpass')

            # Выполнение
            result = db.connect()

            # Проверка
            assert result is False
            assert db.connection is None

    def test_execute_query_success(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'username': 'test', 'email': 'test@example.com'},
            {'id': 2, 'username': 'test2', 'email': 'test2@example.com'}
        ]
        
        mock_db_connection.connection = mock_connection

        # Выполнение
        result = mock_db_connection.execute_query("SELECT * FROM users WHERE id > %s", (0,))

        # Проверка
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['username'] == 'test'
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id > %s", (0,))
        mock_cursor.fetchall.assert_called_once()

    def test_execute_query_no_connection(self, mock_db_connection):
        # Подготовка
        mock_db_connection.connection = None

        # Выполнение
        result = mock_db_connection.execute_query("SELECT * FROM users")

        # Проверка
        assert result is None

    def test_execute_query_exception(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.side_effect = Exception("Query failed")
        
        mock_db_connection.connection = mock_connection

        # Выполнение
        result = mock_db_connection.execute_query("SELECT * FROM users")

        # Проверка
        assert result is None

    def test_execute_command_success(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        
        mock_db_connection.connection = mock_connection

        # Выполнение
        result = mock_db_connection.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)", ("test", "test@example.com"))

        # Проверка
        assert result is True
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, email) VALUES (%s, %s)", ("test", "test@example.com"))
        mock_connection.commit.assert_called_once()

    def test_execute_command_with_returning_id(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)  # ID новой записи
        
        mock_db_connection.connection = mock_connection

        # Выполнение
        result = mock_db_connection.execute_command("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", ("test", "test@example.com"), returning_id=True)

        # Проверка
        assert result == 1
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", ("test", "test@example.com"))
        mock_cursor.fetchone.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_execute_command_no_connection(self, mock_db_connection):
        # Подготовка
        mock_db_connection.connection = None

        # Выполнение
        result = mock_db_connection.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)")

        # Проверка
        assert result is False

    def test_execute_command_exception(self, mock_db_connection):
        # Подготовка
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.side_effect = Exception("Command failed")
        
        mock_db_connection.connection = mock_connection

        # Выполнение
        result = mock_db_connection.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)")

        # Проверка
        assert result is False
        mock_connection.rollback.assert_called_once()

    def test_close_connection(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        db.connection = mock_connection

        # Выполнение
        db.close()

        # Проверка
        assert db.connection is not None
        mock_connection.close.assert_called_once()