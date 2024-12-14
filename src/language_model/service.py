from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
    update as sa_update,
    delete as sa_delete,
)
from sqlalchemy.orm import Session

from src.config import PAGESIZE
from src.schema import PrimaryKey

from .schema import LanguageModel, LanguageModelCreate, LanguageModelDelete


def get(*, db_session: Session, language_model_id: PrimaryKey) -> dict:
    """Gets a language model by its id"""
    statement = sa_select(LanguageModel.__table__).where(
        LanguageModel.id == language_model_id
    )

    result = db_session.execute(statement).mappings().first()
    return result


def get_many(*, db_session: Session, page: int) -> list[dict]:
    """Gets a paginated list of language models"""
    offset = (page - 1) * PAGESIZE
    statement = (
        sa_select(LanguageModel.__table__)
        .order_by(LanguageModel.id.desc())
        .limit(PAGESIZE)
        .offset(offset)
    )

    result = db_session.execute(statement).mappings().fetchall()
    return result


def create(*, db_session: Session, language_model_in: LanguageModelCreate) -> dict:
    """Creates a new language model"""
    statement = (
        sa_insert(LanguageModel)
        .values(
            name=language_model_in.name,
            reference_file=language_model_in.referenceFile,
            main_goals=language_model_in.mainGoals,
            prompts=language_model_in.prompts,
        )
        .returning(LanguageModel.__table__)
    )

    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def update(
    *,
    db_session: Session,
    language_model_id: PrimaryKey,
    language_model_in: LanguageModelCreate,
) -> dict:
    """Updates an existing language model"""
    statement = (
        sa_update(LanguageModel)
        .where(LanguageModel.id == language_model_id)
        .values(
            name=language_model_in.name,
            reference_file=language_model_in.referenceFile,
            main_goals=language_model_in.mainGoals,
            prompts=language_model_in.prompts,
        )
        .returning(LanguageModel.__table__)
    )
    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def delete(
    *, db_session: Session, language_model_in: LanguageModelDelete
) -> list[dict]:
    """Deletes multiple existing language model"""
    result = []
    if language_model_in.language_modelIds:
        statement = (
            sa_delete(LanguageModel)
            .where(LanguageModel.id.in_(language_model_in.languageModelIds))
            .returning(LanguageModel.__table__)
        )
        result = db_session.execute(statement).mappings().fetchall()
        db_session.commit()

    return result
