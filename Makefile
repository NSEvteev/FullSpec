# Makefile — интерфейс команд проекта
# Подробнее: README.md

.PHONY: dev stop build test test-e2e test-load lint clean setup init help sync-structure check-structure

# === Запуск ===

dev:  ## Запустить для разработки
	docker-compose -f docker-compose.dev.yml up

stop:  ## Остановить сервисы
	docker-compose down

# === Сборка ===

build:  ## Собрать для production
	docker-compose build

# === Тесты ===

test:  ## Запустить unit/integration тесты
	@echo "TODO: настроить запуск тестов"

test-e2e:  ## Запустить e2e тесты
	@echo "TODO: настроить e2e тесты"

test-load:  ## Запустить нагрузочные тесты
	@echo "TODO: настроить нагрузочные тесты (k6)"

# === Качество кода ===

lint:  ## Линтинг
	@echo "TODO: настроить линтеры"

# === Утилиты ===

clean:  ## Очистка
	docker-compose down -v --remove-orphans

# === Настройка ===

setup:  ## Первоначальная настройка (pre-commit хуки)
	@echo "📦 Установка pre-commit..."
	pip install pre-commit
	pre-commit install
	@echo "✅ Pre-commit хуки установлены"
	@echo ""
	@echo "Теперь при каждом коммите будут проверяться:"
	@echo "  • Синхронизация README с файловой системой"
	@echo ""
	@echo "Готово! Используйте 'make dev' для запуска."

init:  ## Полная инициализация проекта
	@$(MAKE) setup
	@echo "TODO: дополнительная инициализация (копирование .env.example и т.д.)"

# === Структура ===

sync-structure:  ## Проверить и исправить структуру README
	python .structure/.instructions/.scripts/validate-structure.py --fix
	python .structure/.instructions/.scripts/sync-readme.py --all --fix

check-structure:  ## Проверить структуру README (без исправлений)
	python .structure/.instructions/.scripts/pre-commit-structure.py

# === Справка ===

help:  ## Показать эту справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
