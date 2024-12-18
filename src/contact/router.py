from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import ContactCreate, ContactRead, ContactDelete
from .service import get, get_all, get_many, create, delete


router = APIRouter()
"""BASE_URL/contact-management"""


@router.get("/contacts/{contact_id}", response_model=GenericResponse[ContactRead])
def get_contact(contact_id: PrimaryKey, db_session: DbSession):
    """연락처 조회"""
    contact = get(db_session=db_session, contact_id=contact_id)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{contact_id}",
        )

    return GenericResponse.create(items=contact)


@router.get("/contacts", response_model=GenericResponse[ContactRead])
def get_contacts(db_session: DbSession, page: int = 0):
    """연락처 리스트 조회"""
    if page == 0:
        contacts = get_all(db_session=db_session)
    else:
        try:
            contacts = get_many(db_session=db_session, page=page)
        except DataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"유효하지 않는 페이지 입니다 page:{page}",
            )

    return GenericResponse.create(items=contacts)


@router.post("/contacts", response_model=GenericResponse[ContactRead])
def create_contact(db_session: DbSession, contact_in: ContactCreate):
    """연락처 생성"""
    try:
        contact = create(db_session=db_session, contact_in=contact_in)
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"데이터 베이스 에러 message: {e}",
        )

    return GenericResponse.create(items=[contact])


@router.put("/contacts/{contact_id}", response_model=GenericResponse[list])
def update_contact(contact_id: int, db_session: DbSession):
    """연락처 수정"""
    return GenericResponse.create(items=[])


@router.delete("/contacts", response_model=GenericResponse[ContactRead])
def delete_contacts(db_session: DbSession, contact_in: ContactDelete):
    """연락처 리스트 삭제"""
    contacts = delete(db_session=db_session, contact_in=contact_in)

    return GenericResponse.create(items=[contacts])


@router.post("/contacts/import", response_model=GenericResponse[list])
def batch_create_contacts(db_session: DbSession):
    """연락처 파일 업로드 및 저장"""
    return GenericResponse.create(items=[])
