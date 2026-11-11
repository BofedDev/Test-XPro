FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements/ requirements/
RUN pip install --no-cache-dir -r requirements/prod.txt

COPY . .

EXPOSE 8000

# Миграции -> сидер -> сервер
CMD ["sh", "-c", "alembic upgrade head && python -m src.seed && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
