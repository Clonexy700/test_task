from typing import List, Optional
from sqlalchemy.orm import Session

from src.app.application.interfaces.product_repo import IProductRepository
from src.app.domain.models.product import Product as DomainProduct, Product
from src.app.infrastructure.db.models.product import ProductORM

class ProductRepositorySQLAlchemy(IProductRepository):
    def __init__(self, db_session: Session):
        self._db = db_session

    def add_many(self, products: List[DomainProduct]) -> List[DomainProduct]:
        orm_objects = []
        for product in products:
            orm = ProductORM(
                unique_code=product.unique_code,
                batch_id=product.batch_id,
                is_aggregated=product.is_aggregated,
                aggregated_at=product.aggregated_at
            )
            self._db.add(orm)
            orm_objects.append(orm)

        self._db.commit()
        for orm in orm_objects:
            self._db.refresh(orm)

        return [orm.to_domain() for orm in orm_objects]


    def get_by_code(self, unique_code: str) -> Optional[DomainProduct]:
        row = (
            self._db.query(ProductORM)
            .filter(ProductORM.unique_code == unique_code)
            .first()
        )
        return row.to_domain() if row else None

    def get_by_id(self, product_id: int) -> Optional[DomainProduct]:
        row = self._db.query(ProductORM).get(product_id)
        return row.to_domain() if row else None

    def list_all(self, skip: int = 0, limit: int = 100) -> List[DomainProduct]:
        rows = self._db.query(ProductORM).offset(skip).limit(limit).all()
        return [row.to_domain() for row in rows]

    def update_by_id(self, product_id: int, updates: dict) -> Product:
        orm = self._db.query(ProductORM).get(product_id)
        if not orm:
            raise ValueError(f"Product {product_id} not found")
        for key, value in updates.items():
            setattr(orm, key, value)
        self._db.commit()
        self._db.refresh(orm)
        return orm.to_domain()