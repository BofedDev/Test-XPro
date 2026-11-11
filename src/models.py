"""Единая точка импорта всех моделей (нужна для Alembic и сидера)."""
from src.database import Base  # noqa: F401
from src.categories.models import Category  # noqa: F401
from src.products.models import Product  # noqa: F401
