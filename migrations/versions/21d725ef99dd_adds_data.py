"""adds data

Revision ID: 21d725ef99dd
Revises: 941f3a2bde00
Create Date: 2023-04-30 18:47:29.935735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "21d725ef99dd"
down_revision = "941f3a2bde00"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.bulk_insert(
        sa.table(
            "city",
            sa.column("id", sa.Integer),
            sa.column("name", sa.String),
        ),
        [
            {"id": 1, "name": "Tambov"},
            {"id": 2, "name": "Moscow"},
        ],
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("DELETE FROM city WHERE id IN (1, 2)")
    # ### end Alembic commands ###
