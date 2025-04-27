# 🚀 TSM Bank Project

Банковский асинхронный API на FastAPI, поддерживающий операции с клиентами, счетами, карточками, кредитами и платежами.

Проект находится в активной разработке. В ближайших обновлениях планируется реализация JWT авторизации с Access и Refresh токенами.

---

## 📚 Оглавление

- [Описание](#описание)
- [Технологии](#технологии)
- [Установка](#установка)
- [Запуск проекта](#запуск-проекта)
- [Переменные окружения](#переменные-окружения)
- [Структура проекта](#структура-проекта)
- [Планы на будущее](#планы-на-будущее)
- [Документация API](#документация-api)

---

## 📖 Описание

Этот проект имитирует базовые функции банковской системы:

- Работа с клиентами (`clients`)
- Работа со счетами (`accounts`)
- Работа с кредитами (`loans`)
- Работа с картами (`cards`)
- Переводы между счетами (`transactions`)
- Оплата кредитов (`payments`)

---

## ⚙️ Технологии

- Python 3.10+
- FastAPI
- SQLAlchemy 2.0
- Alembic
- PostgreSQL
- Pydantic 2
- Будет добавлено: PyJWT, bcrypt (для авторизации)

---

## 💻 Установка

```bash
git clone https://github.com/your_username/your_repo.git
cd your_repo
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 🚀 Запуск проекта

# Выполнить миграции
```bash
alembic upgrade head
```
# Запустить сервер
```bash
uvicorn src.main:app --reload
```

## 🔑 Переменные окружения

# Создай .env файл в корне проекта со следующим содержанием:
``` .env
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_db_user
DB_PASS=your_db_password
DB_NAME=your_db_name
```


## 📁 Структура проекта
# Так выглядить текущая структура проекта
```
.
├── alembic.ini
├── sql_scripts/
│   ├── drop_tables.sql
│   └── sync_sequences.sql
└── src/
    ├── api/
    │   └── v1/
    │       ├── accounts.py
    │       ├── cards.py
    │       ├── clients.py
    │       ├── loans.py
    │       ├── payments.py
    │       └── transactions.py
    ├── config.py
    ├── database.py
    ├── main.py
    ├── migrations/
    │   ├── env.py
    │   └── versions/
    │       ├── create_tables.py
    │       └── fill_tables.py
    ├── models/
    │   ├── accounts.py
    │   ├── cards.py
    │   ├── clients.py
    │   ├── loans.py
    │   ├── payments.py
    │   └── transactions.py
    ├── schemas/
    │   └── v1/
    │       ├── base.py
    │       └── schemas.py
    ├── services/
    │   └── account_service.py
    └── swagger/
        └── tags_metadata.py
```
 
## 🚀 Планы на будущее

    Реализация JWT авторизации (Access и Refresh токены)

    Защита эндпоинтов через OAuth2 Password Bearer

    Рефакторинг сервисного слоя

    Добавление автоматических тестов (pytest + httpx)

    Разворачивание на Render или Railway

## 📄 Документация API

# После запуска проекта:

    Swagger UI: http://localhost:8000/docs

    ReDoc: http://localhost:8000/redoc

## 🔥 Контакты

    GitHub: Belous

    Email: kbelous2022@gmail.com
