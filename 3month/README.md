### 🛠 **Рекомендуемый стек для браузерной работы:**

- Python/FastAPI: [Replit](https://replit.com) (создайте шаблон `Python` или `FastAPI`)
- PostgreSQL: [Neon.tech](https://neon.tech) или [Supabase](https://supabase.com) (бесплатный облачный PostgreSQL) + [DB Fiddle](https://www.db-fiddle.com) для чистого SQL
- Тестирование API: [Postman Web](https://web.postman.co) или [Hoppscotch](https://hoppscotch.io)
- Документация: автосгенерируется FastAPI (`/docs`)

---

## 📅 НЕДЕЛЯ 1: PostgreSQL Core + Python ↔ БД

### День 1: DDL. Создание таблиц, типы данных, Primary Key

🎯 Научиться проектировать и создавать таблицы в SQL.📚 **Теория:**

- `CREATE TABLE`, типы: `SERIAL/INTEGER`, `VARCHAR`, `TEXT`, `TIMESTAMP`, `BOOLEAN`
- `PRIMARY KEY`, `NOT NULL`, `DEFAULT`
- Схема БД: логическая vs физическая

💻 **Задание в браузере:**

1. Откройте [DB Fiddle](https://www.db-fiddle.com) → выберите PostgreSQL 15.
2. Вставьте в окно `Schema`:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

3. Нажмите `Run`. Проверьте вкладку `Result`.

✅ **Самопроверка:**

- Если ошибка `duplicate key` → вы запускали дважды. `DROP TABLE users;` перед запуском.
- Вопрос: зачем `SERIAL`? (Ответ: автоматическая генерация уникального ID)

📝 **ДЗ:** Создайте таблицу `posts` с полями: `id`, `user_id` (INT), `title`, `content`, `is_published`.

---

### День 2: DML. INSERT, SELECT, WHERE, ORDER BY

🎯 Вставлять и извлекать данные, фильтровать и сортировать.📚 **Теория:**

- `INSERT INTO ... VALUES (...)`
- `SELECT * FROM ... WHERE ... ORDER BY ... LIMIT ...`
- Операторы: `=`, `<>`, `LIKE`, `IN`, `BETWEEN`, `AND/OR`

💻 **Задание:**

1. В том же DB Fiddle добавьте в `Query`:

```sql
INSERT INTO users (username, email) VALUES 
('alice', 'alice@mail.com'),
('bob', 'bob@mail.com'),
('charlie', 'charlie@mail.com');

SELECT * FROM users WHERE email LIKE '%mail.com' ORDER BY username ASC LIMIT 2;
```

2. Запустите. Ожидается 2 строки.

✅ **Самопроверка:**

- Измените `LIMIT 2` → `LIMIT 10`. Что изменилось?
- Напишите запрос, который вернет пользователей, у которых `username` начинается на `b`.

📝 **ДЗ:** Добавьте в `posts` 5 записей, отфильтруйте только опубликованные.

---

### День 3: UPDATE, DELETE, NULL, Агрегация

🎯 Обновлять/удалять данные, работать с `NULL`, считать статистику.📚 **Теория:**

- `UPDATE ... SET ... WHERE ...` (всегда `WHERE`!)
- `DELETE FROM ... WHERE ...`
- `IS NULL` / `IS NOT NULL`
- `COUNT()`, `SUM()`, `AVG()`, `GROUP BY`, `HAVING`

💻 **Задание:**

```sql
-- Обновление
UPDATE users SET email = 'newalice@mail.com' WHERE username = 'alice';

-- Удаление
DELETE FROM users WHERE username = 'charlie';

-- Агрегация
SELECT COUNT(*) as total, AVG(id) as avg_id FROM users;
```

✅ **Самопроверка:**

- Что будет без `WHERE` в `UPDATE`/`DELETE`? (Ответ: затронуты все строки → катастрофа)
- Чем `WHERE` отличается от `HAVING`?

📝 **ДЗ:** Напишите запрос, который считает количество пользователей, у которых `email` содержит `mail`.

---

### День 4: Python ↔ PostgreSQL (psycopg2)

🎯 Выполнять SQL-запросы из Python.📚 **Теория:**

- `psycopg2` (синхронный) vs `asyncpg` (асинхронный)
- Подключение, курсоры, параметризация (`%s` или `$1`)
- Защита от SQL-инъекций

💻 **Задание в Replit:**

1. Создайте Repl → `Python`.
2. В терминале: `pip install psycopg2-binary`
3. В `main.py`:

```python
import psycopg2

# Замените на свои данные из Neon/Supabase
conn = psycopg2.connect(
    dbname="your_db", user="your_user", password="your_pass",
    host="your_host", port=5432
)
cur = conn.cursor()
cur.execute("SELECT username FROM users LIMIT 3;")
print(cur.fetchall())
cur.close(); conn.close()
```

✅ **Самопроверка:** Выводится список кортежей `[('alice',), ('bob',)]`.
⚠️ Никогда не подставляйте данные через f-строки в SQL!

📝 **ДЗ:** Напишите скрипт, который принимает `username` и `email` из `input()` и безопасно вставляет в таблицу.

---

### День 5: Практикум. Проектирование схемы БД

🎯 Спроектировать и реализовать схему для мини-блога.
📚 **Теория:** Нормализация, связи, выбор типов, индексы (база).

💻 **Задание:**
В DB Fiddle или локально создайте:

- `users` (id, username, email, created_at)
- `posts` (id, user_id, title, content, published_at)
- `comments` (id, post_id, user_id, text, created_at)
  Вставьте по 3 пользователя, 5 постов, 10 комментариев. Напишите 3 запроса:

1. Все посты конкретного пользователя
2. Посты с количеством комментариев
3. Последние 3 комментария к посту

✅ **Самопроверка:** Запросы возвращают ожидаемые данные без дублей/ошибок типов.

📝 **ДЗ:** Добавьте поле `is_deleted` (boolean) в `posts` и напишите запрос только на активные посты.

---

## 📅 НЕДЕЛЯ 2: PostgreSQL Advanced + REST & FastAPI Base

### День 6: Связи и JOINs

🎯 Объединять таблицы, понимать FOREIGN KEY.
📚 `INNER JOIN`, `LEFT JOIN`, `ON`, `USING`, `1:N`, `M:N` (через таблицу-связку).

💻 **Задание:**

```sql
SELECT u.username, p.title, COUNT(c.id) as comment_count
FROM users u
JOIN posts p ON u.id = p.user_id
LEFT JOIN comments c ON p.id = c.post_id
GROUP BY u.username, p.title
ORDER BY comment_count DESC;
```

✅ **Вопрос:** Почему `LEFT JOIN` для комментариев? (Ответ: чтобы посты без комментариев тоже попали в результат с `0`)

📝 **ДЗ:** Напишите запрос для вывода пользователей, у которых нет постов.

---

### День 7: Индексы и EXPLAIN

🎯 Ускорять запросы, понимать планы выполнения.
📚 `CREATE INDEX`, B-Tree, `UNIQUE`, составные индексы. `EXPLAIN ANALYZE`.

💻 **Задание:**

1. Выполните `EXPLAIN ANALYZE SELECT * FROM posts WHERE title ILIKE '%fast%';`
2. Создайте индекс: `CREATE INDEX idx_posts_title ON posts USING gin(title gin_trgm_ops);` (или обычный B-tree `CREATE INDEX idx_posts_title ON posts(title);`)
3. Сравните `Seq Scan` vs `Index Scan`.

✅ **Правило:** Индексы ускоряют `SELECT`, замедляют `INSERT/UPDATE`. Создавайте только под реальные `WHERE/JOIN/ORDER BY`.

📝 **ДЗ:** Создайте составной индекс `(user_id, published_at)` и объясните, когда он полезен.

---

### День 8: Транзакции и ACID

🎯 Гарантировать целостность данных.
📚 `BEGIN`, `COMMIT`, `ROLLBACK`. Изоляция, блокировки.

💻 **Задание (psycopg2):**

```python
conn.autocommit = False
try:
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET balance = balance - 100 WHERE id = 1;")
    cur.execute("UPDATE accounts SET balance = balance + 100 WHERE id = 2;")
    conn.commit()
except Exception as e:
    conn.rollback()
    print("Откат:", e)
```

✅ **Самопроверка:** При ошибке во втором запросе баланс не меняется.

📝 **ДЗ:** Напишите транзакцию, которая создает пользователя и его первый пост одновременно.

---

### День 9: REST API. Принципы и HTTP

🎯 Понимать архитектуру REST, методы, статус-коды.
📚 `GET`, `POST`, `PUT`, `PATCH`, `DELETE`. Коды: `200`, `201`, `400`, `401`, `404`, `500`. JSON, stateless.

💻 **Задание:** Откройте [Hoppscotch](https://hoppscotch.io). Сделайте запросы к `https://jsonplaceholder.typicode.com/posts`:

- `GET /posts` → 200
- `POST /posts` с телом `{"title":"test","body":"text","userId":1}` → 201
- `GET /posts/1` → 200

✅ **Чек-лист:** Знаете разницу `PUT` (полное обновление) vs `PATCH` (частичное)?

📝 **ДЗ:** Напишите 5 примеров эндпоинтов для API блога с методом и ожидаемым кодом.

---

### День 10: FastAPI. Первый сервер

🎯 Запустить асинхронный сервер, создать маршруты, автодокументацию.
📚 Декораторы `@app.get()`, `@app.post()`, `async def`, Pydantic, `/docs`.

💻 **Задание в Replit (шаблон FastAPI):**

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.get("/")
def root():
    return {"message": "Hello FastAPI"}

@app.post("/items/")
def create_item(item: Item):
    return {"item": item, "status": "created"}
```

Запустите → откройте `/docs`. Протестируйте через UI.

✅ **Самопроверка:** Swagger открываетcя, POST принимает JSON, валидирует типы.

📝 **ДЗ:** Добавьте `GET /items/{item_id}` с валидацией `item_id > 0`.

---

## 📅 НЕДЕЛЯ 3: Полноценная REST API разработка

### День 11: CRUD + Репозиторий

🎯 Реализовать полный цикл работы с данными.
📚 Path/Query параметры, разделение маршрутов и логики.

💻 **Задание:** Создайте `db.py` (подключение к БД), `models.py` (Pydantic), `main.py`. Реализуйте:

- `POST /users` → INSERT
- `GET /users` → SELECT
- `GET /users/{id}` → SELECT WHERE
- `PUT /users/{id}` → UPDATE
- `DELETE /users/{id}` → DELETE

✅ **Паттерн:** Выносите SQL в отдельный модуль `repositories.py`. API слой только принимает/возвращает JSON.

📝 **ДЗ:** Добавьте пагинацию `?skip=0&limit=10`.

---

### День 12: Валидация и Обработка ошибок

🎯 Возвращать понятные ошибки, не ломать сервер.
📚 `HTTPException`, `try/except`, Pydantic `Field`, кастомные валидаторы.

💻 **Задание:**

```python
from fastapi import HTTPException
@app.get("/users/{user_id}")
def get_user(user_id: int):
    user = db_get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

✅ **Проверка:** При запросе несуществующего ID возвращается JSON `{"detail": "User not found"}` и статус 404.

📝 **ДЗ:** Добавьте валидацию: email должен содержать `@`, username 3-30 символов.

---

### День 13: SQLAlchemy ORM + FastAPI

🎯 Работать с БД через ORM, а не сырой SQL.
📚 Declarative Base, Sessions, `asyncpg` + `SQLAlchemy 2.0`.

💻 **Задание:** Установите `sqlalchemy asyncpg`. Определите модель:

```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)
```

Настройте `AsyncSession`, создайте CRUD функции. Подключите к FastAPI через `Depends(get_db)`.

✅ **Самопроверка:** `pip install sqlalchemy[asyncio]`, запуск без блокировки event loop.

📝 **ДЗ:** Реализуйте `get_users` с `select(User).offset().limit()`.

---

### День 14: Фильтрация, Сортировка, Поиск

🎯 Делать API гибким.
📚 Query параметры, динамические `WHERE`, `ILIKE`, сортировка по полю.

💻 **Задание:** Реализуйте `GET /posts?search=fastapi&sort=-created_at&limit=5`

- `search` → `WHERE title ILIKE '%fastapi%'`
- `sort` → `ORDER BY created_at DESC` (минус в параметре = DESC)

✅ **Проверка:** Запросы комбинируются, не ломаются при отсутствии параметров.

📝 **ДЗ:** Добавьте фильтр по дате `?date_from=2024-01-01&date_to=2024-12-31`.

---

### День 15: Тестирование API + CI базовый

🎯 Писать автотесты, проверять контракты.
📚 `pytest`, `httpx`, `TestClient`, моки БД.

💻 **Задание:**

```python
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

def test_create_item():
    response = client.post("/items/", json={"name":"test", "price":10.0})
    assert response.status_code == 200
    assert response.json()["status"] == "created"
```

Запустите `pytest test_api.py -v`.

✅ **Чек-лист:** 80%+ покрытие основных маршрутов, проверка 400/404 кодов.

📝 **ДЗ:** Напишите тест для `GET /users/{id}` с несуществующим ID → ожидаем 404.

---

## 📅 НЕДЕЛЯ 4: AuthN/AuthZ, Безопасность, Финальный проект

### День 16: Хеширование паролей + JWT теория

🎯 Понимать AuthN vs AuthZ, хранить пароли безопасно.
📚 `bcrypt`/`passlib`, JWT структура (header.payload.signature), `exp`, `sub`.

💻 **Задание:**

```python
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed = pwd_context.hash("mysecretpassword")
print(pwd_context.verify("mysecretpassword", hashed)) # True
```

✅ **Вопрос:** Почему нельзя хранить пароли в plaintext? (Ответ: утечка → компромисс всех аккаунтов)

📝 **ДЗ:** Напишите функцию `create_access_token(data, expires_delta)`.

---

### День 17: Регистрация и Логин

🎯 Реализовать flow регистрации/авторизации.
📚 `POST /register`, `POST /login`, возврат JWT, валидация уникальности email.

💻 **Задание:** В FastAPI создайте эндпоинты:

- Проверка существования пользователя → 400
- Хеширование пароля → INSERT
- Логин: проверка пароля → генерация JWT → `{"access_token": "...", "token_type": "bearer"}`

✅ **Проверка:** Токен декодируется на [jwt.io](https://jwt.io) с вашим секретом.

📝 **ДЗ:** Добавьте `refresh_token` (опционально, для продвинутых).

---

### День 18: Защита эндпоинтов + Роли

🎯 Закрывать маршруты, проверять права.
📚 `OAuth2PasswordBearer`, `Depends`, декодирование токена, `User` в зависимости.

💻 **Задание:**

```python
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

@app.get("/users/me")
def read_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt(token)
    if not payload: raise HTTPException(401)
    return {"user_id": payload["sub"]}
```

✅ **Самопроверка:** Запрос без `Authorization: Bearer ...` → 401. С валидным → 200.

📝 **ДЗ:** Добавьте поле `role` в JWT и зависимость `require_admin()`.

---

### День 19: Безопасность API + CORS + Rate Limit

🎯 Защитить приложение от базовых атак.
📚 CORS, HTTPS, SQL-инъекции (ORM/параметризация), XSS, Rate Limiting.

💻 **Задание:**

```python
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
)
```

✅ **Чек-лист:**

- Все запросы к БД через ORM/параметры
- CORS ограничен
- Секреты в `.env`, не в коде
- Логирование ошибок без stack trace в продакшене

📝 **ДЗ:** Настройте `python-dotenv`, вынесите `SECRET_KEY`, `DATABASE_URL` в `.env`.

---

### День 20: Финальный мини-проект + Деплой

🎯 Собрать всё воедино, выложить в облако.
📚 Структура проекта, Docker (база), Render/Railway, мониторинг.

💻 **Задание:**

1. Репозиторий с папками: `app/`, `tests/`, `alembic/` (миграции), `.env.example`, `requirements.txt`
2. API: `/register`, `/login`, CRUD `/posts` с защитой JWT
3. Деплой: [Render.com](https://render.com) (Web Service) + [Neon](https://neon.tech) (PostgreSQL)
4. Проверьте `/docs` в продакшене, протестируйте Postman.

✅ **Критерии сдачи:**

- Работает регистрация/логин
- JWT защищает маршруты
- CRUD работает с БД
- Есть тесты (`pytest`)
- Развернут в облаке, доступна ссылка

📝 **Рекомендация:** Добавьте CI через GitHub Actions (запуск тестов при push).

---

## 📦 Материалы для преподавателя/студента

| День | Формат проверки                 | Ожидаемый артефакт       |
| -------- | --------------------------------------------- | ----------------------------------------- |
| 1-5      | SQL-файлы + скриншоты DB Fiddle | Схема БД, 5+ запросов      |
| 6-8      | Код репозитория                 | JOIN, EXPLAIN, транзакции       |
| 9-10     | Скриншот Swagger                      | Работающий FastAPI сервер |
| 11-15    | pytest отчет                             | CRUD, тесты, пагинация      |
| 16-20    | Deploy URL + Postman коллекция       | Auth, защита, деплой          |

## 🔧 Советы по обучению

1. **Не давайте готовые решения сразу.** Пусть студент сначала попробует, затем покажите эталон.
2. **Используйте "поломанные" примеры:** специально добавьте SQL-инъекцию или забытый `WHERE`, пусть найдут уязвимость.
3. **Фиксируйте прогресс:** каждый день → commit с тегом `day_X`.
4. **Переход к локальной среде:** на 3-й неделе рекомендую установить Docker + `docker-compose.yml` (PostgreSQL + pgAdmin), чтобы подготовить к продакшену.

Готов предоставить:

- Шаблоны `docker-compose.yml`
- GitHub Actions конфиг для тестов
- Чек-лист код-ревью для финального проекта
- Презентации/схемы (PlantUML/Mermaid) по архитектуре

Напишите, какой день или тему разобрать глубже, и я подготовлю детальный разбор с кодом, ошибками новичков и способами отладки.
