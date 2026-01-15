# Makefile для управления проектом
# Использование: make <команда>

.PHONY: help install dev build test clean logs stop

# Цвета для вывода
RED=\033[0;31m
GREEN=\033[0;32m
YELLOW=\033[1;33m
NC=\033[0m # No Color

help: ## Показать доступные команды
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# ============================================
# Установка и инициализация
# ============================================

install: ## Установить все зависимости
	@echo "$(GREEN)Установка зависимостей...$(NC)"
	@cd apps/web && npm install
	@cd services/api-gateway && npm install
	@cd services/auth && npm install
	@cd services/users && npm install
	@cd packages/shared && npm install
	@echo "$(GREEN)✓ Зависимости установлены$(NC)"

init: ## Инициализация проекта (первый запуск)
	@echo "$(GREEN)Инициализация проекта...$(NC)"
	@cp .env.example .env
	@cp apps/web/.env.example apps/web/.env
	@cp services/auth/.env.example services/auth/.env
	@cp services/users/.env.example services/users/.env
	@echo "$(GREEN)✓ .env файлы созданы$(NC)"
	@make install
	@echo "$(GREEN)✓ Проект инициализирован$(NC)"
	@echo "$(YELLOW)Следующий шаг: make dev$(NC)"

# ============================================
# Разработка
# ============================================

dev: ## Запустить все сервисы для разработки
	@echo "$(GREEN)Запуск сервисов...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✓ Сервисы запущены$(NC)"
	@echo ""
	@echo "$(GREEN)Доступные сервисы:$(NC)"
	@echo "  $(YELLOW)Web UI:$(NC)           http://localhost:3000"
	@echo "  $(YELLOW)API Gateway:$(NC)      http://localhost:8000"
	@echo "  $(YELLOW)Auth Service:$(NC)     http://localhost:8001"
	@echo "  $(YELLOW)Users Service:$(NC)    http://localhost:8002"
	@echo ""
	@echo "$(GREEN)Dev tools:$(NC)"
	@echo "  $(YELLOW)MailHog:$(NC)          http://localhost:8025"
	@echo "  $(YELLOW)PgAdmin:$(NC)          http://localhost:5050"
	@echo "  $(YELLOW)Redis Commander:$(NC)  http://localhost:8081"
	@echo ""
	@echo "$(YELLOW)Логи: make logs$(NC)"

dev-build: ## Пересобрать и запустить сервисы
	@echo "$(GREEN)Пересборка и запуск...$(NC)"
	docker-compose up -d --build

stop: ## Остановить все сервисы
	@echo "$(YELLOW)Остановка сервисов...$(NC)"
	docker-compose down
	@echo "$(GREEN)✓ Сервисы остановлены$(NC)"

restart: ## Перезапустить все сервисы
	@make stop
	@make dev

# ============================================
# Логи
# ============================================

logs: ## Показать логи всех сервисов
	docker-compose logs -f

logs-web: ## Логи фронтенда
	docker-compose logs -f web

logs-gateway: ## Логи API Gateway
	docker-compose logs -f api-gateway

logs-auth: ## Логи Auth Service
	docker-compose logs -f auth

logs-users: ## Логи Users Service
	docker-compose logs -f users

logs-db: ## Логи PostgreSQL
	docker-compose logs -f postgres

# ============================================
# Тестирование
# ============================================

test: ## Запустить все тесты
	@echo "$(GREEN)Запуск тестов...$(NC)"
	@cd apps/web && npm test
	@cd services/auth && npm test
	@cd services/users && npm test
	@cd tests/e2e && npm test
	@echo "$(GREEN)✓ Все тесты пройдены$(NC)"

test-unit: ## Запустить unit тесты
	@cd apps/web && npm test
	@cd services/auth && npm test
	@cd services/users && npm test

test-e2e: ## Запустить E2E тесты
	@cd tests/e2e && npm test

test-integration: ## Запустить integration тесты
	@cd tests/integration && npm test

# ============================================
# База данных
# ============================================

db-migrate: ## Запустить миграции БД
	@echo "$(GREEN)Запуск миграций...$(NC)"
	@cd services/auth && npm run migrate
	@cd services/users && npm run migrate
	@echo "$(GREEN)✓ Миграции выполнены$(NC)"

db-seed: ## Заполнить БД тестовыми данными
	@echo "$(GREEN)Заполнение тестовыми данными...$(NC)"
	@cd services/auth && npm run seed
	@cd services/users && npm run seed
	@echo "$(GREEN)✓ Данные загружены$(NC)"

db-reset: ## Сбросить и пересоздать БД
	@echo "$(RED)Сброс базы данных...$(NC)"
	docker-compose down -v
	docker-compose up -d postgres redis
	@sleep 3
	@make db-migrate
	@make db-seed
	@echo "$(GREEN)✓ База данных пересоздана$(NC)"

# ============================================
# Сборка
# ============================================

build: ## Собрать все сервисы для production
	@echo "$(GREEN)Сборка для production...$(NC)"
	@cd apps/web && npm run build
	@cd services/api-gateway && npm run build
	@cd services/auth && npm run build
	@cd services/users && npm run build
	@echo "$(GREEN)✓ Сборка завершена$(NC)"

build-docker: ## Собрать Docker образы
	@echo "$(GREEN)Сборка Docker образов...$(NC)"
	docker-compose build
	@echo "$(GREEN)✓ Образы собраны$(NC)"

# ============================================
# Очистка
# ============================================

clean: ## Очистить временные файлы и зависимости
	@echo "$(YELLOW)Очистка...$(NC)"
	@find . -name "node_modules" -type d -prune -exec rm -rf '{}' +
	@find . -name "dist" -type d -prune -exec rm -rf '{}' +
	@find . -name "build" -type d -prune -exec rm -rf '{}' +
	@find . -name ".next" -type d -prune -exec rm -rf '{}' +
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

clean-all: clean ## Полная очистка (включая Docker volumes)
	@echo "$(RED)Полная очистка...$(NC)"
	docker-compose down -v --remove-orphans
	@echo "$(GREEN)✓ Полная очистка завершена$(NC)"

# ============================================
# Утилиты
# ============================================

ps: ## Показать запущенные контейнеры
	docker-compose ps

shell-web: ## Открыть shell в web контейнере
	docker-compose exec web sh

shell-auth: ## Открыть shell в auth контейнере
	docker-compose exec auth sh

shell-users: ## Открыть shell в users контейнере
	docker-compose exec users sh

shell-db: ## Открыть psql в PostgreSQL
	docker-compose exec postgres psql -U postgres

shell-redis: ## Открыть redis-cli
	docker-compose exec redis redis-cli

# ============================================
# Проверки
# ============================================

lint: ## Проверить код линтером
	@echo "$(GREEN)Проверка кода...$(NC)"
	@cd apps/web && npm run lint
	@cd services/api-gateway && npm run lint
	@cd services/auth && npm run lint
	@cd services/users && npm run lint
	@echo "$(GREEN)✓ Проверка завершена$(NC)"

format: ## Отформатировать код
	@echo "$(GREEN)Форматирование кода...$(NC)"
	@cd apps/web && npm run format
	@cd services/api-gateway && npm run format
	@cd services/auth && npm run format
	@cd services/users && npm run format
	@echo "$(GREEN)✓ Форматирование завершено$(NC)"

check: lint test ## Полная проверка (lint + tests)

# ============================================
# Документация
# ============================================

docs-health: ## Проверить здоровье документации (ссылки, структура, статусы)
	@python scripts/check_doc_health.py

docs-health-verbose: ## Проверка документации с подробным выводом
	@python scripts/check_doc_health.py --verbose

docs-links: ## Проверить только ссылки в документации
	@python scripts/check_doc_health.py --check links

docs-structure-check: ## Проверить только структуру документации
	@python scripts/check_doc_health.py --check structure

docs-status: ## Проверить только статусы документов
	@python scripts/check_doc_health.py --check status

docs-metadata: ## Проверить только метаданные документов
	@python scripts/check_doc_health.py --check metadata

docs-markdown: ## Проверить только форматирование markdown
	@python scripts/check_doc_health.py --check markdown

gloss-health: ## Проверить здоровье глоссария
	@python scripts/check_gloss_health.py

gloss-health-verbose: ## Проверка глоссария с подробным выводом
	@python scripts/check_gloss_health.py --verbose

gloss-unused: ## Найти неиспользуемые термины в глоссарии
	@python scripts/check_gloss_health.py --warn-unused

docs-check: docs-health gloss-health ## Полная проверка документации и глоссария

docs-check-deep: ## Глубокий смысловой аудит документации (агрегация контекста для Amy)
	@echo "$(GREEN)Шаг 1: Агрегация контекста документации...$(NC)"
	@python scripts/check_doc_context.py
	@echo ""
	@echo "$(GREEN)✓ Контекст собран: llm_tasks/temp/doc_context.json$(NC)"
	@echo ""
	@echo "$(YELLOW)Следующий шаг:$(NC) Запустите скилл /doc-health-deep для глубокого анализа"
	@echo "$(YELLOW)Скилл автоматически создаст задачи AMY-XXXXX для исправления проблем$(NC)"

docs-structure: ## Обновить структуру проекта в README
	@echo "$(GREEN)Обновление структуры проекта...$(NC)"
	@# TODO: Добавить скрипт генерации структуры
	@echo "$(YELLOW)TODO: Реализовать автогенерацию$(NC)"

# ============================================
# Управление задачами
# ============================================

task-new: ## Создать новую задачу (интерактивно)
	@python scripts/task_new.py -i

task-new-feat: ## Создать задачу FEAT (использование: make task-new-feat TITLE="..." PRIORITY="high")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c feat

task-new-fix: ## Создать задачу FIX (использование: make task-new-fix TITLE="..." PRIORITY="high")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c fix

task-new-docs: ## Создать задачу DOCS (использование: make task-new-docs TITLE="..." PRIORITY="medium")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c docs

backlog-new: ## Создать задачу в бэклоге (интерактивно)
	@python scripts/task_new.py -i

backlog-new-feat: ## Создать задачу FEAT в бэклоге (использование: make backlog-new-feat TITLE="..." PRIORITY="medium")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c feat -f future

backlog-new-fix: ## Создать задачу FIX в бэклоге (использование: make backlog-new-fix TITLE="..." PRIORITY="medium")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c fix -f future

backlog-new-docs: ## Создать задачу DOCS в бэклоге (использование: make backlog-new-docs TITLE="..." PRIORITY="low")
	@python scripts/task_new.py -t "$(TITLE)" -p $(PRIORITY) -c docs -f future

task-complete: ## Завершить задачу (использование: make task-complete ID=FEAT-00001)
	@python scripts/task_complete.py $(ID)

task-move-current: ## Переместить задачу из future в current (использование: make task-move-current ID=FEAT-00001)
	@python scripts/task_move.py $(ID) current

task-move-future: ## Переместить задачу из current в future (использование: make task-move-future ID=FEAT-00001)
	@python scripts/task_move.py $(ID) future

tasks-current: ## Показать текущие задачи
	@cat llm_tasks/current/0_task_index.md

tasks-future: ## Показать бэклог задач
	@cat llm_tasks/future/0_task_index.md

tasks-completed: ## Показать выполненные задачи (последний месяц)
	@ls -t llm_tasks/completed/ | head -1 | xargs -I {} sh -c 'echo "=== Месяц: {} ===" && cat llm_tasks/completed/{}/*/0_task_index.md'

# ============================================
# Управление дискуссиями
# ============================================

discuss-new: ## Создать новую дискуссию (интерактивно)
	@python scripts/discuss_new.py -i

discuss-new-topic: ## Создать дискуссию с темой (использование: make discuss-new-topic TOPIC="...")
	@python scripts/discuss_new.py "$(TOPIC)"

discuss-index: ## Показать индекс дискуссий
	@cat general_docs/01_discuss/000_discuss.md

discuss-delete: ## Удалить дискуссию (использование: make discuss-delete ID="001")
	@python scripts/discuss_delete.py "$(ID)" --force
