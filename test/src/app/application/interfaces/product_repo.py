from abc import ABC, abstractmethod
from typing import List, Optional

from datetime import datetime

from src.app.domain.models.product import Product

class IProductRepository(ABC):
    @abstractmethod
    def add_many(self, product: List[Product]) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_by_code(self, unique_code: str) -> Optional[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, product_id: int) -> Optional[Product]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self, skip: int = 0, limit: int = 100) -> List[Product]:
        raise NotImplementedError

    @abstractmethod
    def update_by_id(self, product_id: int, updates: dict) -> Product:
        raise NotImplementedError



