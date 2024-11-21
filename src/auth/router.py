from fastapi import APIRouter, status

router = APIRouter()
"""BASE_URL/user-management"""


@router.post("/token")
async def create_token():
    return {"token": "mock jwt", "role": "mock user"}


@router.delete("/token", status_code=status.HTTP_201_CREATED)
async def delete_token():
    return {"message": "Logged out successfully"}
