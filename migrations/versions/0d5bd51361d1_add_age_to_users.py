"""add age to users

Revision ID: 0d5bd51361d1
Revises: 09252a49d824
Create Date: 2025-09-18 13:56:52.704361

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0d5bd51361d1"
down_revision: Union[str, Sequence[str], None] = "09252a49d824"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add nullable age column to users
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop age column from users
    op.drop_column("users", "age")
