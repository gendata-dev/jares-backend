from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .schema import QuestionRead, QuestionCreate
from .service import get, get_all, get_many, create, update

router = APIRouter()
"""BASE_URL/question-management"""


@router.get("/questions/{question_id}", response_model=GenericResponse[QuestionRead])
def get_question(db_session: DbSession, question_id: PrimaryKey):
    """질문 조회"""
    question_category = get(db_session=db_session, question_id=question_id)
    if question_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{question_id}",
        )

    return GenericResponse.create(items=[])


@router.get("/questions", response_model=GenericResponse[QuestionRead])
def get_questions(db_session: DbSession, page: int = 0):
    """질문 리스트 조회"""
    if page == 0:
        questions = get_all(db_session=db_session)
    else:
        try:
            questions = get_many(db_session=db_session, page=page)
        except DataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"유효하지 않는 페이지 입니다 page:{page}",
            )

    return GenericResponse.create(items=[questions])


@router.post("/questions", response_model=GenericResponse[QuestionRead])
def create_questions(db_session: DbSession, question_in: QuestionCreate):
    """질문 생성"""
    try:
        question = create(db_session=db_session, question_in=question_in)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{question_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[question])


@router.put("/questions/{question_id}", response_model=GenericResponse[QuestionRead])
def update_questions(
    db_session: DbSession, question_id: PrimaryKey, question_in: QuestionCreate
):
    """질문 수정"""
    try:
        question = update(
            db_session=db_session, question_id=question_id, group_in=group_in
        )
        if question is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"존재하지 않는 id 입니다 id:{question_id}",
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{question_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[question])


@router.delete("/questions", response_model=GenericResponse[list])
def delete_questions(db_session: DbSession):
    """질문 삭제"""

    return GenericResponse.create(items=[])
