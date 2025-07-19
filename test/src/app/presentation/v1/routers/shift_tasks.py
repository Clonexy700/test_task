from typing import List, Optional
from datetime import datetime, date

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from src.app.presentation.v1.schemas.shift_task import ShiftTaskCreate, ShiftTaskRead, ShiftTaskUpdate
from src.app.infrastructure.db.session import get_bd
from src.app.infrastructure.db.repositories.shift_task_repo_sqlalchemy import ShiftTaskRepositorySQLAlchemy
from src.app.application.services.shift_task_service import ShiftTaskService
from src.app.domain.exceptions import DomainError
from src.app.utils.transform import domain_to_read, domains_to_read_list

router = APIRouter(tags=["Shift Tasks"])

@router.post(
    "/",
    response_model=List[ShiftTaskRead],
    status_code=status.HTTP_201_CREATED
)
def create_shift_tasks(
        tasks_in: List[ShiftTaskCreate],
        db: Session = Depends(get_bd)
):
    repo = ShiftTaskRepositorySQLAlchemy(db)
    service = ShiftTaskService(repo)

    tasks_data = [task.model_dump() for task in tasks_in]

    try:
        created_objects = service.create_shift_tasks(tasks_data)
    except DomainError as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

    return domains_to_read_list(created_objects)

@router.get("/{task_id}",
            response_model=ShiftTaskRead,
            status_code=status.HTTP_200_OK
           )
def get_shift_task_by_id(task_id: int, db: Session = Depends(get_bd)):
    repo = ShiftTaskRepositorySQLAlchemy(db)
    service = ShiftTaskService(repo)

    try:
        dom = service.get_shift_task(task_id)
    except DomainError as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))

    return domain_to_read(dom)

@router.get("/",
            response_model=List[ShiftTaskRead],
            status_code=status.HTTP_200_OK)
def get_shift_tasks(
        is_closed: Optional[bool] = Query(None, description="Фильтр по статусу закрытия: true/false"),
        batch_id: Optional[int] = Query(None, description="Фильтр по номеру партии"),
        batch_date: Optional[date] = Query(None, description="Фильтр по дате партии (YYYY-MM-DD)"),
        work_center: Optional[str] = Query(None, description="Фильтр по рабочему центру"),
        shift: Optional[str] = Query(None, description="Фильтр по смене (например, 'morning')"),
        team_name: Optional[str] = Query(None, description="Фильтр по названию бригады"),
        nomenclature: Optional[str] = Query(None, description="Фильтр по номенклатуре"),
        ekn_code: Optional[int] = Query(None, description="Фильтр по коду ЕКН"),
        rc_id: Optional[int] = Query(None, description="Фильтр по идентификатору РЦ"),
        shift_start: Optional[datetime] = Query(None, description="Фильтр по дате-времени начала"),
        shift_end: Optional[datetime] = Query(None, description="Фильтр по дате-времени конца"),
        skip: int = Query(0, ge=0, description="Смещение (offset)"),
        limit: int = Query(100, ge=1, le=1000, description="Лимит записей (limit)"),
        db: Session = Depends(get_bd),
):
    repo = ShiftTaskRepositorySQLAlchemy(db)
    service = ShiftTaskService(repo)
    try:
        tasks = service.list_all(
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
    except DomainError as exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exception))

    return domains_to_read_list(tasks)

@router.patch("/{task_id}",
              response_model=ShiftTaskRead,
              status_code=status.HTTP_200_OK)
def update_shift_task(
        task_id: int,
        task_in: ShiftTaskUpdate,
        db: Session = Depends(get_bd)
):
    repo = ShiftTaskRepositorySQLAlchemy(db)
    service = ShiftTaskService(repo)

    updates = task_in.model_dump(exclude_unset=True)

    try:
        dom = service.update_shift_task(task_id, updates)
    except DomainError as exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exception))

    return domain_to_read(dom)