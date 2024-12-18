from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
    update as sa_update,
    delete as sa_delete,
)
from sqlalchemy.orm import Session

from src.group.schema import Group
from src.survey.schema import Survey
from src.language_model.schema import LanguageModel
from src.schema import PrimaryKey

from .schema import Routine, RoutineCreate, RoutineDelete


def get(*, db_session: Session, routine_id: PrimaryKey) -> dict:
    """Gets a routine by its id"""
    statement = (
        sa_select(
            Routine.__table__,
            Group.name.label("group_name"),
            Survey.name.label("survey_name"),
            LanguageModel.name.label("language_model_name"),
        )
        .select_from(Routine)
        .join(Group, Routine.group_id == Group.id)
        .join(Survey, Routine.survey_id == Survey.id)
        .join(LanguageModel, Routine.language_model_id == LanguageModel.id)
        .where(Routine.id == routine_id)
    )

    result = db_session.execute(statement).mappings().first()
    return result


def get_all(*, db_session: Session) -> list[dict]:
    """Returns all routines"""
    statement = (
        sa_select(
            Routine.__table__,
            Group.name.label("group_name"),
            Survey.name.label("survey_name"),
            LanguageModel.name.label("language_model_name"),
        )
        .select_from(Routine)
        .join(Group, Routine.group_id == Group.id)
        .join(Survey, Routine.survey_id == Survey.id)
        .join(LanguageModel, Routine.language_model_id == LanguageModel.id)
    )

    result = db_session.execute(statement).mappings().fetchall()
    return result


def create(*, db_session: Session, routine_in: RoutineCreate) -> dict:
    """Creates a new routine"""
    statement = (
        sa_insert(Routine)
        .values(
            group_id=routine_in.groupId,
            survey_id=routine_in.surveyId,
            language_model_id=routine_in.languageModelId,
            name=routine_in.name,
            start_date=routine_in.startDate,
            end_date=routine_in.endDate,
            active_status=routine_in.activeStatus,
            execution_days=routine_in.executionDays,
        )
        .returning(Routine.__table__)
    )

    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def update(
    *, db_session: Session, routine_id: PrimaryKey, routine_in: RoutineCreate
) -> dict:
    """Updates an existing routine"""
    statement = (
        sa_update(Routine)
        .where(Routine.id == routine_id)
        .values(
            group_id=routine_in.groupId,
            survey_id=routine_in.surveyId,
            language_model_id=routine_in.languageModelId,
            name=routine_in.name,
            start_date=routine_in.startDate,
            end_date=routine_in.endDate,
            active_status=routine_in.activeStatus,
            execution_days=routine_in.executionDays,
        )
        .returning(Routine.id, Routine.name)
    )

    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def delete(*, db_session: Session, routine_in: RoutineDelete) -> list[dict]:
    """Deletes multiple existing routine"""
    result = []
    if routine_in.routineIds:
        statement = (
            sa_delete(Routine)
            .where(Routine.id.in_(routine_in.routineIds))
            .returning(Routine.__table__)
        )
        result = db_session.execute(statement).mappings().fetchall()
        db_session.commit()

    return result
