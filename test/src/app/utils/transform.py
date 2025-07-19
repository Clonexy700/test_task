from typing import List

from src.app.domain.models.shift_task import ShiftTask as DomainShiftTask

from src.app.presentation.v1.schemas.shift_task import ShiftTaskRead

def domain_to_read(domain_obj: DomainShiftTask) -> ShiftTaskRead:
    return ShiftTaskRead(
        id=domain_obj.id,
        is_closed=domain_obj.is_closed,
        task_description=domain_obj.task_description,
        work_center=domain_obj.work_center,
        shift=domain_obj.shift,
        team_name=domain_obj.team_name,
        batch_id=domain_obj.batch_id,
        batch_date=domain_obj.batch_date,
        nomenclature=domain_obj.nomenclature,
        ekn_code=domain_obj.ekn_code,
        rc_id=domain_obj.rc_id,
        shift_start=domain_obj.shift_start,
        shift_end=domain_obj.shift_end,
    )

def domains_to_read_list(domains: List[DomainShiftTask]) -> List[ShiftTaskRead]:
    return [domain_to_read(obj) for obj in domains]