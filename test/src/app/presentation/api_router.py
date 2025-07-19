from fastapi import APIRouter
from src.app.presentation.v1.routers import shift_tasks
from src.app.presentation.v1.routers import product

api_router = APIRouter()
api_router.include_router(shift_tasks.router, prefix="/api/v1/shift-tasks", tags=["Shift Tasks"])
api_router.include_router(product.router, prefix="/api/v1/products", tags=["Products"])
