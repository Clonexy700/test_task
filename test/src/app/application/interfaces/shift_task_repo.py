from abc import ABC, abstractmethod
from typing import List, Optional

from datetime import date, datetime

from src.app.domain.models.shift_task import ShiftTask

class IShiftTaskRepository(ABC):
    @abstractmethod
    def add_many(self, tasks: List[ShiftTask]) -> List[ShiftTask]:
        raise NotImplementedError

    @abstractmethod
    def list_all(self, *,
                 is_closed: Optional[bool] = None,
                 batch_id: Optional[int] = None,
                 batch_date: Optional[date] = None,
                 work_center: Optional[str] = None,
                 shift: Optional[str] = None,
                 team_name: Optional[str] = None,
                 nomenclature: Optional[str] = None,
                 ekn_code: Optional[int] = None,
                 rc_id: Optional[int] = None,
                 shift_start: Optional[datetime] = None,
                 shift_end: Optional[datetime] = None,
                 skip: int = 0,
                 limit: int = 100
                 ) -> List[ShiftTask]:
        raise NotImplementedError

    @abstractmethod
    def get(self, task_id: int) -> Optional[ShiftTask]:
        raise NotImplementedError

    @abstractmethod
    def update(self, task_id: int, updates: dict) -> ShiftTask:
        raise NotImplementedError
