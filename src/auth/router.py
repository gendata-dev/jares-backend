from fastapi import APIRouter

# APIRouter 객체 생성
router = APIRouter()

# 라우트 정의
@router.get("/example")
async def example_route():
    return {"message": "This is an example route"}