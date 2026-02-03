# Продолжение: Pre-commit хуки

## Что сделано

1. **Makefile** — добавлен `make setup` для установки pre-commit
2. **README.md** и **CLAUDE.md** — добавлены инструкции про `make setup`
3. **validate-rule.py** — адаптирован для приёма пути к файлу (работает)
4. **validate-skill.py** — адаптирован для приёма пути к файлу (работает)
5. **.pre-commit-config.yaml** — добавлены 4 хука:
   - `structure-sync` ✅ работает
   - `rules-validate` ✅ работает
   - `scripts-validate` ❌ падает (см. ниже)
   - `skills-validate` ✅ работает
6. **TODO-cicd-integration.md** — обновлён план, убран GitHub Actions

## Проблема

`scripts-validate` падает потому что pre-commit передаёт **несколько файлов** одной командой:

```
python validate-script.py file1.py file2.py file3.py
```

А скрипт принимает только один файл (`nargs="?"`).

## Что нужно сделать

1. В `.instructions/.scripts/validate-script.py`:
   - Изменить `parser.add_argument("path", nargs="?", ...)` → `nargs="*"`
   - Изменить логику: `elif args.path:` → `elif args.path:` с обработкой списка
   - Уже начал менять docstring

2. Аналогично проверить `validate-rule.py` и `validate-skill.py` — они тоже должны принимать несколько файлов

3. Закоммитить и протестировать

## Быстрый фикс (альтернатива)

Можно в `.pre-commit-config.yaml` добавить для каждого хука:
```yaml
require_serial: true
```
Это заставит pre-commit вызывать скрипт для каждого файла отдельно. Медленнее, но проще.

## Файлы для редактирования

- `.instructions/.scripts/validate-script.py` (строки 306-325)
- `.claude/.instructions/rules/.scripts/validate-rule.py` (если нужно)
- `.claude/.instructions/skills/.scripts/validate-skill.py` (если нужно)
