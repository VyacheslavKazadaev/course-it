# 📚 Неделя 3: Git и GitHub/GitLab (Ветвление, Слияние, Pull Requests)

---

## 🎯 Цели Недели 3

| День | Тема | Практика |
|------|------|----------|
| **День 1** | Ветвление (Branching) | Создание и переключение веток |
| **День 2** | Слияние (Merging) | Merge, конфликты, разрешение |
| **День 3** | Pull/Merge Requests | Code review, workflow |
| **День 4** | Стратегии ветвления | GitFlow, GitHub Flow, Trunk-Based |
| **День 5** | Финальный проект | Полный цикл разработки |

---

## 📖 День 1: Ветвление (Branching)

### Теория

**Что такое ветка?**
Ветка — это независимая линия разработки, которая позволяет работать над функциями без влияния на основную кодовую базу .

```bash
# Просмотр всех веток
git branch

# Создание новой ветки
git branch feature/login

# Переключение на ветку
git checkout feature/login

# Создание и переключение (современный способ)
git switch -c feature/login

# Просмотр всех веток (локальных и удалённых)
git branch -a
```

### 🎮 Интерактивные упражнения в браузере

| Ресурс | Описание | Ссылка |
|--------|----------|--------|
| **Learn Git Branching** | Визуальная игра с уровнями | [learngitbranching.js.org](https://learngitbranching.js.org/)  |
| **Git Rail Control** | Интерактивное обучение Git | [thomasthornton.cloud](https://thomasthornton.cloud/git-rail-control-an-interactive-way-to-learn-git/)  |
| **Git Game** | Геймифицированное обучение | [git-game.com](https://www.git-game.com/) |

### ✅ Задание 1.1: Базовое ветвление

```bash
# 1. Создайте репозиторий (если нет)
git init week3-project
cd week3-project

# 2. Создайте начальный коммит
echo "# Week 3 Project" > README.md
git add README.md
git commit -m "Initial commit"

# 3. Создайте ветку feature/header
git switch -c feature/header

# 4. Внесите изменения
echo "## Header Section" >> README.md
git add .
git commit -m "Add header section"

# 5. Вернитесь на main
git switch main

# 6. Проверьте, что изменения только в ветке
cat README.md
```

**📝 Отчёт:** Сделайте скриншот вывода `git branch -v` и покажите структуру веток.

---

## 📖 День 2: Слияние (Merging) и Конфликты

### Теория

**Типы слияния:**
- **Fast-forward** — когда нет новых коммитов в целевой ветке 
- **Three-way merge** — создаётся новый коммит слияния
- **Rebase** — переписывает историю (осторожно!)

```bash
# Базовое слияние
git switch main
git merge feature/header

# Слияние с rebase (альтернатива)
git switch feature/header
git rebase main

# Отмена слияния при конфликте
git merge --abort
```

### 🎮 Интерактивные упражнения

| Упражнение | Фокус | Ссылка |
|------------|-------|--------|
| **Merge Conflicts Game** | Разрешение конфликтов | [mergely.com](https://www.mergely.com/) |
| **Git Conflict Resolver** | Визуализация конфликтов | [gitconflict.com](https://gitconflict.com/) |

### ✅ Задание 2.1: Создание и разрешение конфликта

```bash
# 1. На main измените README.md
echo "## Main Content" >> README.md
git add .
git commit -m "Add main content on main"

# 2. Переключитесь на feature/header
git switch feature/header

# 3. Измените ТО ЖЕ место в файле
echo "## Different Content" >> README.md
git add .
git commit -m "Add different content on feature"

# 4. Попробуйте слить
git switch main
git merge feature/header
# ⚠️ Появится конфликт!

# 5. Откройте README.md и разрешите конфликт вручную
# <<<<<<< HEAD
# ## Main Content
# =======
# ## Different Content
# >>>>>>> feature/header

# 6. После разрешения
git add README.md
git commit -m "Resolve merge conflict"
```

**📝 Отчёт:** Скриншот файла до и после разрешения конфликта.

---

## 📖 День 3: Pull Requests / Merge Requests

### Теория

**Pull Request (GitHub) / Merge Request (GitLab)** — механизм код-ревью перед слиянием .

```
┌─────────────────────────────────────────────────────────┐
│                    PR Workflow                          │
│                                                         │
│  1. Fork repo → 2. Clone → 3. Branch → 4. Commit       │
│         ↓                                               │
│  5. Push → 6. Create PR → 7. Review → 8. Merge         │
└─────────────────────────────────────────────────────────┘
```

**Best Practices для PR :**
- ✅ Держите PR маленькими и сфокусированными
- ✅ Запрашивайте code review перед мерджем
- ✅ Используйте чек-листы для проверки
- ✅ Пишите осмысленные описания изменений

### 🎮 Интерактивные упражнения

| Платформа | Упражнение | Ссылка |
|-----------|------------|--------|
| **GitHub** | First PR Tutorial | [github.com/first-contributions](https://github.com/first-contributions/first-contributions)  |
| **GitLab** | Merge Request Guide | [docs.gitlab.com/ee/user/project/merge_requests/](https://docs.gitlab.com/ee/user/project/merge_requests/)  |
| **Visual Guide** | PR Visualization | [github.com/yangsu/pull-request-tutorial](https://github.com/yangsu/pull-request-tutorial)  |

### ✅ Задание 3.1: Создание Pull Request

```bash
# 1. Создайте ветку для новой функции
git switch -c feature/footer

# 2. Добавьте изменения
echo "## Footer" >> README.md
git add .
git commit -m "Add footer section"

# 3. Запушьте ветку
git push -u origin feature/footer

# 4. На GitHub/GitLab:
#    - Откройте репозиторий
#    - Нажмите "Compare & pull request"
#    - Заполните описание
#    - Запросите review
```

**📝 Чек-лист PR:**
- [ ] Заголовок описывает изменение
- [ ] Описание включает "что" и "почему"
- [ ] Связанные issue упомянуты
- [ ] Код проходит CI/CD проверки
- [ ] Запрошен минимум 1 ревьюер

---

## 📖 День 4: Стратегии Ветвления

### Теория: Современные подходы 2025-2026

| Стратегия | Описание | Когда использовать |
|-----------|----------|-------------------|
| **Trunk-Based** | Короткоживущие ветки, мердж в main  | CI/CD, небольшие команды |
| **GitHub Flow** | Feature branches → PR → main  | Веб-приложения, SaaS |
| **GitFlow** | develop + feature + release + hotfix  | Релизные циклы, enterprise |
| **GitLab Flow** | Environment branches  | GitLab, деплой по окружениям |

```
┌────────────────────────────────────────────────────────────┐
│              Trunk-Based Development (2026 Trend)     │
│                                                            │
│  main ─●────●────●────●────●────●────●────●───►           │
│          ╲          ╱                                      │
│  feature  ●────●──●                                        │
│                                                            │
│  ⚡ Ветки живут < 1 дня, мердж несколько раз в день         │
└────────────────────────────────────────────────────────────┘
```

### Naming Conventions 2025 

```bash
# ✅ Правильно
feature/user-authentication
bugfix/login-error-404
hotfix/security-patch
release/v2.1.0

# ❌ Неправильно
new-stuff
fix
test
my-branch
```

### ✅ Задание 4.1: Выбор стратегии

**Сценарий:** Вы работаете в команде из 5 разработчиков над веб-приложением с ежедневными деплоями.

**Вопросы:**
1. Какую стратегию ветвления выберете? Почему?
2. Как назовете ветку для функции "добавление корзины"?
3. Как часто будете мерджить в main?

**📝 Отчёт:** Напишите документ `BRANCH_STRATEGY.md` с вашими решениями.

---

## 📖 День 5: Финальный Проект

### 🏆 Капstone Project: "Командная Разработка"

**Цель:** Пройти полный цикл разработки с использованием всех изученных концепций.

```
┌─────────────────────────────────────────────────────────────┐
│                    Финальный Проект                         │
│                                                             │
│  📁 Создать репозиторий на GitHub/GitLab                   │
│  🌿 Создать 3 feature ветки                                │
│  🔀 Сделать merge с разрешением конфликтов                 │
│  📝 Создать 2 Pull Requests с code review                  │
│  🏷️ Добавить теги версий                                  │
│  📊 Написать README с workflow диаграммой                  │
└─────────────────────────────────────────────────────────────┘
```

### ✅ Требования к проекту

| № | Задача | Баллы |
|---|--------|-------|
| 1 | Репозиторий с ≥5 коммитами | 10 |
| 2 | Минимум 3 ветки (feature/*) | 15 |
| 3 | 2 PR с описанием и review | 25 |
| 4 | Разрешённый merge конфликт | 20 |
| 5 | BRANCH_STRATEGY.md документ | 15 |
| 6 | Теги версий (v1.0.0) | 10 |
| 7 | Clean commit history | 5 |
| **Итого** | | **100** |

### 📋 Шаблон Pull Request

```markdown
## Описание изменений
<!-- Что было изменено и почему -->

## Тип изменений
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📝 Documentation
- [ ] ♻️ Refactoring

## Чек-лист
- [ ] Код протестирован
- [ ] Документация обновлена
- [ ] CI/CD проходит
- [ ] Нет merge конфликтов

## Скриншоты (если применимо)
<!-- Добавьте скриншоты изменений -->

## Related Issues
Closes #<номер>
```

---

## 🛠️ Дополнительные Ресурсы

### Интерактивные Платформы

| Платформа | Тип | Ссылка |
|-----------|-----|--------|
| Learn Git Branching | Игра | [learngitbranching.js.org](https://learngitbranching.js.org/)  |
| GitHub Skills | Курсы | [skills.github.com](https://skills.github.com/) |
| GitLab Demo | Песочница | [gitlab.com](https://gitlab.com/) |
| Oh My Git! | Визуализация | [ohmygit.org](https://ohmygit.org/)  |

### Cheatsheet

```bash
# 🔍 Просмотр
git branch -v          # Ветки с последними коммитами
git log --oneline --graph --all  # История с графом

# 🌿 Ветки
git switch -c <name>   # Создать и переключиться
git branch -d <name>   # Удалить ветку
git branch -m <old> <new>  # Переименовать

# 🔀 Слияние
git merge <branch>     # Слить ветку
git merge --abort      # Отменить слияние
git rebase <branch>    # Перебазировать

# 📤 Remote
git push -u origin <branch>  # Push с tracking
git pull --rebase      # Pull с rebase
git fetch --prune      # Очистить stale branches 
```

---

## 📊 Оценка Прогресса

```
День 1: [ ] Теория  [ ] Упражнения  [ ] Задание
День 2: [ ] Теория  [ ] Упражнения  [ ] Задание
День 3: [ ] Теория  [ ] Упражнения  [ ] Задание
День 4: [ ] Теория  [ ] Упражнения  [ ] Задание
День 5: [ ] Проект  [ ] Документация  [ ] Презентация
```

---

## 🎓 Критерии Успешного Завершения

- ✅ Понимаете разницу между merge и rebase
- ✅ Можете создать и разрешить merge конфликт
- ✅ Знаете когда использовать какую стратегию ветвления 
- ✅ Создали рабочий PR с code review
- ✅ Удаляете stale branches регулярно 

---

**🚀 Готовы начать?** Выберите день и приступайте к первому заданию! Если нужны уточнения по любому пункту — спрашивайте.

### USER
```
Очистить stale branches
```
что это значит?

### ASSISTANT
## 🧹 Что такое "Stale Branches" (Устаревшие ветки)?

**Stale branches** — это ветки в Git, которые **больше не нужны**, но всё ещё существуют в вашем репозитории. Они "загрязняют" историю и могут вызывать путаницу.

---

### 📋 Типы устаревших веток

| Тип | Описание | Пример |
|-----|----------|--------|
| **Слитые ветки** | Уже merged в main, но не удалены | `feature/login` после PR ✅ |
| **Заброшенные ветки** | Нет коммитов > 30 дней | `feature/old-experiment` |
| **Неактуальные ветки** | Задача отменена/изменилась | `bugfix/wont-fix` |
| **Локальные "призраки"** | Удалены на remote, но есть локально | `origin/deleted-branch` |

---

### 🔍 Как найти stale branches

```bash
# 1. Показать ветки, слитые в main
git branch --merged main

# 2. Показать ветки, НЕ слитые в main
git branch --no-merged main

# 3. Показать ветки с датой последнего коммита
git branch -v

# 4. Найти ветки без коммитов > 30 дней
git fetch --prune --dry-run  # preview
```

---

### 🧹 Как очистить stale branches

```bash
# ⚠️ Удалить локальную ветку (безопасно, если слита)
git branch -d feature/login

# ⚠️⚠️ Принудительное удаление (если не слита)
git branch -D feature/old-experiment

# 🌐 Удалить ветку на remote
git push origin --delete feature/login

# 🧹 Очистить удалённые треки (если ветка удалена на server)
git fetch --prune
git remote prune origin

# 🚀 Всё в одной команде (GitHub CLI)
gh pr list --state merged | xargs -I {} gh branch delete {}
```

---

### 📊 Визуализация проблемы

```
ДО очистки:                          ПОСЛЕ очистки:
┌────────────────────────┐          ┌────────────────────────┐
│  main ─────●───────────│          │  main ─────●───────────│
│     ╲      │           │          │                        │
│  feature1 ● (merged)   │   ──→    │                        │
│     ╲      │           │          │                        │
│  feature2 ● (abandoned)│          │                        │
│            │           │          │                        │
│  feature3 ● (active)   │          │  feature3 ● (active)   │
└────────────────────────┘          └────────────────────────┘
     ❌ 5 веток                          ✅ 2 ветки
```

---

### ✅ Best Practices 2025-2026

| Практика | Команда | Частота |
|----------|---------|---------|
| Удалять ветку после merge | `git branch -d <branch>` | После каждого PR |
| Очищать remote треки | `git fetch --prune` | Раз в неделю |
| Автоматическое удаление | GitHub: "Delete branch on merge" | В настройках репозитория |
| Ревизия старых веток | `git branch -v --sort=-committerdate` | Раз в месяц |

---

### ⚠️ Предупреждения

```bash
# ❌ ОПАСНО: Удаление активной ветки
git branch -D feature/in-progress  # Потеряете изменения!

# ✅ БЕЗОПАСНО: Сначала проверьте
git branch --merged main           # Что можно удалить?
git log feature/branch --oneline   # Что внутри?

# ✅ СОХРАНИТЕ перед удалением
git branch -m feature/old feature/old-backup
```

---

### 🤖 Автоматизация (GitHub Actions)

```yaml
# .github/workflows/cleanup-stale-branches.yml
name: Cleanup Stale Branches
on:
  schedule:
    - cron: '0 0 * * 0'  # Каждое воскресенье

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Delete merged branches
        run: |
          git fetch --prune
          git branch --merged main | grep -v "main" | xargs git branch -d
```

---

### 📝 Чек-лист для вашей команды

```markdown
## Stale Branch Policy

- [ ] Ветка удаляется сразу после merge PR
- [ ] Включена опция "Delete branch on merge" в GitHub/GitLab
- [ ] Раз в неделю: `git fetch --prune`
- [ ] Ветки > 30 дней без активности помечаются как stale
- [ ] Перед удалением: проверка, что ветка слита
```

---

**🎯 Итог:** Stale branches — это "мусор" в репозитории. Регулярная очистка keeps your repo clean, улучшает производительность и снижает путаницу в команде! 

Хотите, чтобы я добавил это задание в День 5 финального проекта? 🚀