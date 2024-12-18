from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import SurveyRead, SurveyCreate, SurveyDelete
from .service import get, get_all, get_many, create, update, delete

router = APIRouter()
"""BASE_URL/survey-management"""


@router.get("/surveys/{survey_id}", response_model=GenericResponse[SurveyRead])
def get_survey(db_session: DbSession, survey_id: PrimaryKey):
    """설문 조회"""
    survey = get(db_session=db_session, survey_id=survey_id)
    if survey is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{survey_id}",
        )

    return GenericResponse.create(items=[survey])


@router.get("/surveys", response_model=GenericResponse[SurveyRead])
def get_surveys(db_session: DbSession, page: int = 0):
    """설문 리스트 조회"""
    if page == 0:
        surveys = get_all(db_session=db_session)
    else:
        try:
            surveys = get_many(db_session=db_session, page=page)
        except DataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"유효하지 않는 페이지 입니다 page:{page}",
            )

    return GenericResponse.create(items=surveys)


@router.post("/surveys", response_model=GenericResponse[SurveyRead])
def create_survey(db_session: DbSession, survey_in: SurveyCreate):
    """설문 생성"""
    try:
        survey = create(db_session=db_session, survey_in=survey_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 사용중인 이름입니다 name: {survey_in.name}",
        )

    return GenericResponse.create(items=[survey])


@router.put("/surveys/{survey_id}", response_model=GenericResponse[SurveyRead])
def update_survey(
    db_session: DbSession, survey_id: PrimaryKey, survey_in: SurveyCreate
):
    """설문 수정"""
    try:
        survey = update(db_session=db_session, survey_id=survey_id, survey_in=survey_in)
        if survey is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"존재하지 않는 id 입니다 id:{survey_id}",
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{survey_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[survey])


@router.delete("/surveys", response_model=GenericResponse[SurveyRead])
def delete_surveys(db_session: DbSession, survey_in: SurveyDelete):
    """설문 리스트 삭제"""
    surveys = delete(db_session=db_session, survey_in=survey_in)

    return GenericResponse.create(items=surveys)
