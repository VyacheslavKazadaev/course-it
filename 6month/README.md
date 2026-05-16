### ASSISTANT

# 📅 Месяц 6: Масштабирование + Микросервисы (Go 1.26)

> **Формат:** 4 недели × 5 дней. Каждый день содержит теорию, практические инструкции на Go 1.26, браузерные интерактивы и домашнее задание. Проекты накапливаются и финализируются к концу месяца.

---

## 🛠 Как запускать интерактивы в браузере

| Задача                   | Платформа/Инструмент              | Как открыть                                           |
| ------------------------------ | ---------------------------------------------------- | --------------------------------------------------------------- |
| Go 1.26 IDE + терминал | `gitpod.io` или `replit.com`                  | Импорт репозитория →`go run .`              |
| Swagger/OpenAPI UI             | `swagger.io/swagger-ui`                            | `/swagger/index.html` в локальном сервисе    |
| RabbitMQ Management            | `rabbitmq.com/management`                          | `http://localhost:15672` (Docker)                             |
| Kafka UI                       | `provectus/kafka-ui`                               | `http://localhost:8080` (Docker)                              |
| Prometheus + Grafana           | `prometheus.io` / `grafana.com`                  | `http://localhost:9090` / `http://localhost:3000`           |
| PromQL Sandbox                 | `play.prometheus.io`                               | Браузер, без установки                       |
| Test/CI симулятор     | `killercoda.com` / `github.com/actions/setup-go` | Интерактивные сценарии в браузере |

> 💡 **Совет преподавателя:** Все сервисы запускаются через `docker-compose.yml`. В Gitpod/Replit поддерживается Docker-in-Docker, поэтому браузерная среда полностью воспроизводит локальную.

---

## 🗓 НЕДЕЛЯ 1: Архитектура микросервисов

**Цель:** Спроектировать границы сервисов, настроить монорепозиторий Go 1.26, реализовать REST API с контрактной спецификацией.

