import os
import subprocess
import sys
import time

def wait_for_db():
    """Ждет, пока база данных не станет доступной."""
    print("Ожидание запуска PostgreSQL...")
    while True:
        try:
            # Простая проверка подключения
            import psycopg2
            conn = psycopg2.connect(
                dbname=os.getenv("POSTGRES_DB", "pylearn_db"),
                user=os.getenv("POSTGRES_USER", "pylearn_user"),
                password=os.getenv("POSTGRES_PASSWORD", "pylearn_password"),
                host=os.getenv("DB_HOST", "localhost"), # В докере это имя сервиса
                port=os.getenv("DB_PORT", "5432")
            )
            conn.close()
            print("База данных доступна.")
            break
        except Exception as e:
            print(f"База данных недоступна, жду... Ошибка: {e}")
            time.sleep(2)

def run_alembic_migrations():
    """Выполняет миграции Alembic."""
    print("Запуск миграций Alembic...")
    try:
        # Устанавливаем переменную DATABASE_URL для Alembic
        database_url = f"postgresql://{os.getenv('POSTGRES_USER', 'pylearn_user')}:{os.getenv('POSTGRES_PASSWORD', 'pylearn_password')}@{os.getenv('DB_HOST', 'postgresql')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('POSTGRES_DB', 'pylearn_db')}"
        env = os.environ.copy()
        env["DATABASE_URL"] = database_url
        
        # Capture stdout and stderr to print on failure
        result = subprocess.run([
            "alembic", "upgrade", "head"
        ], env=env, cwd="/app", capture_output=True, text=True) # Added capture_output and text
        
        if result.returncode != 0:
            print(f"Alembic failed with stderr:\n{result.stderr}")
            raise RuntimeError(f"Alembic exited with code {result.returncode}")
        print("Миграции успешно применены.")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении миграций: {e}")
        sys.exit(1)


if __name__ == "__main__":
    wait_for_db()
    run_alembic_migrations()