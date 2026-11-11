from decimal import Decimal

from src.database import SessionLocal
from src.models import Category, Product


def seed_db() -> None:
    db = SessionLocal()
    try:
        if db.query(Category).first():
            print("База данных уже содержит данные, сидер пропущен.")
            return

        electronics = Category(
            name="Электроника", description="Гаджеты и техника", parent_category_id=0
        )
        db.add(electronics)
        db.flush()

        smartphones = Category(
            name="Смартфоны",
            description="Мобильные телефоны",
            parent_category_id=electronics.category_id,
        )
        db.add(smartphones)
        db.flush()

        db.add(
            Product(
                name="iPhone 15",
                description="Флагманский смартфон",
                sku="IPH-15",
                price=Decimal("999.99"),
                quantity=10,
                category_id=smartphones.category_id,
            )
        )
        db.commit()
        print("База данных успешно наполнена демо-данными!")
    finally:
        db.close()


if __name__ == "__main__":
    seed_db()
