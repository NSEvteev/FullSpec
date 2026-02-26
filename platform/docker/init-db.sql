-- Инициализация per-service баз данных PostgreSQL
-- Монтируется в docker-entrypoint-initdb.d/
-- SSOT: specs/docs/.system/infrastructure.md

CREATE DATABASE myapp_auth;
CREATE DATABASE myapp_task;
CREATE DATABASE myapp_notification;
CREATE DATABASE myapp_admin;
