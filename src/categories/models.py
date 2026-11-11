from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from src.database import Base


def _now():
    return datetime.now(timezone.utc)


class Category(Base):
    __tablename__ = "category"

    category_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    parent_category_id = Column(Integer, default=0, nullable=False, index=True)
    seo_keyword = Column(String(255), nullable=True)
    meta_title = Column(String(255), nullable=True)
    meta_description = Column(Text, nullable=True)
    meta_keyword = Column(String(255), nullable=True)
    image = Column(String(255), nullable=True)
    status = Column(Integer, default=1, nullable=False)
    date_added = Column(DateTime, default=_now, nullable=False)
    date_modify = Column(DateTime, default=_now, onupdate=_now, nullable=False)
