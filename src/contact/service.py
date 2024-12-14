from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
    update as sa_update,
    delete as sa_delete,
    exists,
    join,
)
from sqlalchemy.orm import Session, aliased
from sqlalchemy.sql import func

from src.config import PAGESIZE
from src.schema import PrimaryKey
from src.group.schema import Group

from .schema import (
    Contact,
    ContactCrop,
    Crop,
    ContactGroup,
    ContactCreate,
    ContactDelete,
)


def get(*, db_session: Session, contact_id: PrimaryKey) -> dict:
    """
    Gets a contact by its id

    PostgreSQL에서 지원하는 json 타입을 활용한 SQL
    Filter, coalesce를 사용하지 않을 경우 {group_id: None} 값 생성
    subquery를 사용
        subquery는 최적화, 성능 측면에서 좋지 않다는 평가가 많다
        query의 개선이 필요
    """
    group_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object(
                        "group_id", Group.id, "group_name", Group.name
                    )
                ),
                "[]",
            ).label("groups"),
        )
        .select_from(ContactGroup)
        .join(Group, ContactGroup.group_id == Group.id)
        .where(ContactGroup.contact_id == contact_id)
        .subquery()
    )

    crop_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object("crop_id", Crop.id, "crop_name", Crop.name)
                ),
                "[]",
            ).label("crops"),
        )
        .select_from(ContactCrop)
        .join(Crop, ContactCrop.crop_id == Crop.id)
        .where(ContactCrop.contact_id == contact_id)
        .subquery()
    )

    statement = sa_select(
        Contact.id,
        Contact.name,
        Contact.phone,
        Contact.region,
        Contact.preferred_call_time,
        group_subquery,
        crop_subquery,
    ).where(Contact.id == contact_id)

    result = db_session.execute(statement).mappings().first()
    return result


# def get_all(*, db_session: Session) -> list[dict]:
#     """Returns all groups"""
#     statement = sa_select(Group.id, Group.group_name).order_by(Group.id.desc())
#     result = db_session.execute(statement).mappings().fetchall()

#     return result


def get_many(*, db_session: Session, page: int) -> list[dict]:
    """Gets a paginated list of contacts"""
    offset = (page - 1) * PAGESIZE

    contact_alias = aliased(Contact)
    group_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object(
                        "group_id", Group.id, "group_name", Group.name
                    )
                ),
                "[]",
            )
        )
        .select_from(ContactGroup)
        .join(Group, ContactGroup.group_id == Group.id)
        .where(ContactGroup.contact_id == contact_alias.id)
    ).correlate(contact_alias)

    crop_subquery = (
        sa_select(
            func.coalesce(
                func.json_agg(
                    func.json_build_object("crop_id", Crop.id, "crop_name", Crop.name)
                ),
                "[]",
            )
        )
        .select_from(ContactCrop)
        .join(Crop, ContactCrop.crop_id == Crop.id)
        .where(ContactCrop.contact_id == contact_alias.id)
    ).correlate(contact_alias)

    statement = (
        sa_select(
            Contact.id,
            Contact.name,
            Contact.phone,
            Contact.region,
            Contact.preferred_call_time,
            group_subquery.label("groups"),
            crop_subquery.label("crops"),
        )
        .select_from(contact_alias)
        .order_by(contact_alias.id.desc())
        .limit(PAGESIZE)
        .offset(offset)
    )

    result = db_session.execute(statement).mappings().all()
    return result


# TODO: need to check work
def create(*, db_session: Session, contact_in: ContactCreate) -> dict:
    """Creates a new contact"""
    contact_statement = (
        sa_insert(Contact)
        .values(
            name=contact_in.name,
            phone=contact_in.phone,
            region=contact_in.region,
            preferred_call_time=contact_in.preferredCallTime,  # noqa
        )
        .returning(Contact.__table__)
    )
    contact_result = db_session.execute(contact_statement).mappings().first()

    contact_group_result = []
    if contact_in.groupIds:
        contact_group_statement = sa_insert(ContactGroup).returning(
            ContactGroup.__table__
        )
        contact_group_data = [
            {"contact_id": contact_result.get("id"), "group_id": group_id}
            for group_id in contact_in.groupIds
        ]
        contact_group_result = (
            db_session.execute(contact_group_statement, contact_group_data)
            .mappings()
            .fetchall()
        )

    contact_crop_result = []
    if contact_in.crops:
        unnest_crops = sa_select(func.unnest(contact_in.crops).label("name")).subquery()

        new_crops_statement = sa_insert(Crop).from_select(
            ["name"],
            sa_select(unnest_crops.c.name)
            .select_from(unnest_crops)
            .outerjoin(Crop, Crop.name == unnest_crops.c.name)
            .where(Crop.name.is_(None)),
        )
        db_session.execute(new_crops_statement)

        existing_crops_statement = sa_select(Crop.id).where(
            Crop.name.in_(contact_in.crops)
        )
        existing_crops = db_session.execute(existing_crops_statement).mappings().all()

        contact_crop_statement = sa_insert(ContactCrop).returning(ContactCrop.__table__)
        contact_crop_data = [
            {"contact_id": contact_result.get("id"), "crop_id": each_crop.id}
            for each_crop in existing_crops
        ]
        contact_crop_result = (
            db_session.execute(contact_crop_statement, contact_crop_data)
            .mappings()
            .fetchall()
        )
        # return

    # db_session.commit()

    result = dict(contact_result)
    result["groups"] = contact_group_result
    result["crops"] = contact_crop_result
    return result


# TODO: not implemented
def update(
    *, db_session: Session, contact_id: PrimaryKey, contact_in: ContactCreate
) -> dict:
    """Updates an existing contact"""
    statement = (
        sa_update(Contact)
        .where(Contact.id == contact_id)
        .values(
            name=contact_in.name,
            phone=contact_in.phone,
            region=contact_in.region,
            preferred_call_time=contact_in.preferredCallTime,
        )
        .returning(Contact.__table__)
    )
    result = db_session.execute(statement).mappings().first()
    db_session.commit()

    return result


def delete(*, db_session: Session, contact_in: ContactDelete) -> list[dict]:
    """Deletes multiple existing contact"""
    result = []
    if contact_in.contactIds:
        statement = (
            sa_delete(Contact)
            .where(Contact.id.in_(contact_in.groupIds))
            .returning(Contact.__table__)
        )
        result = db_session.execute(statement).mappings().fetchall()
        db_session.commit()

    return result
