from typing import List, Optional

from datetime import datetime, UTC, date

from src.app.application.interfaces.shift_task_repo import IShiftTaskRepository
from src.app.domain.exceptions import DomainError
from src.app.domain.models.shift_task import ShiftTask

class ShiftTaskService:
    def __init__(self, repo: IShiftTaskRepository):
        self._repo = repo

    def create_shift_tasks(self, payloads: List[dict]) -> List[ShiftTask]:
        domain_objects : List[ShiftTask] = []
        for data in payloads:
            try:
                object = ShiftTask(
                    id=None,
                    is_closed=data['is_closed'],
                    task_description=data['task_description'],
                    work_center=data['work_center'],
                    shift=data['shift'],
                    team_name=data['team_name'],
                    batch_id=data['batch_id'],
                    batch_date=data['batch_date'],
                    nomenclature=data['nomenclature'],
                    ekn_code=data['ekn_code'],
                    rc_id=data['rc_id'],
                    shift_start=data['shift_start'],
                    shift_end=data['shift_end']
                )
            except DomainError as exception:
                raise DomainError(f"Неверные данные ShiftTask: {exception}")
            domain_objects.append(object)

        saved = self._repo.add_many(domain_objects)
        return saved

    def list_all(self, * ,
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
                 limit: int = 100) -> List[ShiftTask]:
        return self._repo.list_all(
            is_closed=is_closed,
            batch_id=batch_id,
            batch_date=batch_date,
            work_center=work_center,
            shift=shift,
            team_name=team_name,
            nomenclature=nomenclature,
            ekn_code=ekn_code,
            rc_id=rc_id,
            shift_start=shift_start,
            shift_end=shift_end,
            skip=skip,
            limit=limit,
        )

    def get_shift_task(self, task_id: int = 0):
        task = self._repo.get(task_id)
        if task is None:
            raise DomainError(f"ShiftTask с task_id = {task_id} не найден.")
        return task

    def update_shift_task(self, task_id: int, updates: dict) -> ShiftTask:
        task = self.get_shift_task(task_id)

        if "is_closed" in updates:
            is_closed = updates["is_closed"]
            updates["closed_at"] = datetime.now(UTC) if is_closed else None

        return self._repo.update(task_id, updates)
