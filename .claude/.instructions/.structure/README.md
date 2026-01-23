# Инструкции /.structure/

Правила работы со структурой проекта.

**Ключевое:** SSOT зон ответственности = `/.structure/responsibilities.md`

---

## Оглавление

| Секция | Инструкция | Описание |
|--------|------------|----------|
| [1. Факты](#1-факты-structure) | [facts/](./facts/) | Правила для файлов /.structure/ |
| [2. README папок](#2-readme-папок) | [readme/](./readme/) | Форматы README |
| [3. Флоу](#3-флоу) | [workflows/](./workflows/) | Создание, переименование, удаление |
| [4. Зеркалирование](#4-зеркалирование) | [mirroring.md](./mirroring.md) | Папки проекта ↔ инструкции |
| [5. Примеры](#5-примеры) | [examples.md](./examples.md) | Decision Tree |
| [6. Ссылки](#6-ссылки) | [links/](./links/) | Правила ссылок |

```
/.claude/.instructions/.structure/
├── README.md               # Этот файл (индекс)
├── facts/                  # Правила для /.structure/
│   ├── project.md          #   Формат project.md
│   └── responsibilities.md #   Формат responsibilities.md
├── readme/                 # Форматы README
│   ├── project-folder.md   #   README папки проекта
│   └── instructions-folder.md  # README папки инструкций
├── workflows/              # Флоу действий
│   ├── create-folder.md    #   Создание папки
│   ├── create-file.md      #   Создание файла
│   ├── rename.md           #   Переименование
│   └── delete.md           #   Удаление
├── mirroring.md            # Зеркалирование
├── examples.md             # Примеры
└── links/                  # Правила ссылок
```

---

## Главные правила

### SSOT зон ответственности

```
SSOT = /.structure/responsibilities.md
README папки = копия своей зоны + ссылка на SSOT
```

### Разделение ФАКТЫ / ПРАВИЛА

```
/.structure/                          ← ФАКТЫ (что есть)
/.claude/.instructions/.structure/    ← ПРАВИЛА (как работать)
```

---

# 1. Факты (/.structure/)

Правила формата и обновления файлов в папке `/.structure/`.

**Индекс:** [facts/README.md](./facts/README.md)

---

# 2. README папок

Форматы README для разных типов папок.

| Тип | Инструкция |
|-----|------------|
| Папка проекта | [readme/project-folder.md](./readme/project-folder.md) |
| Папка инструкций | [readme/instructions-folder.md](./readme/instructions-folder.md) |

**Индекс:** [readme/README.md](./readme/README.md)

---

# 3. Флоу

Пошаговые инструкции для действий.

| Действие | Инструкция |
|----------|------------|
| Создание папки | [workflows/create-folder.md](./workflows/create-folder.md) |
| Создание файла | [workflows/create-file.md](./workflows/create-file.md) |
| Переименование | [workflows/rename.md](./workflows/rename.md) |
| Удаление | [workflows/delete.md](./workflows/delete.md) |

**Индекс:** [workflows/README.md](./workflows/README.md)

---

# 4. Зеркалирование

Связь между папками проекта и папками инструкций.

```
/src/  →  /.claude/.instructions/src/
```

**Инструкция:** [mirroring.md](./mirroring.md)

---

# 5. Примеры

Decision Tree: куда положить файл, где написать инструкцию.

**Инструкция:** [examples.md](./examples.md)

---

# 6. Ссылки

Правила работы со ссылками в документах.

**Индекс:** [links/README.md](./links/README.md)

---

# 7. Шаблоны

**Шаблоны для этой области отсутствуют.**

---

# 8. Скиллы

| Скилл | Назначение |
|-------|------------|
| `/links-update` | Обновить ссылки после переименования |
| `/links-delete` | Пометить битые ссылки после удаления |
| `/links-validate` | Проверить все ссылки в проекте |
