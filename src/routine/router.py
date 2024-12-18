from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import RoutineRead, RoutineCreate, RoutineDelete
from .service import get, get_all, create, update, delete

router = APIRouter()
"""BASE_URL/routine-management"""


@router.get("/routines/{routine_id}", response_model=GenericResponse[RoutineRead])
def get_routine(routine_id: PrimaryKey, db_session: DbSession):
    """루틴 조회"""
    routine = get(db_session=db_session, routine_id=routine_id)
    if routine is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{routine_id}",
        )

    return GenericResponse.create(items=[routine])


@router.get("/routines", response_model=GenericResponse[RoutineRead])
def get_routines(db_session: DbSession, page: int = 0):
    """루틴 리스트 조회"""
    routines = get_all(db_session=db_session)

    return GenericResponse.create(items=routines)


@router.post("/routines", response_model=GenericResponse[RoutineRead])
def create_routine(db_session: DbSession, routine_in: RoutineCreate):
    """루틴 생성"""
    try:
        routine = create(db_session=db_session, routine_in=routine_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 사용중인 이름입니다 name: {routine_in.name}",
        )

    return GenericResponse.create(items=[routine])


@router.put("/routines/{routine_id}", response_model=GenericResponse[list])
def update_routine(
    db_session: DbSession, routine_id: PrimaryKey, routine_in: RoutineCreate
):
    routine = update(
        db_session=db_session, routine_id=routine_id, routine_in=routine_in
    )

    """루틴 수정"""
    return GenericResponse.create(items=[routine])


@router.delete("/routines", response_model=GenericResponse[RoutineRead])
def delete_routines(db_session: DbSession, routine_in: RoutineDelete):
    """루틴 리스트 삭제"""
    routines = delete(db_session=db_session, routine_in=routine_in)

    return GenericResponse.create(items=routines)
