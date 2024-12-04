from fastapi import APIRouter

from src.database import DbSession
from src.schema import GenericResponse

router = APIRouter()
"""BASE_URL/contact-management"""


@router.get("/contacts", response_model=GenericResponse[list])
async def get_contacts(db_session: DbSession):
    """연락처 리스트 조회"""
    return GenericResponse.create(items=[])


@router.post("/contacts", response_model=GenericResponse[list])
async def create_contacts(db_session: DbSession):
    """연락처 리스트 생성"""
    return GenericResponse.create(items=[])


@router.delete("/contacts", response_model=GenericResponse[list])
async def delete_contacts(db_session: DbSession):
    """연락처 리스트 삭제"""
    return GenericResponse.create(items=[])


@router.get("/contacts/{contact_id}", response_model=GenericResponse[list])
async def get_contact(contact_id: int, db_session: DbSession):
    """연락처 조회"""
    return GenericResponse.create(items=[])


@router.put("/contacts/{contact_id}", response_model=GenericResponse[list])
async def update_contact(contact_id: int, db_session: DbSession):
    """연락처 수정"""
    return GenericResponse.create(items=[])


@router.post("/contacts/import", response_model=GenericResponse[list])
async def batch_create_contacts(db_session: DbSession):
    """연락처 파일 업로드 및 저장"""
    return GenericResponse.create(items=[])


@router.get("/groups", response_model=GenericResponse[list])
async def get_groups(db_session: DbSession):
    """그룹 리스트 조회"""
    return GenericResponse.create(items=[])


@router.post("/groups", response_model=GenericResponse[list])
async def create_groups(db_session: DbSession):
    """그룹 리스트 생성"""
    return GenericResponse.create(items=[])


@router.delete("/groups", response_model=GenericResponse[list])
async def delete_groups(db_session: DbSession):
    """그룹 리스트 삭제"""
    return GenericResponse.create(items=[])


@router.get("/groups/{group_id}", response_model=GenericResponse[list])
async def get_group(group_id: int, db_session: DbSession):
    """그룹 조회"""
    return GenericResponse.create(items=[])


@router.put("/groups/{group_id}", response_model=GenericResponse[list])
async def update_group(group_id: int, db_session: DbSession):
    """그룹 수정"""
    return GenericResponse.create(items=[])


@router.post("/contact-group-realations", response_model=GenericResponse[list])
async def update_group_relation(group_id: int, db_session: DbSession):
    """그룹 리스트에 연락처 리스트 추가"""
    return GenericResponse.create(items=[])
