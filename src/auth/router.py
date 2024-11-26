from fastapi import APIRouter, status

from src.database import DbSession
from src.auth.schema import UserLoginRequest, UserResponse, User, Session
from src.schema import GenericResponse

router = APIRouter()
"""BASE_URL/user-management"""


# @router.post("/token", response_model=GenericResponse[UserResponse])
@router.post("/token")
async def login_user(
    user_in: UserLoginRequest,
    db_session: DbSession,
):
    print(db_session.query(User))
    return {"token": "mock jwt", "role": "mock user"}


@router.delete("/token", status_code=status.HTTP_201_CREATED)
async def delete_token():
    return {"message": "Logged out successfully"}
