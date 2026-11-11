from sqlalchemy.orm import Session

from src.categories.models import Category
from src.exceptions import RelatedObjectNotFound
from src.products.models import Product
from src.products.schemas import ProductCreate, ProductUpdate


class ProductService:
    @staticmethod
    def get_all(
        db: Session, skip: int = 0, limit: int = 100, category_id: int | None = None
    ):
        query = db.query(Product)
        if category_id is not None:
            query = query.filter(Product.category_id == category_id)
        return query.order_by(Product.product_id).offset(skip).limit(limit).all()

    @staticmethod
    def get_by_id(db: Session, product_id: int):
        return db.get(Product, product_id)

    @staticmethod
    def _check_category(db: Session, category_id: int | None):
        if category_id is not None and db.get(Category, category_id) is None:
            raise RelatedObjectNotFound(f"Категория {category_id} не найдена")

    @staticmethod
    def create(db: Session, data: ProductCreate):
        ProductService._check_category(db, data.category_id)
        db_product = Product(**data.model_dump())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def update(db: Session, product_id: int, data: ProductUpdate):
        db_product = ProductService.get_by_id(db, product_id)
        if not db_product:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "category_id" in update_data:
            ProductService._check_category(db, update_data["category_id"])
        for key, value in update_data.items():
            setattr(db_product, key, value)

        db.commit()
        db.refresh(db_product)
        return db_product

    @staticmethod
    def delete(db: Session, product_id: int):
        db_product = ProductService.get_by_id(db, product_id)
        if not db_product:
            return None
        db.delete(db_product)
        db.commit()
        return db_product
