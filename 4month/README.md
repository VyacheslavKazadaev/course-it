### 📅 Месяц 4: Docker + DevOps основы

**Формат:** 4 недели × 5 дней (Пн–Пт). Каждый день: теория → терминал → интерактив в браузере → задание/проверка.
**Пререквизиты:** Установленный Git, базовое понимание Linux, аккаунты GitHub/Docker Hub (бесплатно).
**⚠️ Важно:** Docker не работает чисто в браузере без бэкенда. Все «интерактивные задания в браузере» построены на бесплатных облачных песочницах, веб-интерфейсах PaaS и CI/CD. Для локальной работы рекомендуем Docker Desktop или WSL2 (Windows) / Docker Engine (Linux).

---

## 🟦 НЕДЕЛЯ 1: Docker Core (Images, Containers, Volumes, Networks)

### 📅 День 1: Что такое Docker? Образы и контейнеры

📖 **Теория:** Виртуализация vs контейнеризация. Архитектура Docker (daemon, CLI, registry). Образ = шаблон, контейнер = запущенный экземпляр.
💻 **Терминал:**

```bash
docker version
docker run hello-world
docker run -d -p 8080:80 --name mynginx nginx:alpine
docker ps
docker logs mynginx
docker stop mynginx && docker rm mynginx
```

🌐 **Интерактив в браузере:**

