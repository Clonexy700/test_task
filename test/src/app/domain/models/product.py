from typing import Optional
from datetime import datetime

class Product:
    def __init__(self,
                 id: Optional[int],
                 unique_code: str,
                 batch_id: int,
                 is_aggregated: bool = False,
                 aggregated_at: Optional[datetime] = None
                 ):
        self.id = id
        self.unique_code = unique_code
        self.batch_id = batch_id
        self.is_aggregated = is_aggregated
        self.aggregated_at = aggregated_at
