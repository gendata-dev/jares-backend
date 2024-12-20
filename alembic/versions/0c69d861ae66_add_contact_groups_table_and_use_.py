"""add contact_groups table and use composite key

Revision ID: 0c69d861ae66
Revises: 3cb4d5bafc77
Create Date: 2024-12-04 16:03:00.575915

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0c69d861ae66"
down_revision: Union[str, None] = "3cb4d5bafc77"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "contact_groups",
        sa.Column("contact_id", sa.Integer(), nullable=False),
        sa.Column("crop_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contacts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["crop_id"],
            ["crops.id"],
        ),
        sa.PrimaryKeyConstraint("contact_id", "crop_id"),
    )
    op.drop_column("contact_crops", "id")
    op.drop_column("contact_equipments", "id")
    op.add_column("sessions", sa.Column("id", sa.String(length=255), nullable=False))
    op.drop_column("sessions", "session_id")
    op.add_column(
        "surveys", sa.Column("current_question_id", sa.Integer(), nullable=False)
    )
    op.drop_constraint("surveys_question_id_fkey", "surveys", type_="foreignkey")
    op.create_foreign_key(None, "surveys", "questions", ["current_question_id"], ["id"])
    op.drop_column("surveys", "question_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "surveys",
        sa.Column("question_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "surveys", type_="foreignkey")
    op.create_foreign_key(
        "surveys_question_id_fkey", "surveys", "questions", ["question_id"], ["id"]
    )
    op.drop_column("surveys", "current_question_id")
    op.add_column(
        "sessions",
        sa.Column(
            "session_id", sa.VARCHAR(length=255), autoincrement=False, nullable=False
        ),
    )
    op.drop_column("sessions", "id")
    op.add_column(
        "contact_equipments",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.add_column(
        "contact_crops",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
    )
    op.drop_table("contact_groups")
    # ### end Alembic commands ###