1. Откройте [labs.play-with-docker.com](https://labs.play-with-docker.com)
2. Нажмите `Add New Instance` → откроется терминал в браузере.
3. Выполните команды выше, затем нажмите `Open Port` → `8080`. Убедитесь, что в новой вкладке загрузилась страница Nginx.
   📝 **Задание:** Запустите 2 контейнера с разными версиями `nginx` (`nginx:1.24`, `nginx:alpine`). Сделайте скриншот `docker ps` с обеими записями.
   💡 **Совет преподавателя:** `docker run -d` запускает в фоне. `-p host:container` пробрасывает порты. Без `-d` контейнер умрёт вместе с терминалом.

---

### 📅 День 2: Dockerfile → кастомный образ

📖 **Теория:** Слои образа, кэширование сборки, инструкции `FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, `EXPOSE`.
💻 **Терминал:**

```bash
mkdir myapp && cd myapp
echo "print('Hello Docker')" > app.py
cat > Dockerfile <<EOF
FROM python:3.11-slim
WORKDIR /app
COPY app.py .
CMD ["python", "app.py"]
EOF
docker build -t mypython:v1 .
docker run --rm mypython:v1
```

🌐 **Интерактив в браузере:**

1. Откройте [GitHub Codespaces](https://github.com/features/codespaces) → `New codespace` на любом репозитории.
2. В терминале VS Code в браузере выполните сборку.
3. В панели `PORTS` добавьте `8000`, откройте в браузере (можно временно заменить `CMD` на `python -m http.server 8000`).
   📝 **Задание:** Измените `Dockerfile`: добавьте `RUN pip install flask`, создайте `app.py` с Flask-сервером на порту 5000. Соберите, запустите, откройте в браузере Codespaces.
   💡 **Совет:** Каждый `RUN` = новый слой. Группируйте команды: `RUN apt-get update && apt-get install -y ... && rm -rf /var/lib/apt/lists/*`.

---

### 📅 День 3: Volumes → сохранение данных

📖 **Теория:** Эфемерная файловая система контейнера. Bind mounts vs named volumes. Жизненный цикл данных.
💻 **Терминал:**

```bash
docker volume create pgdata
docker run -d --name postgres -e POSTGRES_PASSWORD=dev -v pg/var/lib/postgresql/data postgres:15
docker exec -it postgres psql -U postgres -c "CREATE TABLE demo(id int);"
docker stop postgres && docker rm postgres
docker run -d --name postgres2 -e POSTGRES_PASSWORD=dev -v pg/var/lib/postgresql/data postgres:15
docker exec -it postgres2 psql -U postgres -c "\dt"
```

🌐 **Интерактив в браузере:**

1. [Play with Docker](https://labs.play-with-docker.com) → создайте инстанс.
2. Выполните команды выше. После перезапуска контейнера убедитесь через `psql`, что таблица `demo` сохранилась.
   📝 **Задание:** Создайте bind mount `-v $(pwd)//data`, запишите файл из хоста, прочитайте из контейнера. Объясните в 3 предложениях, когда использовать volumes, а когда bind mounts.
   💡 **Совет:** Никогда не храните секреты или код в volumes для продакшена. Volumes управляются Docker, bind mounts зависят от ОС.

---

### 📅 День 4: Docker Networks → связь контейнеров

📖 **Теория:** Сети `bridge` (по умолчанию), `host`, `none`. DNS-разрешение по имени контейнера.
💻 **Терминал:**

```bash
docker network create mynet
docker run -d --name app --network mynet alpine sleep 3600
docker run -d --name db --network mynet postgres:15-alpine -e POSTGRES_PASSWORD=pass
docker exec app ping -c 2 db
```

🌐 **Интерактив в браузере:**

1. Play with Docker → 2 инстанса.
2. На первом: `docker run -d --name web --network host nginx:alpine`
3. На втором: `curl http://<IP_первого_инстанса>` (IP виден в шапке сессии).
4. Переключитесь на кастомную сеть, повторите `curl` по имени.
   📝 **Задание:** Запустите `redis` и `python:alpine` в одной сети. Из Python выполните `import redis; r = redis.Redis(host="redis")` и убедитесь, что соединение проходит.
   💡 **Совет:** `host` network убирает изоляцию. Используйте только для отладки или высокой производительности.

---

### 📅 День 5: Итог недели → мини-проект

📖 **Теория:** Повторение: lifecycle контейнера, слои, volumes, сети.🌐 **Интерактив:** [GitHub Codespaces](https://github.com/codespaces) + Docker.📝 **Задание:**

1. Напишите `Dockerfile` для Node.js/Python приложения.
2. Добавьте `volume` для логов.
3. Создайте сеть, запустите 2 контейнера, свяжите их.
4. Сделайте `docker inspect` и сохраните JSON в репозиторий.
   ✅ **Чек-лист недели:**

- [ ] Собрал кастомный образ без предупреждений
- [ ] Данные пережили `docker rm`
- [ ] Контейнеры пингуются по имени в кастомной сети
- [ ] `docker system prune` очистил мусор

---

## 🟨 НЕДЕЛЯ 2: Docker Compose для многоконтейнерных приложений

### 📅 День 6: Введение в Docker Compose

📖 **Теория:** `docker-compose.yml` (v3+/Compose Spec), сервисы, зависимости, порты, переменные окружения.
💻 **Терминал:**

```bash
mkdir compose-app && cd compose-app
cat > docker-compose.yml <<EOF
version: "3.8"
services:
  web:
    image: nginx:alpine
    ports: ["8080:80"]
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes: ["pg/var/lib/postgresql/data"]
volumes:
  pgdata:
EOF
docker compose up -d
docker compose ps
docker compose logs -f db
```

🌐 **Интерактив в браузере:**

1. Откройте [Railway](https://railway.app) → `New Project` → `Deploy from GitHub`.
2. Запушьте `docker-compose.yml` в репозиторий. Railway автоматически распознает сервисы и запустит их.
   📝 **Задание:** Добавьте `redis` сервис, пробросьте порт `6379`. Убедитесь через `docker compose exec web redis-cli -h redis ping`.
   💡 **Совет:** `docker compose` (v2) — встроен в Docker Desktop. Старый `docker-compose` (Python) устарел.

---

### 📅 День 7: Healthchecks, depends_on, масштабирование

📖 **Теория:** Проверка готовности сервиса, порядок запуска, `deploy: replicas`.
💻 **Терминал:** Добавьте в `docker-compose.yml`:

```yaml
  db:
    image: postgres:15
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
  web:
    depends_on:
      db:
        condition: service_healthy
```

🌐 **Интерактив в браузере:**

1. [Play with Docker] → запустите compose.
2. В браузере откройте `http://<IP>:8080`.
3. Сделайте `docker compose up --scale web=3`. Посмотрите `docker compose ps`.
   📝 **Задание:** Настройте `depends_on` так, чтобы `web` стартовал только после готовности `db`. Сломать healthcheck намеренно, проверить, что `web` не стартует.
   💡 **Совет:** `depends_on` не ждёт готовности БД без `condition`. Всегда используйте healthcheck для production.

---

### 📅 День 8: Реальный стек (App + DB + Cache)

📖 **Теория:** Типичные стеки: Python/Flask + PostgreSQL + Redis, или Node + Mongo.
💻 **Терминал:** Создайте `app.py` (Flask), подключите `psycopg2` и `redis`. В compose добавьте:

```yaml
  app:
    build: .
    ports: ["5000:5000"]
    environment:
      DATABASE_URL: postgresql://postgres:secret@db:5432/app
      REDIS_URL: redis://redis:6379/0
    depends_on:
      db: {condition: service_healthy}
      redis: {condition: service_started}
```

🌐 **Интерактив в браузере:**

1. GitHub Codespaces → `docker compose up`.
2. В панели `PORTS` откройте `5000`. Проверьте ответ API.
   📝 **Задание:** Добавьте `pgAdmin` или `redis-commander` в compose для визуального мониторинга.
   💡 **Совет:** Не храните пароли в `docker-compose.yml`. Используйте `.env` и `env_file`.

---

### 📅 День 9: Безопасность и оптимизация образов

📖 **Теория:** Non-root users, `--read-only`, multi-stage builds, сканирование уязвимостей.
💻 **Терминал:**

```Dockerfile
FROM python:3.11-slim AS builder
RUN pip install --user flask
FROM python:3.11-slim
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
RUN useradd -m appuser && chown -R appuser /app
USER appuser
CMD ["python", "app.py"]
```

🌐 **Интерактив в браузере:**

1. [Docker Hub](https://hub.docker.com) → загрузите образ. Вкладка `Security` покажет сканирование (бесплатно до 3 приватных).
2. Альтернатива: `docker scout cves <image>` (если установлен).
   📝 **Задание:** Уменьшите размер образа на 60%+. Запустите контейнер с `--read-only --tmpfs /tmp`.
   💡 **Совет:** `docker system df` покажет, сколько места занимают образы/volumes. `docker builder prune` очистит кэш сборки.

---

### 📅 День 10: Итог недели → Production-ready Compose

🌐 **Интерактив:** [Render](https://render.com) → `New Blueprint` → подключите GitHub репозиторий с `docker-compose.yml`. Render автоматически развернёт сервисы.📝 **Задание:**

1. Добавьте `.env` с секретами.
2. Настройте `restart: unless-stopped`.
3. Добавьте `healthcheck` для всех сервисов.
4. Задеплойте в Render/Railway, откройте URL в браузере.
   ✅ **Чек-лист недели:**

- [ ] Compose запускается одной командой
- [ ] Сервисы ждут готовности зависимостей
- [ ] Образ < 200 МБ, работает без root
- [ ] Успешный деплой в PaaS

---

## 🟧 НЕДЕЛЯ 3: Базовые CI/CD пайплайны

### 📅 День 11: GitHub Actions → первый workflow

📖 **Теория:** YAML-синтаксис, jobs, steps, runners, триггеры.🌐 **Интерактив в браузере:**

1. GitHub → ваш репозиторий → вкладка `Actions`.
2. `Set up a workflow yourself` → вставьте:

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: {python-version: '3.11'}
      - run: pip install pytest
      - run: pytest || true
```

📝 **Задание:** Создайте `test_app.py` с фейковым тестом. Запушьте. В браузере откройте `Actions` → кликните на запуск → посмотрите логи.
💡 **Совет:** `|| true` нужен, чтобы пайплайн не падал на ранних этапах обучения. Уберите в продакшене.

---

### 📅 День 12: Сборка и публикация Docker-образа в CI

📖 **Теория:** Кэширование слоёв, логин в registry, push/pull.🌐 **Интерактив в браузере:**

1. GitHub → `Settings` → `Secrets and variables` → `Actions` → добавьте `DOCKER_USERNAME`, `DOCKER_PASSWORD`.
2. Добавьте job:

```yaml
  build-push:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/setup-buildx-action@v3
      - uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      - uses: docker/build-push-action@v5
        with:
          push: true
          tags: ${{ secrets.DOCKER_USERNAME }}/myapp:latest
```

📝 **Задание:** Запушьте. Откройте [Docker Hub](https://hub.docker.com) в браузере → убедитесь, что образ появился.
💡 **Совет:** Используйте `docker/metadata-action` для тегов `v1.0.0`, `sha-abc123`.

---

### 📅 День 13: GitLab CI/CD

📖 **Теория:** `.gitlab-ci.yml`, stages, runners, variables.🌐 **Интерактив в браузере:**

1. [GitLab.com](https://gitlab.com) → `New project` → `Import` из GitHub.
2. Создайте `.gitlab-ci.yml`:

```yaml
stages: [test, build]
test:
  stage: test
  image: python:3.11
  script: [pip install pytest, pytest]
build:
  stage: build
  image: docker:latest
  services: [docker:dind]
  script: [docker build -t myapp .]
```

3. Откройте вкладку `CI/CD` → `Pipelines`.
   📝 **Задание:** Добавьте кэширование `pip`. Запустите пайплайн вручную (`Run pipeline`).
   💡 **Совет:** GitLab shared runners бесплатны, но имеют лимиты. Для Docker-in-Docker нужен `docker:dind`.

---

### 📅 День 14: Тесты, артефакты,覆盖率

📖 **Теория:** Сохранение логов, coverage, fail-fast, code quality gates.🌐 **Интерактив в браузере:**

1. GitHub Actions → добавьте:

```yaml
      - run: pip install pytest-cov
      - run: pytest --cov=. --cov-report=xml
      - uses: codecov/codecov-action@v4
        with: {token: ${{ secrets.CODECOV_TOKEN }} }
```

2. Откройте [Codecov.io](https://codecov.io) → подключите репозиторий → увидите графики покрытия.
   📝 **Задание:** Настройте `fail: true` если coverage < 70%. Добавьте linting (`flake8` или `ruff`).
   💡 **Совет:** Не храните токены в коде. Используйте `secrets` или `OIDC`.

---

### 📅 День 15: Итог недели → полный пайплайн

🌐 **Интерактив:** GitHub Actions UI + Docker Hub + Codecov.📝 **Задание:** Соберите пайплайн: `lint → test → build Docker → push → notify (email/discord webhook)`.✅ **Чек-лист недели:**

- [ ] Пайплайн запускается на push/PR
- [ ] Образ собирается и публикуется автоматически
- [ ] Тесты и coverage отображаются в вебе
- [ ] Секреты не попадают в логи

---

## 🟥 НЕДЕЛЯ 4: Деплой в облако + интеграция

### 📅 День 16: PaaS → Render & Railway

📖 **Теория:** Zero-config деплой, managed DB, auto-scaling, custom domains.🌐 **Интерактив в браузере:**

1. [Render](https://render.com) → `New Web Service` → подключите GitHub → выберите `Docker`.
2. Укажите порт, добавьте переменные окружения. Нажмите `Create`.
3. В браузере откройте предоставленный URL.
   📝 **Задание:** Настройте автоматический деплой при push в `main`. Добавьте healthcheck endpoint `/health`.
   💡 **Совет:** Free tier Render засыпает после 15 мин простоя. Railway не засыпает, но имеет лимит часов.

---

### 📅 День 17: Деплой многоконтейнерных приложений

📖 **Теория:** Как PaaS обрабатывает compose. Managed PostgreSQL/Redis.🌐 **Интерактив в браузере:**

1. [Railway](https://railway.app) → `New Project` → `Deploy from GitHub`.
2. Railway автоматически парсит `docker-compose.yml`.
3. В dashboard кликните на `Postgres` → скопируйте `DATABASE_URL`. Вставьте в сервис `app`.
4. Откройте URL приложения.
   📝 **Задание:** Добавьте `redis` сервис. Убедитесь, что `app` подключается к managed Redis Railway.
   💡 **Совет:** PaaS заменяют `volumes` на managed storage. Не используйте bind mounts в облаке.

---

### 📅 День 18: AWS Free Tier → EC2 + Docker

📖 **Теория:** IaaS vs PaaS, security groups, SSH, systemd, auto-start.🌐 **Интерактив в браузере:**

1. [AWS Console](https://console.aws.amazon.com) → `EC2` → `Launch Instance` → `Amazon Linux 2023` (t3.micro, free tier).
2. Скачайте `.pem`, подключитесь через `ssh -i key.pem ec2-user@IP`.
3. Выполните:

```bash
sudo dnf update -y
sudo dnf install -y docker
sudo systemctl enable --now docker
sudo usermod -aG docker $USER
# logout/login
docker run -d -p 80:80 nginx:alpine
```

4. В браузере: `http://<EC2_Public_IP>`.
   📝 **Задание:** Напишите `systemd` сервис для автозапуска контейнера. Настройте security group: open 80, 443, 22.
   💡 **Совет:** Free tier = 750 часов/мес. Не запускайте больше 1 инстанса одновременно. Удаляйте ресурсы после практики.

---

### 📅 День 19: CI/CD → Облако (GitOps основы)

📖 **Теория:** Webhooks, deploy triggers, rollback, инфраструктура как код (базово).🌐 **Интерактив в браузере:**

1. В GitHub Actions добавьте step:

```yaml
      - name: Deploy to Render
        run: |
          curl -X POST "https://api.render.com/v1/services/<SERVICE_ID>/deploys" \
          -H "Authorization: Bearer ${{ secrets.RENDER_API_KEY }}" \
          -H "Content-Type: application/json" \
          -d '{"clearCache": "clear"}'
```

2. Откройте Render dashboard → вкладка `Deploys` → увидите запуск.
   📝 **Задание:** Настройте деплой только на `main`. Добавьте manual approval step.
   💡 **Совет:** Для AWS используйте `aws ecs update-service` или `eb deploy`. В CI/CD всегда логируйте `git sha`.

---

### 📅 День 20: Финальный проект месяца

🌐 **Интерактив:** Браузер + терминал + облако.📝 **Задание:**

1. Репозиторий с приложением (Flask/Node).
2. `Dockerfile` + `docker-compose.yml` (app + db + cache).
3. GitHub Actions: lint → test → build → push → deploy to Render/Railway.
4. Healthcheck, logs, custom domain (или subdomain).
5. Скриншоты: CI pipeline, cloud dashboard, working URL.
   ✅ **Итоговый чек-лист месяца:**

- [ ] Контейнеризация с volumes/networks
- [ ] Compose с healthchecks и секретами
- [ ] CI/CD с тестами, сборкой, публикацией
- [ ] Деплой в PaaS + базовый AWS EC2
- [ ] Автоматизация деплоя из CI
- [ ] Проект доступен по URL в браузере

---

## 🎓 Рекомендации преподавателя

1. **Безопасность:** Никогда не коммитьте `.env`, ключи, `.pem`. Используйте `gitignore`, CI secrets, AWS IAM.
2. **Отладка:** `docker compose logs -f`, `docker exec -it <container> sh`, `curl -v http://localhost`, `docker system prune -a`.
3. **Следующий месяц:** Kubernetes basics, Helm, Terraform (IaC), мониторинг (Prometheus/Grafana), продвинутый CI/CD (ArgoCD, GitOps).
4. **Ресурсы:**
   - [Docker Docs](https://docs.docker.com)
   - [GitHub Actions Docs](https://docs.github.com/actions)
   - [Render/Railway Docs](https://render.com/docs)
   - [AWS Free Tier FAQ](https://aws.amazon.com/free)

Готов адаптировать темп, добавить разбор типичных ошибок, или предоставить шаблон репозитория с `docker-compose.yml`, CI/CD и `README.md` для быстрого старта.
