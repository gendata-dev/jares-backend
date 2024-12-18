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
from src.question.schema import QuestionCategory

from .schema import (
    Survey,
    SurveyQuestionCategory,
    SurveyCreate,
    SurveyDelete,
)


def get(*, db_session: Session, survey_id: PrimaryKey) -> dict:
    """Gets a survey by its id"""
    question_category_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object(
                        "question_category_id",
                        QuestionCategory.id,
                        "question_category",
                        QuestionCategory.category,
                    )
                ),
                "[]",
            ).label("question_categories")
        )
        .select_from(SurveyQuestionCategory)
        .join(
            QuestionCategory,
            SurveyQuestionCategory.question_category_id == QuestionCategory.id,
        )
        .where(SurveyQuestionCategory.survey_id == survey_id)
        .subquery()
    )

    statement = sa_select(
        Survey.__table__,
        question_category_subquery,
    ).where(Survey.id == survey_id)

    result = db_session.execute(statement).mappings().first()
    return result


def get_all(*, db_session: Session) -> list[dict]:
    """Returns all questions"""
    survey_alias = aliased(Survey)
    question_category_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object(
                        "question_category_id",
                        QuestionCategory.id,
                        "question_category",
                        QuestionCategory.category,
                    )
                ),
                "[]",
            )
        )
        .select_from(SurveyQuestionCategory)
        .join(
            QuestionCategory,
            SurveyQuestionCategory.question_category_id == QuestionCategory.id,
        )
        .where(SurveyQuestionCategory.survey_id == survey_alias.id)
    ).correlate(survey_alias)

    statement = sa_select(
        Survey.__table__, question_category_subquery.label("question_categories")
    ).order_by(Survey.id.desc())

    result = db_session.execute(statement).mappings().fetchall()
    return result


def get_many(*, db_session: Session, page: int) -> list[dict]:
    """Returns a paginated list of questions"""
    offset = (page - 1) * PAGESIZE

    survey_alias = aliased(Survey)
    question_category_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object(
                        "question_category_id",
                        QuestionCategory.id,
                        "question_category",
                        QuestionCategory.category,
                    )
                ),
                "[]",
            )
        )
        .select_from(SurveyQuestionCategory)
        .join(
            QuestionCategory,
            SurveyQuestionCategory.question_category_id == QuestionCategory.id,
        )
        .where(SurveyQuestionCategory.survey_id == survey_alias.id)
    ).correlate(survey_alias)

    statement = (
        sa_select(
            Survey.__table__, question_category_subquery.label("question_categories")
        )
        .order_by(Survey.id.desc())
        .limit(PAGESIZE)
        .offset(offset)
    )

    result = db_session.execute(statement).mappings().fetchall()
    return result


def create(*, db_session: Session, survey_in: SurveyCreate) -> dict:
    """Creates a new survey"""
    survey_statement = (
        sa_insert(Survey)
        .values(
            name=survey_in.name,
        )
        .returning(Survey.__table__)
    )
    survey_result = db_session.execute(survey_statement).mappings().first()

    survey_category_statement = sa_insert(SurveyQuestionCategory).returning(
        SurveyQuestionCategory.question_category_id
    )
    survey_category_data = [
        {"survey_id": survey_result.get("id"), "question_category_id": category_id}
        for category_id in survey_in.questionCategories
    ]
    survey_category_result = (
        db_session.execute(survey_category_statement, survey_category_data)
        .mappings()
        .fetchall()
    )
    db_session.commit()

    result = dict(survey_result)
    result["question_categories"] = survey_category_result
    return result


def update(
    *,
    db_session: Session,
    survey_id: PrimaryKey,
    survey_in: SurveyCreate,
) -> dict:
    """Updates an existing survey"""
    existing_relation_statement = sa_select(
        SurveyQuestionCategory.question_category_id,
    ).where(SurveyQuestionCategory.survey_id == survey_id)
    existing_category_result = (
        db_session.execute(existing_relation_statement).scalars().fetchall()
    )

    existing_category_ids = set(existing_category_result)
    new_category_ids = set(survey_in.questionCategories)
    to_add = new_category_ids - existing_category_ids
    to_remove = existing_category_ids - new_category_ids

    if to_add:
        insert_relation_statement = sa_insert(SurveyQuestionCategory).values(
            [
                {"survey_id": survey_id, "question_category_id": new_category_id}
                for new_category_id in to_add
            ]
        )
        db_session.execute(insert_relation_statement)

    if to_remove:
        delete_relation_statement = sa_delete(SurveyQuestionCategory).where(
            (SurveyQuestionCategory.survey_id == survey_id)
            & (SurveyQuestionCategory.question_category_id.in_(to_remove))
        )
        db_session.execute(delete_relation_statement)

    update_statement = (
        sa_update(Survey)
        .where(Survey.id == survey_id)
        .values(
            name=survey_in.name,
        )
    )

    db_session.execute(update_statement)
    db_session.commit()

    result = get(db_session=db_session, survey_id=survey_id)
    return result


def delete(*, db_session: Session, survey_in: SurveyDelete) -> list[dict]:
    """Deletes multiple existing language model"""
    result = []
    if survey_in.surveyIds:
        statement = (
            sa_delete(Survey)
            .where(Survey.id.in_(survey_in.surveyIds))
            .returning(Survey.__table__)
        )
        result = db_session.execute(statement).mappings().fetchall()
        db_session.commit()

    return result
