# Makefile — интерфейс команд проекта
# Подробнее: README.md

.PHONY: dev stop build test test-e2e test-load lint clean help

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

init:  ## Инициализация проекта
	@echo "TODO: настроить инициализацию"

# === Справка ===

help:  ## Показать эту справку
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
