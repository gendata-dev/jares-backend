import bcrypt
from sqlalchemy import (
    select as sa_select,
    insert as sa_insert,
)
from sqlalchemy.orm import Session


from .schema import (
    User,
    UserLogin,
    UserCreate,
)


def get(*, db_session: Session, user_in: UserLogin) -> dict:
    """Gets a user by its name and password"""
    statement = sa_select(
        User.__table__,
    ).where(User.name == user_in.name)
    db_user = db_session.execute(statement).mappings().first()
    if db_user is None:
        return None

    hashed = bcrypt.hashpw(user_in.password.encode("utf-8"), bcrypt.gensalt())
    is_valid_pw = bcrypt.checkpw(user_in.password.encode("utf-8"), hashed)
    if not is_valid_pw:
        return None

    result = dict(db_user)
    result["password_hash"] = ""
    return result


def create(*, db_session: Session, user_in: UserCreate) -> dict:
    """Creates a new user"""
    existing_user_statement = sa_select(User.name).where(User.name == user_in.name)
    existing_user = db_session.execute(existing_user_statement).first()
    if existing_user is not None:
        return None

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_in.password.encode("utf-8"), salt)

    user_insert_statement = (
        sa_insert(User)
        .values(
            name=user_in.name,
            password_hash=hashed_password,
            is_active=True,
        )
        .returning(
            User.name,
            User.is_active,
        )
    )

    result = db_session.execute(user_insert_statement).mappings().first()
    db_session.commit()
    return result


# def update(
# *, db_session: Session, question_id: PrimaryKey, question_in: QuestionCreate
# ) -> dict:
# """Updates an existing question"""
# statement = (
#     sa_update(Question)
#     .where(Question.id == question_id)
#     .values(
#         name=question_in.name
#     )
#     .returning(question.id, question.name)
# )
# result = db_session.execute(statement).mappings().first()
# db_session.commit()

# return result


# def delete(*, db_session: Session, question_in: list) -> list[dict]:
# """Deletes multiple existing questions"""
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
