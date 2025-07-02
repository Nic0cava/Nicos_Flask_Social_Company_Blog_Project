"""add now() default to blog_post.date manual migration

Revision ID: bd5988c3a94c
Revises: d14a65afad3b
Create Date: 2025-07-02 13:34:29.113303

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = 'bd5988c3a94c'
down_revision = 'd14a65afad3b'
branch_labels = None
depends_on = None



def upgrade():
    # explicitly set the default at the SQL level
    op.execute(
        "ALTER TABLE blog_post "
        "ALTER COLUMN date SET DEFAULT now();"
    )


def downgrade():
    op.execute(
        "ALTER TABLE blog_post "
        "ALTER COLUMN date DROP DEFAULT;"
    )
