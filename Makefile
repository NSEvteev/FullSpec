# Makefile — интерфейс команд проекта
# Подробнее: README.md
# Docker: platform/.instructions/standard-docker.md

COMPOSE_FILE = platform/docker/docker-compose.yml
COMPOSE_TEST_FILE = platform/docker/docker-compose.test.yml

.PHONY: dev stop build test test-e2e test-load test-smoke lint clean setup init help sync-structure check-structure

# === Запуск ===

dev:  ## Запустить для разработки
	docker compose -f $(COMPOSE_FILE) up

stop:  ## Остановить сервисы
	docker compose -f $(COMPOSE_FILE) down

# === Сборка ===

build:  ## Собрать для production
	docker compose -f $(COMPOSE_FILE) build

# === Тесты ===

test:  ## Запустить unit/integration тесты
	docker compose -f $(COMPOSE_TEST_FILE) up -d --wait
	pytest src/ tests/integration/ || true
	docker compose -f $(COMPOSE_TEST_FILE) down -v

test-e2e:  ## Запустить e2e тесты
	docker compose -f $(COMPOSE_TEST_FILE) up -d --wait
	pytest tests/e2e/ || true
	docker compose -f $(COMPOSE_TEST_FILE) down -v

test-load:  ## Запустить нагрузочные тесты
	@echo "TODO: настроить нагрузочные тесты (k6)"

test-smoke:  ## Запустить smoke тесты (post-deploy)
	@echo "TODO: настроить smoke тесты (tests/smoke/)"

# === Per-service тесты ===
# Использование: make test-auth, make test-task, make lint-notification

test-%:  ## Тесты одного сервиса (make test-{svc})
	docker compose -f $(COMPOSE_TEST_FILE) up -d --wait
	pytest src/$*/tests/ || true
	docker compose -f $(COMPOSE_TEST_FILE) down -v

lint-%:  ## Линтинг одного сервиса (make lint-{svc})
	@echo "TODO: настроить линтер для src/$*/"

# === Качество кода ===

lint:  ## Линтинг (все сервисы)
	@echo "TODO: настроить линтеры"

# === Утилиты ===

clean:  ## Очистка
	docker compose -f $(COMPOSE_FILE) down -v --remove-orphans

# === Настройка ===

setup:  ## Первоначальная настройка (pre-commit + gh CLI + Docker)
	@echo "📦 Проверка зависимостей..."
	@echo ""
	@echo "1/4 Python..."
	@python --version || (echo "❌ Python не найден. Установите: https://python.org" && exit 1)
	@echo ""
	@echo "2/4 Pre-commit..."
	@pip install pre-commit
	@pre-commit install
	@pre-commit install --hook-type commit-msg
	@echo "✅ Pre-commit хуки установлены"
	@echo ""
	@echo "3/4 GitHub CLI..."
	@gh --version 2>/dev/null || (echo "❌ GitHub CLI не найден. Установите: winget install GitHub.cli" && exit 1)
	@gh auth status 2>/dev/null || (echo "❌ GitHub CLI не авторизован. Выполните: gh auth login" && exit 1)
	@echo ""
	@echo "4/4 Docker..."
	@docker compose version 2>/dev/null || (echo "❌ Docker не найден. Установите Docker Desktop: https://docker.com/products/docker-desktop/" && exit 1)
	@echo ""
	@echo "════════════════════════════════════════"
	@echo "✅ Настройка завершена!"
	@echo ""
	@echo "Следующий шаг:"
	@echo "  cp platform/docker/.env.example platform/docker/.env"
	@echo "  make dev"
	@echo ""
	@echo "Подробнее: .structure/initialization.md"
	@echo "════════════════════════════════════════"

init:  ## Полная инициализация проекта
	@$(MAKE) setup
	@echo ""
	@echo "Синхронизация Labels..."
	@python .github/.instructions/.scripts/sync-labels.py --apply --force 2>/dev/null || echo "Labels: gh CLI не доступен или не авторизован"
	@echo ""
	@echo "Верификация..."
	@pre-commit run --all-files || true
	@echo ""
	@echo "========================================"
	@echo "  Для полной интерактивной настройки:"
	@echo "  Claude Code -> /init-project"
	@echo "========================================"

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
