# Makefile для управления миграциями Alembic
#
# Доступные команды:
#   make create-migration name="<описание>" - Создает новую миграцию
#   make upgrade                           - Выполняет все миграции
#   make downgrade                         - Откатывает последнюю миграцию
#   make help                              - Показывает эту справку

# Цель по умолчанию
.DEFAULT_GOAL := help

# Переменная для активации виртуального окружения
ACTIVATE_VENV = bash -c "source ../../.venv/bin/activate &&

# Отображение справки по командам
help:
	@echo "Makefile для управления миграциями Alembic"
	@echo ""
	@echo "Доступные команды:"
	@echo "  make create-migration name='<описание>' - Создает новую миграцию"
	@echo "  make upgrade                          - Выполняет все миграции"
	@echo "  make downgrade                        - Откатывает последнюю миграцию"
	@echo "  make help                             - Показывает эту справку"

# Цель для создания новой миграции. Имя миграции передается как аргумент.
# Пример использования: make create-migration name="add_user_table"
create-migration:
	$(ACTIVATE_VENV) alembic revision --autogenerate -m '$(name)'"

# Цель для выполнения всех ожидающих миграций
upgrade:
	$(ACTIVATE_VENV) alembic upgrade head"

# Цель для отката последней примененной миграции
downgrade:
	$(ACTIVATE_VENV) alembic downgrade -1"

.PHONY: create-migration upgrade downgrade help