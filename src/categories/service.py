from sqlalchemy.orm import Session

from src.categories.models import Category
from src.categories.schemas import CategoryCreate, CategoryUpdate
from src.exceptions import ConflictError, RelatedObjectNotFound


class CategoryService:
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100):
        return (
            db.query(Category)
            .order_by(Category.category_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_by_id(db: Session, category_id: int):
        return db.get(Category, category_id)

    @staticmethod
    def _check_parent(db: Session, parent_id: int | None, own_id: int | None = None):
        if not parent_id:  # None или 0 — корневая категория
            return
        if own_id is not None and parent_id == own_id:
            raise ConflictError("Категория не может быть родителем самой себя")
        if db.get(Category, parent_id) is None:
            raise RelatedObjectNotFound(f"Родительская категория {parent_id} не найдена")

    @staticmethod
    def create(db: Session, data: CategoryCreate):
        CategoryService._check_parent(db, data.parent_category_id)
        db_category = Category(**data.model_dump())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def update(db: Session, category_id: int, data: CategoryUpdate):
        db_category = CategoryService.get_by_id(db, category_id)
        if not db_category:
            return None

        update_data = data.model_dump(exclude_unset=True)
        if "parent_category_id" in update_data:
            if update_data["parent_category_id"] is None:
                update_data["parent_category_id"] = 0
            CategoryService._check_parent(
                db, update_data["parent_category_id"], own_id=category_id
            )
        for key, value in update_data.items():
            setattr(db_category, key, value)

        db.commit()
        db.refresh(db_category)
        return db_category

    @staticmethod
    def delete(db: Session, category_id: int):
        db_category = CategoryService.get_by_id(db, category_id)
        if not db_category:
            return None
        has_children = (
            db.query(Category.category_id)
            .filter(Category.parent_category_id == category_id)
            .first()
        )
        if has_children:
            raise ConflictError("Нельзя удалить категорию, у которой есть подкатегории")
        db.delete(db_category)
        db.commit()
        return db_category
