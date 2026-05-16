### ASSISTANT

Вот детальный помесячный план **7-го месяца** курса. Каждый день разбит на теорию, практику, интерактивное браузерное задание и проверку. Бэкенд ориентирован на **Python (FastAPI)**, но для каждой задачи указаны эквиваленты на **Go (Gin/Echo + gorilla/websocket)**, чтобы студенты могли выбрать стек и не терять совместимость.

---

## 🗓️ НЕДЕЛЯ 1: Современные паттерны фронтенда + Realtime MVP

*Фокус: Next.js App Router, SSR/SSG/ISR, компоненты, WebSockets, базовая архитектура соцсети.*

### 📅 Понедельник: Архитектура Next.js / Nuxt.js

🎯 **Цель:** Понять разницу между SSR, SSG, ISR, Server/Client Components.📖 **Теория:** Как Next.js рендерит страницы на сервере, кэширует статику, использует `app/` роутер.💻 **Практика:**

1. Создайте проект: `npx create-next-app@latest social-mvp --typescript --tailwind --app`
2. В `app/page.tsx` добавьте `export const dynamic = 'force-dynamic'` для SSR.
3. Создайте `app/layout.tsx` с глобальным `Metadata` и навигацией.
   🌐 **Интерактивное задание:** Откройте [stackblitz.com](https://stackblitz.com) → Next.js → Создайте 2 страницы: `/feed` (SSR) и `/about` (SSG). Добавьте `console.log('render mode')` в компонент и проверьте вывод в терминале StackBlitz.
   ✅ **Проверка:** В логах сервера `/feed` выводит при каждом запросе, `/about` только при сборке.
   🔧 **Бэкенд:** Python: `fastapi run` + `uvicorn`. Go: `go run main.go` с `gin.Default()`.

### 📅 Вторник: Роутинг, Layouts, Data Fetching

🎯 **Цель:** Настроить вложенные роуты, shared layouts, загрузку данных через Server Components.📖 **Теория:** `loading.tsx`, `error.tsx`, `fetch` кэширование, React Server Components.💻 **Практика:**

1. Создайте `app/feed/layout.tsx` с сайдбаром.
2. В `app/feed/page.tsx` добавьте `async function FeedPage() { const res = await fetch('/api/posts') ... }`
3. Реализуйте `loading.tsx` с анимацией.
   🌐 **Интерактивное задание:** В браузере DevTools → Network → Отметьте `Disable cache`. Перезагрузите `/feed`. Убедитесь, что HTML содержит уже отрендеренный список постов (View Source).
   ✅ **Проверка:** В исходном коде страницы есть `<li>` с постами, а не пустой `div`.
   🔧 **Бэкенд:** Python: `@app.get("/api/posts")` → SQLAlchemy query. Go: `r.GET("/api/posts", getPosts)`.

### 📅 Среда: State Management & Realtime Prep

🎯 **Цель:** Подготовить клиентскую часть для WebSocket/SSE, настроить Zustand/Redux Toolkit.📖 **Теория:** Когда использовать клиентский стейт, как избегать перерендеров.💻 **Практика:**

1. `npm i zustand`
2. Создайте `store/postStore.ts` с `addPost`, `updateLikes`.
3. Подготовьте компонент `NewPostForm` с `useEffect` на отправку.
   🌐 **Интерактивное задание:** Откройте [next.new](https://next.new) → Вставьте код стора. В консоли браузера выполните: `import { usePostStore } from './store'; const s = usePostStore.getState(); console.log(s.posts)`.
   ✅ **Проверка:** Выводит `[]` без ошибок.
   🔧 **Бэкенд:** Python: `websockets` или `sse-starlette`. Go: `gorilla/websocket`.

### 📅 Четверг: API Design & DB Schema

🎯 **Цель:** Спроектировать REST-эндпоинты, настроить БД (PostgreSQL/SQLite), миграции.📖 **Теория:** Нормализация, индексы, пагинация, OpenAPI-документация.💻 **Практика:**

1. Python: `pip install fastapi sqlalchemy alembic psycopg2`
2. Создайте модели `User`, `Post`, `Comment`.
3. Реализуйте `/api/posts?limit=20&offset=0`.
   🌐 **Интерактивное задание:** Откройте Swagger UI (`/docs` или `/api/v1/docs`). Отправьте тестовый POST-запрос через интерфейс.
   ✅ **Проверка:** Возвращается `201 Created` с ID записи.
   🔧 **Go:** `gorm` + `gin`, `swag init` для Swagger.

### 📅 Пятница: Realtime Integration

🎯 **Цель:** Подключить WebSocket, отправлять новые посты/комментарии в реальном времени.📖 **Теория:** Heartbeat, reconnect logic, fallback to SSE.💻 **Практика:**

1. На бэке создайте WS-эндпоинт `/ws`.
2. На фронте: `const ws = new WebSocket(wsUrl)`, `onmessage` → `store.addPost(data)`.
3. Добавьте индикатор подключения.
   🌐 **Интерактивное задание:** Откройте 2 вкладки браузера с приложением. В первой создайте пост. Во второй он должен появиться без перезагрузки.
   ✅ **Проверка:** Новый элемент DOM добавляется в обе вкладки ≤ 200мс.
   🔧 **Python:** `websockets.serve(handler)`. **Go:** `websocket.Upgrade()`.

### 📅 Суббота: Code Review & Polish

🎯 **Цель:** Рефакторинг, линтинг, фикс багов, подготовка к оптимизации.
💻 **Практика:** Запустите `next lint`, `prettier --write .`, `pytest`/`go test`. Исправьте варнинги.
🌐 **Интерактивное задание:** Прогоните код через [eslint.org/demo](https://eslint.org/demo) с конфигами Next.js.
✅ **Проверка:** 0 ошибок линтера, 100% покрытие базовых юнит-тестов.

---

## 🗓️ НЕДЕЛЯ 2: Оптимизация производительности + Безопасность

*Фокус: Core Web Vitals, кэширование, XSS/CSRF/JWT, rate-limiting, аудит соцсети.*

### 📅 Понедельник: Core Web Vitals & Asset Optimization

🎯 **Цель:** Улучшить LCP, FID/INP, CLS. Оптимизировать изображения/скрипты.
📖 **Теория:** `next/image`, `next/font`, code splitting, `use client` граница.
💻 **Практика:** Замените `<img>` на `<Image>`, добавьте `font-display: swap`, разделите тяжелые компоненты через `dynamic(() => import(...), { ssr: false })`.
🌐 **Интерактивное задание:** Откройте [pagespeed.web.dev](https://pagespeed.web.dev) → Вставьте локальный URL (`localhost:3000`). Зафиксируйте метрики до/после.
✅ **Проверка:** LCP < 2.5s, CLS < 0.1, INP < 200ms.

### 📅 Вторник: Caching Strategies

🎯 **Цель:** Настроить клиентский (SWR/React Query) и серверный кэш (Redis/Next.js cache).
📖 **Теория:** Stale-while-revalidate, revalidation tags, cache invalidation.
💻 **Практика:** `npm i @tanstack/react-query`. Оберните фетчи в `useQuery({ staleTime: 5000 })`. На сервере используйте `revalidateTag('posts')`.
🌐 **Интерактивное задание:** В DevTools → Application → Storage → Clear cache. Обновите страницу 3 раза подряд. Заметите, что 2-й и 3-й запросы отдают `200 OK (disk cache)` или `304`.
✅ **Проверка:** Количество сетевых запросов сократилось на 60%+.

### 📅 Среда: Auth & Security Basics

🎯 **Цель:** Реализовать JWT, защитить от XSS/CSRF, настроить CORS.📖 **Теория:** HttpOnly cookies, SameSite, CSP, sanitization.💻 **Практика:**

1. Python: `python-jose`, `passlib`, `fastapi.middleware.cors`.
2. Сохраняйте токен в `Set-Cookie; HttpOnly; Secure; SameSite=Lax`.
3. Добавьте `<meta http-equiv="Content-Security-Policy" content="default-src 'self'">`.
   🌐 **Интерактивное задание:** Откройте [securityheaders.com](https://securityheaders.com) → Вставьте URL. Убедитесь, что `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options` = `green`.
   ✅ **Проверка:** Все заголовки безопасности настроены, JWT нельзя прочитать через `document.cookie`.

### 📅 Четверг: Input Validation & Rate Limiting

🎯 **Цель:** Валидировать данные на фронте и бэке, ограничить запросы.
📖 **Теория:** Zod/Pydantic/Gin binding, sliding window rate limit, brute-force protection.
💻 **Практика:** Python: `pydantic` модели + `slowapi`. Go: `validator` + `ulule/limiter`.
🌐 **Интерактивное задание:** В Postman/Insomnia отправьте 10 запросов за 5 сек к `/api/posts`. 11-й должен вернуть `429 Too Many Requests`.
✅ **Проверка:** Валидация отклоняет `<script>` в полях, rate limit срабатывает.

### 📅 Пятница: Security Audit & Performance Profiling

🎯 **Цель:** Провести аудит, найти утечки, оптимизировать рендер.
📖 **Теория:** React DevTools Profiler, Next.js `next dev --turbo`, bundle analysis.
💻 **Практика:** `npm run build && npx next bundle-analyzer`. Оптимизируйте `useMemo`, `React.memo` на тяжелых списках.
🌐 **Интерактивное задание:** В DevTools → Performance → Запишите 5 сек скролла ленты. Найдите `Long Task` > 50ms. Устраните через `requestIdleCallback` или виртуализацию.
✅ **Проверка:** Нет Long Tasks > 50ms, размер JS-бандла < 200KB gzip.

### 📅 Суббота: Refactor & Documentation

🎯 **Цель:** Документировать API, добавить OpenAPI, подготовить чек-лист безопасности.
💻 **Практика:** Напишите `SECURITY.md`, `PERFORMANCE.md`, добавьте комментарии к эндпоинтам.
🌐 **Интерактивное задание:** Сгенерируйте клиентскую библиотеку через `openapi-generator` и импортируйте в отдельный файл. Проверьте автодополнение в IDE.
✅ **Проверка:** Swagger UI обновлен, клиенты генерируются без ошибок.

---

## 🗓️ НЕДЕЛЯ 3: SaaS архитектура + SEO & Accessibility

*Фокус: Подписки, Stripe, RBAC, мультиарендность, SEO, a11y, WCAG.*

### 📅 Понедельник: Subscription Models & Payments

🎯 **Цель:** Интегрировать Stripe, обработать вебхуки, создать тарифы.
📖 **Теория:** Checkout Session, webhook signature verification, idempotency.
💻 **Практика:** Python: `stripe` SDK, `stripe.Webhook.construct_event`. Go: `stripe-go`, ручная проверка `Stripe-Signature`.
🌐 **Интерактивное задание:** В Stripe Dashboard → Developers → Webhooks → Добавьте `localhost:3000/api/webhooks/stripe`. Отправьте тестовый `checkout.session.completed`.
✅ **Проверка:** БД обновляет `user.subscription = 'pro'`, лог показывает `200 OK`.

### 📅 Вторник: RBAC & Multi-tenancy

🎯 **Цель:** Роли `user/admin`, изоляция данных, feature flags.
📖 **Теория:** Middleware авторизации, `tenant_id` в схемах, soft delete.
💻 **Практика:** Добавьте `@require_role("admin")` (Python) / `middleware.Auth()` (Go). Фильтруйте запросы по `user.organization_id`.
🌐 **Интерактивное задание:** Войдите как `user` и `admin`. Попробуйте вызвать `DELETE /api/posts/{id}`. `user` → 403, `admin` → 200.
✅ **Проверка:** Разделение прав работает, данные организаций не пересекаются.

### 📅 Среда: SEO Fundamentals

🎯 **Цель:** Meta-теги, Open Graph, sitemap.xml, canonical, structured data.
📖 **Теория:** Как поисковики индексируют SPA/SSR, микроразметка JSON-LD.
💻 **Практика:** В `layout.tsx` добавьте `metadata: { title, description, openGraph }`. Сгенерируйте `sitemap.ts` через `next-sitemap`.
🌐 **Интерактивное задание:** Откройте [search.google.com/test/rich-results](https://search.google.com/test/rich-results) → Вставьте URL страницы. Проверьте валидность JSON-LD.
✅ **Проверка:** Rich Results тест проходит, `robots.txt` и `sitemap.xml` доступны.

### 📅 Четверг: Accessibility (a11y)

🎯 **Цель:** WCAG 2.2, ARIA, keyboard navigation, color contrast.
📖 **Теория:** Focus traps, skip links, `alt` тексты, семантика.
💻 **Практика:** Добавьте `skip-link`, проверьте контраст через `tailwind` цвета, используйте `<button>` вместо `<div onClick>`.
🌐 **Интерактивное задание:** Установите расширение [axe DevTools](https://www.deque.com/axe/devtools/). Запустите аудит на `/feed`. Исправьте все `Critical` и `Serious` нарушения.
✅ **Проверка:** axe показывает 0 нарушений. Навигация `Tab` работает полностью.

### 📅 Пятница: SaaS MVP + SEO/a11y Implementation

🎯 **Цель:** Собрать рабочий SaaS-лендинг с тарифами, SEO-оптимизацией и доступностью.
💻 **Практика:** Интегрируйте всё из недели. Добавьте `/pricing`, `/dashboard`, `/settings`.
🌐 **Интерактивное задание:** Протестируйте покупку подписки в режиме тестовой карты Stripe (`4242...`). Проверьте, что страница рейтинга проходит Lighthouse ≥ 90 по всем категориям.
✅ **Проверка:** Покупка проходит, Lighthouse ≥ 90, axe = 0 ошибок.

### 📅 Суббота: Testing & Final Adjustments

🎯 **Цель:** E2E тесты (Playwright), фикс багов, подготовка к портфолио.
💻 **Практика:** `npx playwright install`, напишите тест `pricing.spec.ts` → клик `Subscribe` → проверка `URL contains /dashboard`.
🌐 **Интерактивное задание:** Запустите `npx playwright test --ui`. Убедитесь, что 100% тестов проходят.
✅ **Проверка:** E2E зеленые, покрытие критических путей ≥ 80%.

---

## 🗓️ НЕДЕЛЯ 4: Полномасштабный портфолио-проект + Deployment

*Фокус: Monorepo, CI/CD, edge-функции, мониторинг, деплой, упаковка.*

### 📅 Понедельник: Architecture & Monorepo

🎯 **Цель:** Структурировать проект, вынести shared-код, настроить workspace.
📖 **Теория:** Turborepo, shared UI/DB types, workspace dependencies.
💻 **Практика:** `npx create-turbo@latest`. Папки: `apps/web`, `apps/api`, `packages/ui`, `packages/db`.
🌐 **Интерактивное задание:** В `packages/ui` создайте `Button.tsx`. Импортируйте в `apps/web`. Запустите `turbo dev`.
✅ **Проверка:** Изменения в `packages` применяются без перезапуска `web`.

### 📅 Вторник: CI/CD Pipeline

🎯 **Цель:** Автоматизировать линт, тесты, билд, деплой на PR.
📖 **Теория:** GitHub Actions, caching, environment secrets, preview deployments.
💻 **Практика:** Создайте `.github/workflows/ci.yml`: `lint → test → build → deploy-preview`.
🌐 **Интерактивное задание:** Откройте [github.com/actions](https://github.com/features/actions) → Вставьте workflow. Сделайте PR. Убедитесь, что проверки проходят.
✅ **Проверка:** Все шаги зеленые, preview URL доступен в комментариях PR.

### 📅 Среда: Advanced Optimization

🎯 **Цель:** Edge functions, prefetching, bundle treeshaking, CDN.
📖 **Теория:** Vercel Edge/Cloudflare Workers, `next/prefetch`, `experimental.optimizePackageImports`.
💻 **Практика:** Перенесите `/api/search` в `app/api/search/route.ts` (Edge runtime). Добавьте `prefetch` на ссылки.
🌐 **Интерактивное задание:** В DevTools → Network → Проверьте, что `/api/search` отвечает из `Edge` (TTFB < 50ms).
✅ **Проверка:** Время отклика API снижено на 70%+.

### 📅 Четверг: Security Hardening & Monitoring

🎯 **Цель:** Sentry, OpenTelemetry, log aggregation, error boundaries.
📖 **Теория:** Tracing, error sampling, PII masking.
💻 **Практика:** Интегрируйте `@sentry/nextjs` и `@sentry/node`. Добавьте `ErrorBoundary`. Настройте `sentry.dsn` в env.
🌐 **Интерактивное задание:** Вызовите `throw new Error('test')` в компоненте. Проверьте, что ошибка попала в Sentry Dashboard с stack trace.
✅ **Проверка:** Ошибка logged, user context attached, no PII leaked.

### 📅 Пятница: Deployment & Final QA

🎯 **Цель:** Деплой на Vercel/Render/AWS, smoke tests, production readiness.
📖 **Теория:** Zero-downtime deploys, health checks, graceful shutdown.
💻 **Практика:** Подключите репозиторий к Vercel (web) и Render/Railway (api). Настройте переменные окружения.
🌐 **Интерактивное задание:** Откройте [uptimerobot.com](https://uptimerobot.com) → Добавьте URL. Запустите 10-минутный smoke test: регистрация → покупка → создание поста → логаут.
✅ **Проверка:** 100% uptime, все сценарии проходят без 5xx.

### 📅 Суббота: Portfolio Packaging

🎯 **Цель:** README, демо-видео, live link, архитектура-схема, подготовка к собеседованиям.
💻 **Практика:** Напишите `README.md` с: Tech stack, Architecture diagram (Mermaid), Setup, Live demo, Lessons learned. Запишите 3-мин видео демо.
🌐 **Интерактивное задание:** Залейте на GitHub Pages/Notion. Протестируйте ссылку с мобильного. Попросите коллегу пройти по чек-листу.
✅ **Проверка:** README ≥ 400 строк, видео < 3 мин, ссылка работает на всех устройствах.

---

## 🛠️ Рекомендации по оценке и поддержке

1. **Ежедневный чек-ин:** Студент отправляет PR с флагом `ready-for-review`. Наставник проверяет по чек-листу (теория → код → тесты → безопасность → производительность).
2. **Интерактивные платформы:**
   - `stackblitz.com` / `next.new` для быстрого прототипирования
   - `replit.com` для бэкенда с pre-installed Python/Go
   - `web.dev/measure` и `axe.dev` для аудита
3. **Критерии успеха месяца:**
   - ✅ 3 проекта в портфолио с live links
   - ✅ Lighthouse ≥ 90, axe = 0, Core Web Vitals green
   - ✅ CI/CD pipeline, мониторинг ошибок, документация
   - ✅ Защита от OWASP Top 10, валидация, rate limiting
   - ✅ Готовность к собеседованиям по Full-Stack + Security/Perf

Если нужно, могу сгенерировать:

- Готовые репозитории-шаблоны (Next.js + FastAPI/Gin + Docker + CI)
- Чек-листы для код-ревью по каждому дню
- Наборы тестовых данных и мок-серверы для локального запуска без регистрации в Stripe/DB

Уточните, какую часть детализировать или адаптировать под конкретный стек студента.
