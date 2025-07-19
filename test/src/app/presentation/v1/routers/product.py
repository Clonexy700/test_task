from typing import List
from datetime import time, datetime, date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.app.presentation.v1.schemas.product import (
    ProductRead,
    ProductCreate,
    ProductAggregateResponse,
    ProductAggregateRequest,
)
from src.app.infrastructure.db.session import get_bd
from src.app.infrastructure.db.repositories.product_repo_sqlalchemy import ProductRepositorySQLAlchemy
from src.app.infrastructure.db.repositories.shift_task_repo_sqlalchemy import ShiftTaskRepositorySQLAlchemy
from src.app.application.services.product_service import ProductsService
from src.app.domain.exceptions import DomainError
from src.app.utils.transform import domain_to_read, domains_to_read_list

router = APIRouter(tags=["Products"])

@router.post("/",
             response_model=List[ProductRead],
             status_code=status.HTTP_201_CREATED
             )
def create_products(
        items: List[ProductCreate],
        db: Session = Depends(get_bd)
):
    shift_task_repo = ShiftTaskRepositorySQLAlchemy(db)
    product_repo = ProductRepositorySQLAlchemy(db)
    service = ProductsService(product_repo, shift_task_repo)

    payloads = [item.model_dump() for item in items]
    try:
        created = service.create_products(payloads)
    except DomainError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return created

@router.post(
    "/aggregate",
    response_model=ProductAggregateResponse,
    status_code=status.HTTP_200_OK,
)
def aggregate_product(
        request: ProductAggregateRequest,
        db: Session = Depends(get_bd),
):
    product_repo = ProductRepositorySQLAlchemy(db)
    shift_task_repo = ShiftTaskRepositorySQLAlchemy(db)
    service = ProductsService(product_repo, shift_task_repo)

    try:
        updated = service.aggregate_product(request.batch_pk, request.unique_code)
    except DomainError as e:
        msg = str(e)
        if msg == "Product not found":
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        if msg == "Batch id mismatch":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unique code is attached to another batch",
            )
        if msg.startswith("Product has already been aggregated at:"):
            at = msg.split(":", 1)[1]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product unique code already used at {at}",
            )
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    return ProductAggregateResponse(unique_code=updated.unique_code)