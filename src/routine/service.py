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

from .schema import Routine, RoutineCreate, RoutineRead


def get(*, db_session: Session, routine_id: PrimaryKey) -> dict:
    """Gets a routine by its id"""
    statement = sa_select(Routine.__table__).where(Routine.id == routine_id)

    result = db_session.execute(statement).mappings.first()
    return result


def create(*, db_session: Session, routine_in: RoutineCreate) -> dict:
    """Creates a new routine"""
    statement = (
        sa_insert(Routine)
        .values(
            group_id=routine_in.groupId,
            survey_id=routine_in.surveyId,
            llm_id=routine_in.llmId,
            name=routine_in.name,
            start_date=routine_in.startDate,
            end_date=routine_in.endDate,
            active_status=routine_in.activeStatus,
            day_of_week=routine_in.dayOfWeek,
        )
        .returning(Routine.__table__)
    )

    result = db_session.execute(statement).mappings().first()
    # db_session.commit()

    return result


# def get_many(*, db_session: Session, page: int) -> list[dict]:
#     """Gets a paginated list of contacts"""
#     offset = (page - 1) * PAGESIZE

#     contact_alias = aliased(Contact)
#     group_subquery = (
#         sa_select(
#             func.coalesce(
#                 func.json_agg(
#                     func.json_build_object(
#                         "group_id", Group.id,
#                         "group_name", Group.name
#                     )
#                 ),
#                 "[]"
#             )
#         )
#         .select_from(ContactGroup)
#         .join(Group, ContactGroup.group_id == Group.id)
#         .where(ContactGroup.contact_id == contact_alias.id)
#     ).correlate(contact_alias)

#     crop_subquery = (
#         sa_select(
#             func.coalesce(
#                 func.json_agg(
#                     func.json_build_object(
#                         "crop_id", Crop.id,
#                         "crop_name", Crop.name
#                     )
#                 ),
#                 "[]"
#             )
#         )
#         .select_from(ContactCrop)
#         .join(Crop, ContactCrop.crop_id == Crop.id)
#         .where(ContactCrop.contact_id == contact_alias.id)
#     ).correlate(contact_alias)

#     statement = (
#         sa_select(
#             Contact.id,
#             Contact.name,
#             Contact.phone,
#             Contact.region,
#             Contact.preferred_call_time,
#             group_subquery.label("groups"),
#             crop_subquery.label("crops")
#         )
#         .select_from(contact_alias)
#         .order_by(contact_alias.id.desc())
#         .limit(PAGESIZE)
#         .offset(offset)
#     )

#     result = db_session.execute(statement).mappings().all()
#     return result


# # TODO: need to check work
# def create(*, db_session: Session, contact_in: ContactCreate) -> dict:
#     """Creates a new contact"""
#     contact_statement = (
#         sa_insert(Contact)
#         .values(
#                 name=contact_in.name,
#                 phone=contact_in.phone,
#                 region=contact_in.region,
#                 preferred_call_time=contact_in.preferredCallTime,  # noqa
#             )
#         .returning(Contact.__table__)
#     )
#     contact_result = db_session.execute(contact_statement).mappings().first()

#     contact_group_result = []
#     if contact_in.groupIds:
#         contact_group_statement = (
#             sa_insert(ContactGroup)
#             .returning(ContactGroup.__table__)
#         )
#         contact_group_data = [{"contact_id": contact_result.get("id"), "group_id": group_id} for group_id in contact_in.groupIds]
#         contact_group_result = db_session.execute(contact_group_statement, contact_group_data).mappings().fetchall()

#     contact_crop_result = []
#     if contact_in.crops:
#         unnest_crops = sa_select(func.unnest(contact_in.crops).label("name")).subquery()

#         new_crops_statement = (
#             sa_insert(Crop)
#             .from_select(
#                 ["name"],
#                 sa_select(unnest_crops.c.name)
#                 .select_from(unnest_crops)
#                 .outerjoin(
#                     Crop,
#                     Crop.name == unnest_crops.c.name
#                 )
#                 .where(Crop.name.is_(None))
#             )
#         )
#         db_session.execute(new_crops_statement)

#         existing_crops_statement = sa_select(Crop.id).where(Crop.name.in_(contact_in.crops))
#         existing_crops = db_session.execute(existing_crops_statement).mappings().all()

#         contact_crop_statement = (
#             sa_insert(ContactCrop)
#             .returning(ContactCrop.__table__)
#         )
#         contact_crop_data = [
#             {"contact_id": contact_result.get("id"), "crop_id": each_crop.id}
#             for each_crop in existing_crops
#         ]
#         contact_crop_result = db_session.execute(contact_crop_statement, contact_crop_data).mappings().fetchall()
#         # return

#     # db_session.commit()

#     result = dict(contact_result)
#     result["groups"] = contact_group_result
#     result["crops"] = contact_crop_result
#     return result


# # TODO: not implemented
# def update(*, db_session: Session, contact_id: PrimaryKey, contact_in: ContactCreate) -> dict:
#     """Updates an existing contact"""
#     statement = (
#         sa_update(Contact)
#         .where(Contact.id == contact_id)
#         .values(
#             name=contact_in.name,
#             phone=contact_in.phone,
#             region=contact_in.region,
#             preferred_call_time=contact_in.preferredCallTime,

#         )
#         .returning(Contact.__table__)
#     )
#     result = db_session.execute(statement).mappings().first()
#     db_session.commit()

#     return result


# def delete(*, db_session: Session, contact_in: ContactDelete) -> list[dict]:
#     """Deletes multiple existing contact"""
#     result = []
#     if contact_in.contactIds:
#         statement = (
#             sa_delete(Contact)
#             .where(Contact.id.in_(contact_in.groupIds))
#             .returning(Contact.__table__)
#         )
#         result = db_session.execute(statement).mappings().fetchall()
#         db_session.commit()

#     return result
