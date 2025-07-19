from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

class ProductCreate(BaseModel):
    unique_code: str = Field(..., description="Уникальный код продукта")
    batch_id: int = Field(..., description="Дата партии")
    batch_date: date = Field(..., description="Дата партии")

class ProductAggregateRequest(BaseModel):
    batch_pk: int = Field(..., description="Номер партии (shift_task.id)")
    unique_code: str = Field(..., description="Уникальный код продукта")

class ProductAggregateResponse(BaseModel):
    unique_code: str = Field(..., description="Уникальный код продукта после агрегации")


class ProductRead(BaseModel):
    id: int = Field(..., description="Идентификатор продукта")
    unique_code: str = Field(..., description="Уникальный код продукта")
    batch_id: int = Field(..., description="Номер партии")
    is_aggregated: bool = Field(..., description="Агрегирован ли продукт")
    aggregated_at: Optional[datetime] = Field(..., description="Дата агрегации продукта")

    class Config:
        orm_mode = True