| День       | Цель                                      | Теория                                                                                                         | Практика (Go 1.26)                                                                                                                        | Интерактивное задание (браузер)                                                                                                | ДЗ                                                                                               |
| -------------- | --------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Пн** | Монолит vs Микросервисы    | SRP, слабая связность, API-контракты, когда микросервисы*не нужны* | Анализ архитектуры существующего монолита. Разбивка на `catalog`, `cart`, `order`, `user` | 🌐[draw.io](https://app.diagrams.net) → нарисовать схему границ сервисов + экспортировать в `.png`            | Описать в `ARCHITECTURE.md` ответственность каждого сервиса |
| **Вт** | Структура Go-проекта          | `go work` (монорепозиторий), `cmd/`, `internal/`, `pkg/`, `api/`, `slog`                  | Создать `go.work`, 2 сервиса с `main.go`, настроить `slog` с JSON-логами                                     | 🌐 Gitpod → открыть терминал, запустить `go run ./cmd/catalog`, проверить логи в `/var/log` эмуляторе | Добавить `cart-service` с аналогичной структурой                   |
| **Ср** | Контракты и OpenAPI                 | REST vs gRPC, OpenAPI 3.1, генерация сервера/клиента, валидация                      | `oapi-codegen` → генерация `catalog` из `api/openapi.yaml`, middleware валидации                                       | 🌐 Swagger UI →`/swagger/index.html` → отправить POST/GET, проверить ошибки 400                                               | Добавить `cart-service` OpenAPI, сгенерировать сервер                 |
| **Чт** | Конфигурация и Service Discovery | Env vars,`.env`, `viper`, graceful shutdown, health-checks                                                       | Внедрить `viper` + `config.yaml`, `/health`, `os/signal` для graceful stop                                                     | 🌐 Postman Web → протестировать `/health`, `/metrics`, `/api/v1/...`                                                                 | Настроить hot-reload конфига при изменении `.env`                    |
| **Пт** | 🚀 Проект: E-commerce (старт)      | Версионирование API, idempotency, базовая пагинация                                   | Запустить `catalog` + `cart` в `docker-compose`, настроить cross-service HTTP вызовы                               | 🌐 Killercoda → выполнить сценарий "Deploy Microservices" → проверить статус                                            | Реализовать `user-service` с JWT-аутентификацией (заглушка)   |

---

## 🗓 НЕДЕЛЯ 2: Message Brokers (RabbitMQ/Kafka)

**Цель:** Освоить асинхронную коммуникацию, реализовать систему уведомлений с очередями, понять trade-offs RabbitMQ vs Kafka.

| День       | Цель                                               | Теория                                                                                    | Практика (Go 1.26)                                                                               | Интерактивное задание (браузер)                                                          | ДЗ                                                                                      |
| -------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Пн** | Синхрон vs Асинхрон                     | Pub/Sub, Work Queues, Event Sourcing (базово), когда использовать broker | Сравнение: HTTP vs MQ. Диаграмма потоков данных в E-commerce             | 🌐[MQ Pattern Quiz](https://learn.microsoft.com/en-us/azure/architecture/patterns/) → пройти тест           | Написать в `NOTES.md` 3 случая для async в вашем проекте |
| **Вт** | RabbitMQ Basics                                        | Exchanges, Queues, Bindings, Ack/Nack, DLQ,`rabbitmq/amqp091-go`                              | Producer →`amqp091-go` → publish, Consumer → consume + manual ack                                   | 🌐 RabbitMQ Management UI → создать `notifications`, посмотреть сообщения в Real-time | Добавить retry с exponential backoff                                             |
| **Ср** | Kafka Basics                                           | Topics, Partitions, Offsets, Consumer Groups,`segmentio/kafka-go`                             | Producer →`kafka-go` → send, Consumer → poll + commit                                               | 🌐 Kafka UI → создать `order-events`, проверить partitioning                                     | Сравнить latency RabbitMQ vs Kafka в логах                                  |
| **Чт** | 🚀 Проект: Система уведомлений | Idempotency, message dedup, circuit breaker (базово)                                      | `order-service` → publish `OrderCreated` → `notification-service` → consume + send email (mock) | 🌐 Browser Console → эмулировать storm: 100 msg/s → проверить DLQ и retry                    | Добавить дедупликацию по `order_id`                               |
| **Пт** | Продвинутые паттерны                | Schema Registry (Avro/JSON), dead letter, outbox pattern                                        | Реализовать outbox table в `order-service` + relay consumer                                | 🌐[Killercoda Kafka Scenario](https://killercoda.com) → выполнить "Exactly-Once Delivery"                    | Интегрировать Kafka fallback в систему уведомлений        |

---

## 🗓 НЕДЕЛЯ 3: Мониторинг (Prometheus/Grafana)

**Цель:** Инструментировать Go-сервисы, настроить Prometheus scrape, создать дашборды, алерты, health-чеки.

| День       | Цель                                           | Теория                                                                      | Практика (Go 1.26)                                                                                 | Интерактивное задание (браузер)                                                                             | ДЗ                                                                      |
| -------------- | -------------------------------------------------- | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Пн** | RED/USE методологии                     | Метрики vs Логи vs Трассировки,`prometheus/client_golang` | Добавить `http_request_duration_seconds`, `active_connections`, `queue_depth`                | 🌐[Prometheus Metrics Explorer](https://prometheus.io/docs/prometheus/latest/getting_started/) → query `rate(http_requests_total[5m])` | Добавить бизнес-метрику `orders_created_total`     |
| **Вт** | Prometheus Setup                                   | Scrape configs, service discovery,`prometheus.yml`, `go-metrics` bridge       | Настроить `docker-compose` с Prometheus, добавить `job_name: ecommerce`              | 🌐`localhost:9090` → Targets → проверить `UP`, выполнить PromQL                                                | Настроить relabeling для меток `service`, `env`      |
| **Ср** | Grafana Dashboards                                 | Panels, variables, templating, alerting basics                                    | Подключить Prometheus datasource, создать дашборд: latency, error rate, queue size | 🌐`localhost:3000` → Import `Go Application Dashboard` (ID: 14062)                                                                | Добавить панель `notification_latency_seconds`            |
| **Чт** | Алерты и Health Checks                      | Alertmanager, routing, inhibition,`/health`, `/ready`                         | Настроить алерт `high_error_rate`, `/ready` для K8s readiness probe                   | 🌐 Alertmanager UI → trigger alert → проверить email/webhook mock                                                           | Написать runbook для `queue_stuck` алерта              |
| **Пт** | 🚀 Проект: Полный мониторинг | Centralized logging (базово), Jaeger tracing intro                          | Интегрировать `otel` + `jaeger`, trace `order → notification` flow                     | 🌐 Grafana Explore → trace view → проверить span propagation                                                                | Добавить кастомную панель для `order_service` |

---

## 🗓 НЕДЕЛЯ 4: Тестирование + Финализация

**Цель:** Освоить пирамиду тестов, написать unit/integration/e2e, настроить CI, собрать финальный E-commerce.

| День       | Цель                     | Теория                                                                                           | Практика (Go 1.26)                                                                           | Интерактивное задание (браузер)                                                        | ДЗ                                                                                 |
| -------------- | ---------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| **Пн** | Unit Testing                 | `testing`, `testify`, `gomock`, table-driven tests, `slogtest`                                 | Тесты `cart` service, моки `db`, `http.Client`, coverage                              | 🌐 Replit →`go test -cover ./...` → открыть `cover.html`                                             | Добавить fuzz-тесты для парсинга заказов              |
| **Вт** | Integration Testing          | `testcontainers-go`, Docker-in-Docker, real DB/queue                                                 | Запустить `PostgreSQL` + `RabbitMQ` в тестах, проверить end-to-end flow | 🌐 Killercoda →`testcontainers` sandbox → выполнить тесты                                       | Написать тест на идемпотентность уведомлений |
| **Ср** | E2E Testing                  | `godog`/`ginkgo`, `httptest`, scenario-driven, contract tests                                    | Сценарий "Оформление заказа": HTTP → queue → email mock                    | 🌐 Browser Test Runner → загрузить `features/order.feature` → выполнить шаги            | Добавить negative-сценарии (недостаточно товара)   |
| **Чт** | CI/CD Basics                 | GitHub Actions,`go test -race`, `golangci-lint`, Docker build                                      | Написать pipeline: lint → test → build → push image                                       | 🌐 GitHub Actions UI → просмотреть logs, failed steps, artifacts                                      | Добавить `cache: go` и `matrix: go 1.25, 1.26`                          |
| **Пт** | 🚀 Финал & Защита | Нагрузочное тестирование (`k6`), документация, SRE-чеклист | Запустить `docker-compose up`, `k6 run load.js`, собрать метрики          | 🌐 Grafana Live → мониторинг в реальном времени → демо преподавателю | Подготовить `README.md`, coverage badge, presentation                   |

---

## 📦 Стек и зависимости (Go 1.26)

```bash
go get github.com/prometheus/client_golang/prometheus
go get github.com/rabbitmq/amqp091-go
go get github.com/segmentio/kafka-go
go get github.com/testcontainers/testcontainers-go
go get github.com/oapi-codegen/oapi-codegen/v2/cmd/oapi-codegen
go get github.com/stretchr/testify
go get github.com/spf13/viper
go get go.opentelemetry.io/otel
```

> `go 1.26` поддерживает улучшенный `go work`, `testing/slogtest`, нативную работу с generics в моках, оптимизированный `http.Transport`. Все примеры адаптированы под стандарты 2026 года.

---

## 🎓 Методические рекомендации преподавателя

1. **Интерактивы в браузере:** Используйте Gitpod/Replit для Go-кода, а веб-UI (Swagger, RabbitMQ, Grafana, Prometheus) открывайте в соседних вкладках. Это максимально приближено к production-среде.
2. **Пошаговая отладка:** Всегда запускайте `docker compose logs -f` перед написанием кода. Ошибки брокеров/мониторинга часто решаются на уровне сети, а не кода.
3. **Тестирование:** Не пропускайте `testcontainers`. Интеграционные тесты с реальными БД/очередями экономят часы отладки в продакшене.
4. **Документация:** `ARCHITECTURE.md`, `API.md`, `RUNBOOK.md` — обязательны к концу месяца. Инженер без документации = техдолг.
5. **Оценка:**
   - ✅ 80%+ покрытие тестами
   - ✅ Работающий `docker-compose up` с 4 сервисами
   - ✅ Grafana дашборд с 3+ алертами
   - ✅ README с инструкцией деплоя

---

## 📬 Готовые материалы для запуска

- 📁 Шаблон монорепозитория: `github.com/qwen-course/go-microservices-month6`
- 🐳 `docker-compose.yml` (PostgreSQL, RabbitMQ, Kafka, Prometheus, Grafana, Jaeger)
- 🧪 `testcontainers` fixtures + `k6` load scripts
- 📖 `ARCHITECTURE.md` + `TESTING_GUIDE.md`

Если нужно, могу:

- Сгенерировать полные `go.mod`, `docker-compose.yml`, `main.go` для каждого дня
- Подготовить браузерные сценарии в формате Killercoda/Gitpod
- Добавить CI/CD pipeline с GitHub Actions + Trivy + GoReleaser

Укажите, какой день или инструмент разобрать подробнее, и я подготовлю пошаговый код + интерактивную инструкцию. 🚀
