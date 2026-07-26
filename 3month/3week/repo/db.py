import psycopg2
from psycopg2.extras import RealDictCursor
import os
from typing import Optional, Dict, Any, Union

class PostgreSQLConnection:
    """ Пример использования:
    
    if __name__ == "__main__":
        db = PostgreSQLConnection(
            host='localhost',
            database='testdb',
            user='username',
            password='password'
        )
        
        if db.connect():
            # Пример выполнения SELECT запроса
            results = db.execute_query("SELECT * FROM users WHERE age > %s", (18,))
            if results:
                for row in results:
                    print(row)
            
            # Пример выполнения INSERT команды
            success = db.execute_command(
                "INSERT INTO users (name, email, age) VALUES (%s, %s, %s)",
                ("John Doe", "john@example.com", 30)
            )
            if success:
                print("User inserted successfully")
            
            db.close()
    """
    def __init__(self, host: str = None, port: int = None, database: str = None, 
                 user: str = None, password: str = None):
        """
        Инициализация подключения к базе данных PostgreSQL
        
        Args:
            host: Адрес сервера базы данных
            port: Порт подключения
            database: Название базы данных
            user: Имя пользователя
            password: Пароль пользователя
        """
        self.host = host or os.getenv('DB_HOST', 'localhost')
        self.port = port or int(os.getenv('DB_PORT', 5432))
        self.database = database or os.getenv('DB_NAME', 'postgres')
        self.user = user or os.getenv('DB_USER', 'postgres')
        self.password = password or os.getenv('DB_PASSWORD', '')
        self.connection = None
    
    def connect(self) -> bool:
        """
        Устанавливает подключение к базе данных
        
        Returns:
            bool: True если подключение успешно установлено, иначе False
        """
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print("Successfully connected to PostgreSQL")
            return True
        except Exception as e:
            print(f"Error connecting to PostgreSQL: {e}")
            return False
    
    def execute_query(self, query: str, params: Optional[tuple] = None) -> Optional[list]:
        """
        Выполняет SQL-запрос и возвращает результат
        
        Args:
            query: SQL-запрос для выполнения
            params: Параметры для запроса
            
        Returns:
            Список результатов или None в случае ошибки
        """
        if not self.connection:
            print("No connection established. Call connect() first.")
            return None
        
        try:
            with self.connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
                return [dict(row) for row in result]
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
    
    def execute_command(self, command: str, params: Optional[tuple] = None, returning_id: bool = False) -> Union[bool, Optional[int]]:
        """
        Выполняет команду (INSERT, UPDATE, DELETE)
        
        Args:
            command: SQL-команда для выполнения
            params: Параметры для команды
            returning_id: Если True, возвращает ID вставленной записи для INSERT команд
            
        Returns:
            bool: True если команда выполнена успешно, иначе False (для UPDATE/DELETE)
            int or None: ID вставленной записи для INSERT команд, если returning_id=True
        """
        if not self.connection:
            print("No connection established. Call connect() first.")
            return False
        
        try:
            with self.connection.cursor() as cursor:
                if returning_id and command.strip().upper().startswith('INSERT') and 'RETURNING' not in command.upper():
                    # Модифицируем команду, чтобы она возвращала ID
                    command += " RETURNING id"
                
                cursor.execute(command, params)
                
                # Если запрошено возвращение ID и это INSERT команда
                if returning_id and command.strip().upper().startswith('INSERT'):
                    result = cursor.fetchone()
                    inserted_id = result[0] if result else None
                    self.connection.commit()
                    return inserted_id
                else:
                    self.connection.commit()
                    return True
        except Exception as e:
            print(f"Error executing command: {e}")
            self.connection.rollback()
            return False
    
    def close(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            self.connection.close()
            print("PostgreSQL connection closed")

