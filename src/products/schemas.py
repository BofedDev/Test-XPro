from datetime import datetime
from typing import Optional
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., max_length=255, description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    sku: Optional[str] = Field(None, max_length=100, description="Артикул")
    model: Optional[str] = Field(None, max_length=64, description="Модель")
    price: Decimal = Field(..., ge=0, description="Цена")
    quantity: int = Field(0, ge=0, description="Количество на складе")
    image: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = Field(None, description="ID категории")
    status: int = Field(1, description="Статус: 1 - включен, 0 - выключен")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None)
    sku: Optional[str] = Field(None, max_length=100)
    model: Optional[str] = Field(None, max_length=64)
    price: Optional[Decimal] = Field(None, ge=0)
    quantity: Optional[int] = Field(None, ge=0)
    image: Optional[str] = Field(None, max_length=255)
    category_id: Optional[int] = Field(None)
    status: Optional[int] = Field(None)


class ProductResponse(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    product_id: int
    date_added: datetime
    date_modify: datetime