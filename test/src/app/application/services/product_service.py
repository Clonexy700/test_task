from typing import List, Dict
from datetime import datetime, timezone

from src.app.application.interfaces.product_repo import IProductRepository
from src.app.application.interfaces.shift_task_repo import IShiftTaskRepository
from src.app.domain.models.product import Product
from src.app.domain.exceptions import DomainError

class ProductsService:
    def __init__(self, product_repo: IProductRepository,
                 shift_task_repo: IShiftTaskRepository):
        self._product_repo = product_repo
        self._shift_task_repo = shift_task_repo


    def create_products(self, payloads: List[Dict]) -> List[Product]:
        domain_objects = []
        for data in payloads:
            code = data['unique_code']
            bid = data['batch_id']
            bdate = data['batch_date']

            exists = self._shift_task_repo.list_all(
                batch_id=bid, batch_date=bdate, limit=1
            )

            if not exists:
                continue

            domain_object = Product(
                id=None,
                unique_code=code,
                batch_id=bid,
                is_aggregated=False,
                aggregated_at=None
            )
            domain_objects.append(domain_object)

        if not  domain_objects:
            return []

        saved = self._product_repo.add_many(domain_objects)
        return saved

    def aggregate_product(self, batch_pk: int, unique_code: str) -> Product:
        product = self._product_repo.get_by_code(unique_code)
        if not product:
            raise DomainError("Product not found")

        if product.batch_id != batch_pk:
            raise DomainError("Batch id mismatch")

        if product.is_aggregated:
            at = product.aggregated_at.isoformat() if product.aggregated_at else ""
            raise DomainError(f"Product has already been aggregated at: {at}")

        now = datetime.now(timezone.utc)

        updates = {
            "is_aggregated": True,
            "aggregated_at": now,
        }

        updated = self._product_repo.update_by_id(product.id, updates)
        return updated