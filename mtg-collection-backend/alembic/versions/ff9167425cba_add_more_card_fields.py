"""Add more card fields

Revision ID: ff9167425cba
Revises: 313b55bd4b15
Create Date: 2025-05-18 01:14:38.364640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff9167425cba'
down_revision: Union[str, None] = '313b55bd4b15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
