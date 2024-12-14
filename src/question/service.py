from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
    update as sa_update,
    delete as sa_delete,
)
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

from src.config import PAGESIZE
from src.schema import PrimaryKey

from .schema import Question, QuestionCategory, QuestionCreate, QuestionRead


def get(*, db_session: Session, question_category_id: PrimaryKey) -> dict:
    """Gets a question by its id"""
    statement = sa_select(QuestionCategory.__table__).where(
        QuestionCategory.id == question_category_id
    )

    result = db_session.execute(statement).mappings.first()
    return result


def get_all(*, db_session: Session) -> list[dict]:
    """Returns all questions"""
    statement = sa_select(QuestionCategory.__table__).order_by(
        QuestionCategory.id.desc()
    )

    result = db_session.execute(statement).mappings.first()
    return result


def get_many(*, db_session: Session, page: int) -> list[dict]:
    """Returns a paginated list of questions"""
    offset = (page - 1) * PAGESIZE
    statement = (
        sa_select(QuestionCategory.__table__)
        .order_by(QuestionCategory.id.desc())
        .limit(PAGESIZE)
        .offset(offset)
    )

    result = db_session.execute(statement).mappings.first()
    return result


def create(*, db_session: Session, question_in: QuestionCreate) -> dict:
    """Creates a new question"""
    statement = (
        sa_insert(QuestionCategory)
        .values(
            category=question_in.category,
            question_list=question_in.questionList,
        )
        .returning(Question.__table__)
    )

    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def update(
    *, db_session: Session, group_id: PrimaryKey, question_in: QuestionCreate
) -> dict:
    """Updates an existing questions"""
    # statement = (
    #     sa_update(Group)
    #     .where(Group.id == group_id)
    #     .values(name=group_in.name)
    #     .returning(Group.id, Group.name)
    # )
    # result = db_session.execute(statement).mappings().first()
    # db_session.commit()

    # return result


def delete(*, db_session: Session, question_in: list) -> list[dict]:
    """Deletes multiple existing questions"""
    # result = []
    # if group_in.groupIds:
    #     statement = (
    #         sa_delete(Group)
    #         .where(Group.id.in_(group_in.groupIds))
    #         .returning(Group.id, Group.name)
    #     )
    #     result = db_session.execute(statement).mappings().fetchall()
    #     db_session.commit()

    # return result
