from fastapi import APIRouter, HTTPException, status

from src.database import DbSession
from src.schema import GenericResponse

from .service import get, create
from .schema import UserLogin, UserCreate, UserRead


router = APIRouter()
"""BASE_URL/user-management"""


@router.post("/token", response_model=GenericResponse[UserRead])
def login_user(
    db_session: DbSession,
    user_in: UserLogin,
):
    user = get(db_session=db_session, user_in=user_in)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{user_in.name}",
        )

    return GenericResponse.create(items=[user])


@router.post("/registry", response_model=GenericResponse[UserRead])
def create_user(
    db_session: DbSession,
    user_in: UserCreate,
):
    user = create(db_session=db_session, user_in=user_in)

    return GenericResponse.create(items=[user])


@router.delete("/token", status_code=status.HTTP_204_NO_CONTENT)
def delete_token():
    """유저 로그아웃"""
    return
