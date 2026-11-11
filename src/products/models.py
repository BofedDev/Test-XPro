from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from src.database import Base


def _now():
    return datetime.now(timezone.utc)


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    sku = Column(String(100), nullable=True, index=True)
    model = Column(String(64), nullable=True)
    quantity = Column(Integer, default=0, nullable=False)
    price = Column(Numeric(15, 4), default=0, nullable=False)
    image = Column(String(255), nullable=True)
    category_id = Column(
        Integer,
        ForeignKey("category.category_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    status = Column(Integer, default=1, nullable=False)
    date_added = Column(DateTime, default=_now, nullable=False)
    date_modify = Column(DateTime, default=_now, onupdate=_now, nullable=False)

    category = relationship("Category", backref="products")
