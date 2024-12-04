from fastapi import APIRouter

from src.database import DbSession
from src.schema import GenericResponse

router = APIRouter()
"""BASE_URL/survey-management"""


@router.get("/surveys", response_model=GenericResponse[list])
async def get_surveys(db_session: DbSession):
    """설문 리스트 조회"""
    return GenericResponse.create(items=[])


@router.post("/surveys", response_model=GenericResponse[list])
async def create_surveys(db_session: DbSession):
    """설문 리스트 생성"""
    return GenericResponse.create(items=[])


@router.delete("/surveys", response_model=GenericResponse[list])
async def delete_surveys(db_session: DbSession):
    """설문 리스트 삭제"""
    return GenericResponse.create(items=[])


@router.get("/surveys/{survey_id}", response_model=GenericResponse[list])
async def get_survey(survey_id: int, db_session: DbSession):
    """설문 조회"""
    return GenericResponse.create(items=[])


@router.put("/surveys/{survey_id}", response_model=GenericResponse[list])
async def update_survey(survey_id: int, db_session: DbSession):
    """설문 수정"""
    return GenericResponse.create(items=[])


@router.get("/surveys/{survey_id}/questions", response_model=GenericResponse[list])
async def get_questions(survey_id: int, db_session: DbSession):
    """질문 리스트 조회"""
    return GenericResponse.create(items=[])


@router.post("/surveys/{survey_id}/questions", response_model=GenericResponse[list])
async def create_questions(survey_id: int, db_session: DbSession):
    """질문 생성"""
    return GenericResponse.create(items=[])


@router.put("/surveys/{survey_id}/questions", response_model=GenericResponse[list])
async def delete_questions(survey_id: int, db_session: DbSession):
    """질문 삭제"""
    return GenericResponse.create(items=[])


@router.delete("/surveys/{survey_id}/questions", response_model=GenericResponse[list])
async def update_questions(survey_id: int, db_session: DbSession):
    """질문 수정"""
    return GenericResponse.create(items=[])
