from typing import List, Optional
from datetime import datetime, date

from sqlalchemy.orm import Session
from sqlalchemy import  Column, Integer, String, Boolean, Date, DateTime
from sqlalchemy import and_

from src.app.application.interfaces.shift_task_repo import IShiftTaskRepository
from src.app.domain.models.shift_task import ShiftTask as DomainShiftTask
from src.app.infrastructure.db.base import Base

class ShiftTaskORM(Base):
    __tablename__ = "shift_tasks"

    id = Column(Integer, primary_key=True, index=True)
    is_closed = Column(Boolean, index=True, default=False, nullable=False)
    task_description = Column(String, nullable=False)
    work_center = Column(String, nullable=False)
    shift = Column(String, nullable=False)
    team_name = Column(String, nullable=False)
    batch_id = Column(Integer, nullable=False)
    batch_date = Column(Date, nullable=False)
    nomenclature = Column(String, nullable=False)
    ekn_code = Column(Integer, nullable=False)
    rc_id = Column(Integer, nullable=False)
    shift_start = Column(DateTime, nullable=False)
    shift_end = Column(DateTime, nullable=False)

    def to_domain(self) -> DomainShiftTask:
        return DomainShiftTask(
            id=self.id,
            is_closed=self.is_closed,
            task_description=self.task_description,
            work_center=self.work_center,
            shift=self.shift,
            team_name=self.team_name,
            batch_id=self.batch_id,
            batch_date=self.batch_date,
            nomenclature=self.nomenclature,
            ekn_code=self.ekn_code,
            rc_id=self.rc_id,
            shift_start=self.shift_start,
            shift_end=self.shift_end,
        )


class ShiftTaskRepositorySQLAlchemy(IShiftTaskRepository):
    def __init__(self, db_session: Session):
        self._db = db_session

    def add_many(self, tasks: List[DomainShiftTask]) -> List[DomainShiftTask]:
        orm_objects = []
        for task in tasks:
            orm = ShiftTaskORM(
                is_closed=task.is_closed,
                task_description=task.task_description,
                work_center=task.work_center,
                shift=task.shift,
                team_name=task.team_name,
                batch_id=task.batch_id,
                batch_date=task.batch_date,
                nomenclature=task.nomenclature,
                ekn_code=task.ekn_code,
                rc_id=task.rc_id,
                shift_start=task.shift_start,
                shift_end=task.shift_end,
            )
            self._db.add(orm)
            orm_objects.append(orm)


        self._db.commit()
        for orm in orm_objects:
            self._db.refresh(orm)

        return [orm.to_domain() for orm in orm_objects]


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
                 limit: int = 100) -> List[DomainShiftTask]:
        query = self._db.query(ShiftTaskORM)
        filter_map = {
            "is_closed": ShiftTaskORM.is_closed,
            "batch_id": ShiftTaskORM.batch_id,
            "batch_date": ShiftTaskORM.batch_date,
            "work_center": ShiftTaskORM.work_center,
            "shift": ShiftTaskORM.shift,
            "team_name": ShiftTaskORM.team_name,
            "nomenclature": ShiftTaskORM.nomenclature,
            "ekn_code": ShiftTaskORM.ekn_code,
            "rc_id": ShiftTaskORM.rc_id,
            "shift_start": ShiftTaskORM.shift_start,
            "shift_end": ShiftTaskORM.shift_end,
        }
        filters = []
        for attr_name, column in filter_map.items():
            value = locals().get(attr_name)
            if value is not None:
                filters.append(column == value)

        if filters:
            query = query.filter(and_(*filters))

        rows = query.offset(skip).limit(limit).all()
        return [row.to_domain() for row in rows]

    def get(self, task_id: int) -> Optional[DomainShiftTask]:
        orm : ShiftTaskORM = self._db.query(ShiftTaskORM).filter(ShiftTaskORM.id == task_id).first()
        return orm.to_domain() if orm else None

    def update(self, task_id: int, updates: dict) -> DomainShiftTask:
        orm : ShiftTaskORM = self._db.query(ShiftTaskORM).filter(ShiftTaskORM.id == task_id).first()

        for key, value in updates.items():
            setattr(orm, key, value)

        self._db.commit()
        self._db.refresh(orm)

        return orm.to_domain()
