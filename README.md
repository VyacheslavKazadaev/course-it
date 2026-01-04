# Конспект

## Задание 1: Настройка окружения (45 минут)

```bash
# Шаг 0: Установка Python
sudo apt update
sudo apt install -y python3 python3-pip python3-venv 

# Шаг 1: Проверить установку Python
python --version
# Ожидаемый результат: Python 3.12.x

# Шаг 2: Создать рабочую папку
mkdir ~/it_course
cd ~/it_course
mkdir week1
cd week1

# Шаг 3: Создать первый файл
touch hello.py
```

## Задание 2: Первая программа (60 минут)

**greet_user.go**

## Задание 3: Деплой на GitHub (45 минут)

```bash
# Инициализировать Git репозиторий
git init
git add hello.py
git commit -m "Первая программа - приветствие пользователя"

# Создать аккаунт на GitHub (если нет)
# Создать новый репозиторий "python-basics-week1"
# Связать локальный и удаленный репозиторий
git remote add origin https://github.com/ваш-логин/python-basics-week1.git
git push -u origin master
```