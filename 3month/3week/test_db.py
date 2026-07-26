import pytest
from unittest.mock import MagicMock, patch
from repo.db import PostgreSQLConnection


class TestPostgreSQLConnection:
    @patch('repo.db.psycopg2.connect')
    def test_connect_success(self, mock_connect):
        # Подготовка
        mock_connection = MagicMock()
        mock_connect.return_value = mock_connection
        
        db = PostgreSQLConnection(host='localhost', database='testdb', user='testuser', password='testpass')

        # Выполнение
        result = db.connect()

        # Проверка
        assert result is True
        mock_connect.assert_called_once_with(
            host='localhost',
            port=5432,
            database='testdb',
            user='testuser',
            password='testpass'
        )
        assert db.connection == mock_connection

    @patch('repo.db.psycopg2.connect')
    def test_connect_failure(self, mock_connect):
        # Подготовка
        mock_connect.side_effect = Exception("Connection failed")
        
        db = PostgreSQLConnection(host='invalid_host', database='testdb', user='testuser', password='testpass')

        # Выполнение
        result = db.connect()

        # Проверка
        assert result is False
        mock_connect.assert_called_once()
        assert db.connection is None

    def test_execute_query_success(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [
            {'id': 1, 'username': 'test', 'email': 'test@example.com'},
            {'id': 2, 'username': 'test2', 'email': 'test2@example.com'}
        ]
        
        db.connection = mock_connection

        # Выполнение
        result = db.execute_query("SELECT * FROM users WHERE id > %s", (0,))

        # Проверка
        assert len(result) == 2
        assert result[0]['id'] == 1
        assert result[0]['username'] == 'test'
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("SELECT * FROM users WHERE id > %s", (0,))
        mock_cursor.fetchall.assert_called_once()

    def test_execute_query_no_connection(self):
        # Подготовка
        db = PostgreSQLConnection()
        db.connection = None

        # Выполнение
        result = db.execute_query("SELECT * FROM users")

        # Проверка
        assert result is None

    def test_execute_query_exception(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.side_effect = Exception("Query failed")
        
        db.connection = mock_connection

        # Выполнение
        result = db.execute_query("SELECT * FROM users")

        # Проверка
        assert result is None

    def test_execute_command_success(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.return_value = None
        
        db.connection = mock_connection

        # Выполнение
        result = db.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)", ("test", "test@example.com"))

        # Проверка
        assert result is True
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, email) VALUES (%s, %s)", ("test", "test@example.com"))
        mock_connection.commit.assert_called_once()

    def test_execute_command_with_returning_id(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)  # ID новой записи
        
        db.connection = mock_connection

        # Выполнение
        result = db.execute_command("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", ("test", "test@example.com"), returning_id=True)

        # Проверка
        assert result == 1
        mock_connection.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id", ("test", "test@example.com"))
        mock_cursor.fetchone.assert_called_once()
        mock_connection.commit.assert_called_once()

    def test_execute_command_no_connection(self):
        # Подготовка
        db = PostgreSQLConnection()
        db.connection = None

        # Выполнение
        result = db.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)")

        # Проверка
        assert result is False

    def test_execute_command_exception(self):
        # Подготовка
        db = PostgreSQLConnection()
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connection.cursor.return_value.__enter__.side_effect = Exception("Command failed")
        
        db.connection = mock_connection

        # Выполнение
        result = db.execute_command("INSERT INTO users (username, email) VALUES (%s, %s)")

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