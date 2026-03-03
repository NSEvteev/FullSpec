-- Инициализация per-service баз данных PostgreSQL
-- Монтируется в docker-entrypoint-initdb.d/
-- SSOT: specs/docs/.system/infrastructure.md

-- Добавить CREATE DATABASE myapp_{svc} при создании сервиса через analysis chain.
