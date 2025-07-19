from typing import Optional
from datetime import date, datetime
from src.app.domain.exceptions import DomainError

class ShiftTask:
    def __init__(self, id: Optional[int], is_closed: bool,
                 task_description: str, work_center: str,
                 shift: str, team_name: str, batch_id: int,
                 batch_date: date, nomenclature: str, ekn_code: int,
                 rc_id: int, shift_start: datetime, shift_end: datetime):
        self.id = id
        self.is_closed = is_closed
        self.task_description = task_description
        self.work_center = work_center
        self.shift = shift
        self.team_name = team_name
        self.batch_id = batch_id
        self.batch_date = batch_date
        self.nomenclature = nomenclature
        self.ekn_code = ekn_code
        self.rc_id = rc_id
        self.shift_start = shift_start
        self.shift_end = shift_end

        self._validate_times()

    def _validate_times(self):
        if self.shift_start >= self.shift_end:
            raise DomainError("Начало смены должно начинаться до её окончания")

    def close(self):
        if self.is_closed:
            raise DomainError("Задания смены уже было закрыто")
        self.is_closed = True



