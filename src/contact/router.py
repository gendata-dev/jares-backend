from fastapi import APIRouter

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import ContactCreate
from .service import get, create

router = APIRouter()
"""BASE_URL/contact-management"""


@router.get("/contacts", response_model=GenericResponse[list])
async def get_contacts(db_session: DbSession):
    """연락처 리스트 조회"""
    return GenericResponse.create(items=[])


@router.delete("/contacts", response_model=GenericResponse[list])
async def delete_contacts(db_session: DbSession):
    """연락처 리스트 삭제"""
    return GenericResponse.create(items=[])


@router.post("/contacts", response_model=GenericResponse[list])
async def create_contacts(db_session: DbSession, contact_in: ContactCreate):
    """연락처 생성"""
    items = create(db_session=db_session, contact_in=contact_in)
    return GenericResponse.create(items=[items])


@router.get("/contacts/{contact_id}", response_model=GenericResponse[list])
async def get_contact(contact_id: PrimaryKey, db_session: DbSession):
    """연락처 조회"""
    items = get(db_session=db_session, contact_id=contact_id)
    return GenericResponse.create(items=[items])


@router.put("/contacts/{contact_id}", response_model=GenericResponse[list])
async def update_contact(contact_id: int, db_session: DbSession):
    """연락처 수정"""
    return GenericResponse.create(items=[])


@router.post("/contacts/import", response_model=GenericResponse[list])
async def batch_create_contacts(db_session: DbSession):
    """연락처 파일 업로드 및 저장"""
    return GenericResponse.create(items=[])
