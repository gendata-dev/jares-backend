from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import GroupCreate, GroupRead, GroupList
from .service import get, get_all, get_many, create, update, delete

router = APIRouter()
"""BASE_URL/group-management"""


@router.get("/groups/{group_id}", response_model=GenericResponse[GroupRead])
def get_group(db_session: DbSession, group_id: PrimaryKey):
    """그룹 조회"""
    group = get(db_session=db_session, group_id=group_id)
    if group is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{group_id}",
        )

    return GenericResponse.create(items=[group])


@router.get("/groups", response_model=GenericResponse[GroupRead])
def get_groups(db_session: DbSession, page: int = 0):
    """그룹 리스트 조회"""
    if page == 0:
        groups = get_all(db_session=db_session)
    else:
        try:
            groups = get_many(db_session=db_session, page=page)
        except DataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"유효하지 않는 페이지 입니다 page:{page}",
            )

    return GenericResponse.create(items=groups)


@router.post("/groups", response_model=GenericResponse[GroupRead])
def create_group(db_session: DbSession, group_in: GroupCreate):
    """그룹 생성"""
    try:
        group = create(db_session=db_session, group_in=group_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 사용중인 이름입니다 name: {group_in.name}",
        )

    return GenericResponse.create(items=[group])


@router.put("/groups/{group_id}", response_model=GenericResponse[GroupRead])
def update_group(db_session: DbSession, group_id: PrimaryKey, group_in: GroupCreate):
    """그룹 수정"""
    try:
        group = update(db_session=db_session, group_id=group_id, group_in=group_in)
        if group is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"존재하지 않는 id 입니다 id:{group_id}",
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{group_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[group])


@router.delete("/groups", response_model=GenericResponse[GroupRead])
def delete_groups(db_session: DbSession, group_in: GroupList):
    """그룹 리스트 삭제"""
    groups = delete(db_session=db_session, group_in=group_in)

    return GenericResponse.create(items=groups)


@router.post("/contact-group-realations", response_model=GenericResponse[list])
def update_group_relation(db_session: DbSession, group_id: int):
    """그룹 리스트에 연락처 리스트 추가"""
    return GenericResponse.create(items=[])
