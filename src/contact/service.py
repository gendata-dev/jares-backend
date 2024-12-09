from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from .schema import Contact


def get_contact(*, db_session: Session, contact_id: int) -> Optional[list]:
    """Gets a contact by its id"""
    stmt = select(Contact).where(Contact.id == contact_id)
    return db_session.execute(stmt).all()


def create_contact(*, db_session: Session, contact_in: int) -> Optional[list]:
    """Creates a new contact"""
    stmt = insert(Contact).values(
        group_id=1,
        name=contact_in.name,
        phone=contact_in.phone,
        region=contact_in.region,
        preferred_call_time=contact_in.preferredCallTime,
    )

    result = db_session.execute(stmt)
    db_session.commit()

    return result.inserted_primary_key[0]


