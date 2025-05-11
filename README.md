# 💳 TSMBank API

TSMBank — это асинхронный REST API банковской системы, построенный на FastAPI с PostgreSQL, Alembic, JWT-аутентификацией и кастомной логикой баланса.

---

## 📦 Зависимости

Проект использует:

- **FastAPI** — асинхронный web-фреймворк
- **SQLAlchemy** (async) — ORM
- **Alembic** — миграции базы данных
- **asyncpg** — асинхронный драйвер PostgreSQL
- **python-jose** — работа с JWT токенами
- **passlib** — хэширование паролей
- **Pydantic** — валидация схем
- **dotenv** — загрузка переменных из `.env`

---

## ⚙️ Структура проекта

```
tsmbank/
├── src/
│   ├── api/v1/         # Версионированные маршруты
│   ├── models/         # SQLAlchemy модели
│   ├── schemas/        # Pydantic схемы
│   ├── services/       # Бизнес-логика
│   ├── migrations/     # Alembic миграции
│   ├── database.py     # Асинхронная сессия
│   ├── config.py       # Загрузка конфигураций из .env
│   └── main.py         # Точка входа
├── requirements.txt    # Зависимости проекта
└── alembic.ini         # Конфигурация Alembic
```

---

## 🚀 Запуск (без Docker)

### 1. Установите зависимости:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Настройте `.env` в корне проекта:

Пример:

```env
DB_URL=postgresql+asyncpg://user:password@localhost:5432/tsmbank
SECRET_KEY=supersecret
ALGORITHM=RS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_MINUTES=1440
PUBLIC_KEY_PATH=keys/public.pem
PRIVATE_KEY_PATH=keys/private.pem
```

### 3. Примените миграции:

```bash
alembic upgrade head
```

### 4. Запустите сервер:

```bash
python -m src.main
```

---

## 🧪 Миграции Alembic

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
```

---

## 🔐 Авторизация

- `POST /api/v1/auth/login` — получение access/refresh токена
- `POST /api/v1/auth/refresh` — обновление access токена
- `GET /api/v1/clients/me` — получить текущего клиента (защищённый маршрут)

---

## 📒 Возможности

- Управление клиентами, аккаунтами, картами, транзакциями
- Ограничение доступа: клиент может управлять только своими ресурсами
- Автоматическое обновление баланса аккаунта при изменении карточных операций
- Проверка токенов по `exp`
- Разделение access/refresh с RSA-шифрованием

---

## 🛠 SQL Scripts

- `sql_scripts/drop_tables.sql` — удалить все таблицы
- `sql_scripts/sync_sequences.sql` — синхронизация последовательностей

---

## 📫 Автор

TSMBank API — разработан как учебный проект с прицелом на продакшн-практики.