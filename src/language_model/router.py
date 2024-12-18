from fastapi import APIRouter, HTTPException, status
from sqlalchemy.exc import IntegrityError, DataError

from src.database import DbSession
from src.schema import GenericResponse, PrimaryKey

from .service import get, get_many, create, update, delete
from .schema import LanguageModelCreate, LanguageModelRead, LanguageModelDelete

router = APIRouter()
"""BASE_URL/llm-management"""


@router.get(
    "/language-models/{language_model_id}",
    response_model=GenericResponse[LanguageModelRead],
)
def get_language_model(db_session: DbSession, language_model_id: PrimaryKey):
    """언어 모델 조회"""
    language_model = get(db_session=db_session, language_model_id=language_model_id)
    if language_model is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"존재하지 않는 id 입니다 id:{language_model_id}",
        )

    return GenericResponse.create(items=[language_model])


@router.get("/language-models", response_model=GenericResponse[LanguageModelRead])
def get_language_models(db_session: DbSession, page: int = 0):
    """언어 모델 리스트 조회"""
    # TODO -> GET_ALL if state
    try:
        language_models = get_many(db_session=db_session, page=page)
    except DataError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않는 페이지 입니다 page:{page}",
        )

    return GenericResponse.create(items=language_models)


@router.post("/language-models", response_model=GenericResponse[LanguageModelRead])
def create_language_model(
    db_session: DbSession, language_model_in: LanguageModelCreate
):
    """언어 모델 생성"""
    try:
        language_model = create(
            db_session=db_session, language_model_in=language_model_in
        )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"이미 사용중인 이름입니다 name: {language_model_in.name}",
        )

    return GenericResponse.create(items=[language_model])


@router.put(
    "/language-models/{language_model_id}",
    response_model=GenericResponse[LanguageModelRead],
)
def update_language_model(
    db_session: DbSession,
    language_model_id: PrimaryKey,
    language_model_in: LanguageModelCreate,
):
    """언어 모델 수정"""
    try:
        language_model = update(
            db_session=db_session,
            language_model_id=language_model_id,
            language_model_in=language_model_in,
        )
        if language_model is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"존재하지 않는 id 입니다 id:{language_model_id}",
            )
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{language_model_in.name}은 이미 사용중인 이름입니다",
        )

    return GenericResponse.create(items=[language_model])


@router.delete("/language-models", response_model=GenericResponse[list])
def delete_language_models(
    db_session: DbSession, language_model_in: LanguageModelDelete
):
    """언어 모델 삭제"""
    language_models = delete(db_session=db_session, language_model_in=language_model_in)

    return GenericResponse.create(items=[language_models])
