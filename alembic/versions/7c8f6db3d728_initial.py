"""initial

Revision ID: 7c8f6db3d728
Revises: 
Create Date: 2023-12-14 12:37:17.768870

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7c8f6db3d728"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column(
            "full_name",
            sa.VARCHAR(length=50),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "password",
            sa.VARCHAR(length=100),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("phone", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    # ### end Alembic commands ###
