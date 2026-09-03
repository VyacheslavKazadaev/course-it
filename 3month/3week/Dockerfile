FROM python:3.12-alpine

WORKDIR /app

# Установка системных зависимостей, если они требуются для компиляции пакетов из requirements.txt
RUN apk add --no-cache gcc musl-dev linux-headers

# Копируем файл зависимостей pip
COPY requirements.txt .

# Устанавливаем зависимости через pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код приложения
COPY . .

# Создание скрипта для активации venv и запуска приложения
CMD ["python", "main.py"]