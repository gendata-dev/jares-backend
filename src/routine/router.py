from fastapi import APIRouter

from src.database import DbSession
from src.schema import GenericResponse

router = APIRouter()
"""BASE_URL/routine-management"""


@router.get("/routines", response_model=GenericResponse[list])
async def get_routines(db_session: DbSession):
    """루틴 리스트 조회"""
    return GenericResponse.create(items=[])


@router.post("/routines", response_model=GenericResponse[list])
async def create_routines(db_session: DbSession):
    """루틴 리스트 생성"""
    return GenericResponse.create(items=[])


@router.delete("/routines", response_model=GenericResponse[list])
async def delete_routines(db_session: DbSession):
    """루틴 리스트 삭제"""
    return GenericResponse.create(items=[])


@router.get("/routines/{routine_id}", response_model=GenericResponse[list])
async def get_routine(routine_id: int, db_session: DbSession):
    """루틴 조회"""
    return GenericResponse.create(items=[])


@router.put("/routines/{routine_id}", response_model=GenericResponse[list])
async def update_routine(routine_id: int, db_session: DbSession):
    """루틴 수정"""
    return GenericResponse.create(items=[])
