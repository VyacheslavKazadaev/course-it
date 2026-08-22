import os
import time
import pytest
import httpx2

# --- Фикстура для клиента API, обращающегося к реальному серверу ---
@pytest.fixture
def real_api_client():
    """
    Фикстура, предоставляющая HTTP-клиент httpx2 и базовый URL API для тестирования реального запущенного сервера.
    Убедитесь, что сервер запущен перед запуском этих тестов.
    """
    base_url = os.environ.get("API_BASE_URL", "http://localhost:8000")
    if not base_url.endswith('/'):
        base_url += '/'

    # Проверим, доступен ли сервер перед созданием клиента
    max_retries = 10
    retries = 0
    ready = False
    while retries < max_retries and not ready:
        try:
            # Попробуем получить список пользователей как сигнал готовности
            response = httpx2.get(url=f"{base_url.rstrip('/')}/users", timeout=5.0)
            if response.status_code in [200, 404]:  # 200 OK или 404 (но не ConnectionError) значит сервер жив
                print(f"Сервер доступен по адресу {base_url}, статус проверочного запроса: {response.status_code}")
                ready = True
            else:
                print(f"Сервер вернул неожиданный статус {response.status_code} при проверке, ждем...")
        except httpx2.ConnectError:
            print(f"Не удается подключиться к серверу {base_url}, попытка {retries + 1}/{max_retries}. Ждем...")
        except Exception as e:
            print(f"Произошла ошибка при проверке сервера: {e}, ждем...")
        
        if not ready:
            time.sleep(2)  # Ждем 2 секунды перед повторной попыткой
            retries += 1

    if not ready:
        raise RuntimeError(f"Сервер не стал доступным по адресу {base_url} за отведенное время.")

    client = httpx2.Client(base_url=base_url, timeout=10.0)
    yield client
    client.close()


# --- E2E Тесты для реального API ---
class TestE2ERealServerUserAPI:
    def test_e2e_create_and_get_user(self, real_api_client):
        """E2E тест: создание пользователя и его последующее получение от реального API."""
        base_url = str(real_api_client.base_url)

        # Шаг 1: Получить список пользователей до создания нового
        response_before = real_api_client.get("/users")
        assert response_before.status_code == 200
        users_before = response_before.json()
        initial_count = len(users_before)

        # Шаг 2: Создать нового пользователя
        new_user_data = {
            "username": "real_server_test_user",
            "email": "real_server_test@example.com"
        }
        response_create = real_api_client.post("/users/", json=new_user_data)
        assert response_create.status_code == 200
        created_user = response_create.json()
        assert created_user["username"] == new_user_data["username"]
        assert created_user["email"] == new_user_data["email"]
        user_id = created_user["id"]

        # Шаг 3: Получить список пользователей после создания
        response_after = real_api_client.get("/users")
        assert response_after.status_code == 200
        users_after = response_after.json()
        assert len(users_after) == initial_count + 1

        # Шаг 4: Получить конкретного созданного пользователя по ID
        response_get_single = real_api_client.get(f"/users/{user_id}")
        assert response_get_single.status_code == 200
        fetched_user = response_get_single.json()
        assert fetched_user["id"] == user_id
        assert fetched_user["username"] == new_user_data["username"]
        assert fetched_user["email"] == new_user_data["email"]

    def test_e2e_delete_user(self, real_api_client):
        """E2E тест: создание и удаление пользователя через реальный API."""
        # Шаг 1: Создать пользователя для теста удаления
        new_user_data = {
            "username": "real_server_test_user_to_delete",
            "email": "real_server_delete_test@example.com"
        }
        response_create = real_api_client.post("/users/", json=new_user_data)
        assert response_create.status_code == 200
        created_user = response_create.json()
        user_id = created_user["id"]
        assert created_user["username"] == new_user_data["username"]

        # Шаг 2: Удалить пользователя
        response_delete = real_api_client.delete(f"/users/{user_id}")
        assert response_delete.status_code == 200
        delete_response = response_delete.json()
        assert delete_response["success"] is True

        # Шаг 3: Проверить, что пользователь больше не существует
        response_get_deleted = real_api_client.get(f"/users/{user_id}")
        assert response_get_deleted.status_code in [404, 200] # Сервер может вернуть 404 или пустой объект
        if response_get_deleted.status_code == 200:
             assert response_get_deleted.json() == {}
        elif response_get_deleted.status_code == 404:
            pass # Успешно удален

    def test_e2e_get_users_list(self, real_api_client):
        """E2E тест: получение списка пользователей от реального API."""
        response = real_api_client.get("/users")
        assert response.status_code == 200
        users = response.json()
        assert isinstance(users, list)

    def test_e2e_validation_error(self, real_api_client):
        """E2E тест: проверка валидации на некорректный ID пользователя через реальный API."""
        # Отправляем отрицательный ID, который должен провалидироваться
        response = real_api_client.get("/users/-1")
        assert response.status_code == 422 # Unprocessable Entity для валидации Pydantic