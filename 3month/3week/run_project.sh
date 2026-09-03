#!/bin/bash

# Немедленный выход, если команда завершается с ненулевым статусом
set -e

echo "Starting the project..."

# Создаем .env из .env_example если он не существует
if [ ! -f .env ]; then
    echo "Creating .env file from .env_example..."
    cp .env_example .env
    echo ".env file created successfully!"
else
    echo ".env file already exists."
fi

# Поднимаем postgresql и migrator
echo "Starting PostgreSQL and running migrations..."
docker compose up -d postgresql api migrator

# Ждем, пока миграции завершатся
echo "Waiting for migrations to complete..."
while [[ ! "$(docker compose ps migrator -a --format json | jq -r '.State')" =~ ^[[:space:]]*exited[[:space:]]*$ ]] || [[ "$(docker compose ps migrator -a --format json | jq -r '.ExitCode')" -ne 0 ]]; do
    echo "Waiting for migration container to finish..."
    sleep 5
done

echo "Migrations completed successfully!"

# Проверяем статус контейнеров
echo "Current status:"
docker compose ps

echo "Project started successfully! PostgreSQL is running and migrations are applied."
echo "You can now start your main application service."