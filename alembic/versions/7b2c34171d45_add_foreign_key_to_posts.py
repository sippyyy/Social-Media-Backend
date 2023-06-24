"""add foreign_key to posts

Revision ID: 7b2c34171d45
Revises: d7744cca2d1a
Create Date: 2023-06-21 00:59:11.483868

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b2c34171d45'
down_revision = 'd7744cca2d1a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column("owner_id",sa.Integer(),nullable=False))
    op.create_foreign_key(constraint_name="post_users_fk",
                          source_table="posts",
                          referent_table="users",
                          local_cols=["owner_id"],
                          remote_cols=["id"],
                          ondelete="CASCADE"
                          )
    pass


def downgrade() -> None:
    op.drop_column("posts","owner_id")
    op.drop_constraint("post_users_fk","posts")
    pass
