"""create posts table

Revision ID: cca8e626dada
Revises: 
Create Date: 2023-06-21 00:44:53.509025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cca8e626dada'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts',
                    sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                    sa.Column('title',sa.String(),nullable=False),
                    sa.Column('content',sa.String(),nullable=False),
                    sa.Column('published',sa.Boolean(),nullable=False,server_default="TRUE"),
                    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('NOW()')),
                    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
