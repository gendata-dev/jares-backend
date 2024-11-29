from fastapi import APIRouter, status

from src.database import DbSession
from src.schema import GenericResponse
from src.auth.schema import UserLoginRequest, UserResponse


router = APIRouter()
"""BASE_URL/user-management"""


@router.post("/token", response_model=GenericResponse[UserResponse])
async def login_user(user_in: UserLoginRequest, db_session: DbSession):
    """ 유저 로그인 """
    items = [UserResponse(userID=1, username="kimwooseok")]
    return GenericResponse.create(items=items)


@router.delete("/token", status_code=status.HTTP_204_NO_CONTENT)
async def delete_token():
    """ 유저 로그아웃 """
    return
