# FastAPI Store Management API

REST API для управления категориями товаров и продуктами: миграции Alembic, автоматический сидер демо-данных, Docker.

## Стек

- Python 3.11+
- FastAPI, Pydantic v2
- SQLAlchemy 2 (SQLite локально / MySQL в Docker)
- Alembic
- Docker & Docker Compose

## Запуск через Docker

```bash
cp .env.example .env      # задайте свои пароли
docker compose up --build
```

При старте контейнер выполняет `alembic upgrade head`, затем сидер `src/seed.py`, затем запускает сервер.

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Порт MySQL наружу не публикуется, БД доступна только приложению.

## Локальный запуск (SQLite, без Docker)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .\.venv\Scripts\activate
pip install -r requirements/dev.txt
cp .env.example .env             # по умолчанию SQLite: shop.db
alembic upgrade head             # создать таблицы
python -m src.seed               # демо-данные (необязательно)
uvicorn src.main:app --reload
```

## Тесты

```bash
pip install -r requirements/dev.txt
pytest
```

## Миграции

```bash
alembic revision --autogenerate -m "описание"
alembic upgrade head
```

## Структура проекта

```text
├── migrations/        # Alembic (env.py, versions/)
├── requirements/      # base.txt, dev.txt, prod.txt
├── src/
│   ├── categories/    # модель, схемы, сервис, роутер
│   ├── products/      # модель, схемы, сервис, роутер
│   ├── config.py      # настройки из .env
│   ├── database.py    # engine, сессия, Base
│   ├── exceptions.py  # доменные ошибки и их обработчики
│   ├── models.py      # единая точка импорта моделей
│   ├── main.py        # точка входа FastAPI
│   └── seed.py        # сидер демо-данных
├── tests/             # pytest
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
└── .env.example
```

## Основные эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| GET/POST | `/categories/` | список / создание категории |
| GET/PUT/DELETE | `/categories/{id}` | категория по id |
| GET/POST | `/products/` | список (фильтр `?category_id=`) / создание товара |
| GET/PUT/DELETE | `/products/{id}` | товар по id |
| GET | `/health` | проверка работоспособности |

Правила: товар нельзя привязать к несуществующей категории (400); нельзя удалить категорию с подкатегориями (409); при удалении категории у её товаров `category_id` становится `NULL`.
