from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=255, description="Название категории")
    description: Optional[str] = Field(None, description="Описание")
    parent_category_id: int = Field(0, description="ID родительской категории (0 если корневая)")
    seo_keyword: Optional[str] = Field(None, max_length=255)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None)
    meta_keyword: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None, max_length=255)
    status: int = Field(1, description="Статус: 1 - включена, 0 - выключена")


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)
    parent_category_id: Optional[int] = Field(None)
    seo_keyword: Optional[str] = Field(None, max_length=255)
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = Field(None)
    meta_keyword: Optional[str] = Field(None, max_length=255)
    image: Optional[str] = Field(None, max_length=255)
    status: Optional[int] = Field(None)


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    category_id: int
    date_added: datetime
    date_modify: datetime
