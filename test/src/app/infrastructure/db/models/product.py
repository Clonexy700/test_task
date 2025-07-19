from sqlalchemy import Column, Integer, String, Boolean, DateTime
from src.app.infrastructure.db.base import Base
from src.app.domain.models.product import Product as DomainProduct


class ProductORM(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    unique_code = Column(String, unique=True, nullable=False, index=True)
    batch_id = Column(Integer, nullable=False, index=True)
    is_aggregated = Column(Boolean, nullable=False, default=False)
    aggregated_at = Column(DateTime, nullable=True)


    def to_domain(self) -> DomainProduct:
        return DomainProduct(
            id=self.id,
            unique_code=self.unique_code,
            batch_id=self.batch_id,
            is_aggregated=self.is_aggregated,
            aggregated_at=self.aggregated_at
        )
