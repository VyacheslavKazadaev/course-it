# Конспект

## 1-2 день

### Задание 1: Настройка окружения (45 минут)

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

### Задание 2: Первая программа (60 минут)

**greet_user.go**

### Задание 3: Деплой на GitHub (45 минут)

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

### Практические задачи

* Калькулятор в консоли
* Конвертер валют

### Git практика: создание новых веток в консоли

```bash
# Обновить репозиторий
git add calculator.py currency_converter.py
git commit -m "Добавлены калькулятор и конвертер валют"

# Создать ветку для улучшений
git checkout -b feature/improvements
# Внести изменения в один из файлов
git add .
git commit -m "Добавлена дополнительная функция"
git push origin feature/improvements

# Вернуться в основную ветку
git checkout master
```

## 3-4 день

### Циклы и списки

Интерактивные упражнения (15 минут):

* Python Loops на learnpython.org
* Python Lists на learnpython.org
* Python Dictionaries на learnpython.org
* Sets на learnpython.org

* **loops_lists.py**
* **dict.py**
* **sets_tuple.py**

Визуализация (15 минут):

[Python Tutor](https://pythontutor.com/?spm=a2ty_o01.29997173.0.0.4a565171ebn7Tm) - визуализатор выполнения кода
Протестировать несколько примеров с циклами и списками

### Практика

* Таблица умножения 
* Список покупок: list_buy.py




