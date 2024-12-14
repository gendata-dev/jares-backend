from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import RoutineRead, RoutineCreate
from .service import get, create

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
    return GenericResponse.create(items=[])


@router.get("/routines", response_model=GenericResponse[RoutineRead])
def get_routines(db_session: DbSession, page: int = 0):
    """루틴 리스트 조회"""
    # if page == 0:
    # routines = get_all(db_session=db_session)
    # else:
    # try:
    # routines = get_many(db_session=db_session, page=page)
    # except DataError:
    # raise HTTPException(
    # status_code=status.HTTP_400_BAD_REQUEST,
    # detail=f"유효하지 않는 페이지 입니다 page:{page}",
    # )

    return GenericResponse.create(items=[])


@router.post("/routines", response_model=GenericResponse[list])
def create_routine(db_session: DbSession, routine_in: RoutineCreate):
    """루틴 생성"""
    try:
        routine = create(db_session=db_session, routine_in=routine_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{routine_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[routine])


@router.put("/routines/{routine_id}", response_model=GenericResponse[list])
def update_routine(routine_id: PrimaryKey, db_session: DbSession):
    """루틴 수정"""
    return GenericResponse.create(items=[])


@router.delete("/routines", response_model=GenericResponse[list])
def delete_routines(db_session: DbSession):
    """루틴 리스트 삭제"""
    return GenericResponse.create(items=[])
