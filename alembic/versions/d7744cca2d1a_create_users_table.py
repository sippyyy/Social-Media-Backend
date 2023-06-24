"""create users table

Revision ID: d7744cca2d1a
Revises: cca8e626dada
Create Date: 2023-06-21 00:52:37.044507

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7744cca2d1a'
down_revision = 'cca8e626dada'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id", sa.Integer,nullable=False,primary_key=True),
                    sa.Column("email", sa.String(),nullable=False),
                    sa.Column("password", sa.String(),nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text("NOW()")),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
