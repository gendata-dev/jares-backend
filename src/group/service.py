from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
    update as sa_update,
    delete as sa_delete,
)
from sqlalchemy.orm import Session

from src.config import PAGESIZE
from src.schema import PrimaryKey

from .schema import Group, GroupCreate, GroupList


def get(*, db_session: Session, group_id: PrimaryKey) -> dict:
    """Gets a group by its id"""
    statement = sa_select(Group.id, Group.group_name).where(Group.id == group_id)
    result = db_session.execute(statement).mappings().first()

    return result


def get_all(*, db_session: Session) -> list[dict]:
    """Returns all groups"""
    statement = sa_select(Group.id, Group.group_name).order_by(Group.id.desc())
    result = db_session.execute(statement).mappings().fetchall()

    return result


def get_many(*, db_session: Session, page: int) -> list[dict]:
    """Gets a paginated list of groups"""
    offset = (page - 1) * PAGESIZE
    statement = (
        sa_select(Group.id, Group.group_name)
        .order_by(Group.id.desc())
        .limit(PAGESIZE)
        .offset(offset)
    )
    result = db_session.execute(statement).mappings().fetchall()

    return result


def create(*, db_session: Session, group_in: GroupCreate) -> dict:
    """Creates a new group"""
    statement = (
        sa_insert(Group)
        .values(group_name=group_in.groupName)
        .returning(Group.id, Group.group_name)
    )
    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def update(*, db_session: Session, group_id: PrimaryKey, group_in: GroupCreate) -> dict:
    """Creates a new group"""
    statement = (
        sa_update(Group)
        .where(Group.id == group_id)
        .values(group_name=group_in.groupName)
        .returning(Group.id, Group.group_name)
    )
    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def delete(*, db_session: Session, group_in: GroupList) -> list[dict]:
    """Deletes multiple existing entity"""
    statement = (
        sa_delete(Group)
        .where(Group.id.in_(group_in.groupIds))
        .returning(Group.id, Group.group_name)
    )
    result = db_session.execute(statement).mappings().fetchall()
    db_session.commit()

    return result
