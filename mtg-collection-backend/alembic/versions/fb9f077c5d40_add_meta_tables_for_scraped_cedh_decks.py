"""add meta tables for scraped cEDH decks

Revision ID: fb9f077c5d40
Revises: 653b503b5bba
Create Date: 2025-05-19 10:02:35.173425

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fb9f077c5d40'
down_revision: Union[str, None] = '653b503b5bba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'meta_tournaments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('date', sa.Date, nullable=True),
        sa.Column('url', sa.String, nullable=False),
    )
    op.create_table(
        'meta_decks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('commander', sa.String, nullable=True),
        sa.Column('tournament_id', sa.Integer, sa.ForeignKey('meta_tournaments.id')),
        sa.Column('placement', sa.String, nullable=True),
        sa.Column('url', sa.String, nullable=False),
    )
    op.create_table(
        'meta_deck_cards',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('deck_id', sa.Integer, sa.ForeignKey('meta_decks.id')),
        sa.Column('card_name', sa.String, nullable=False),
        sa.Column('set_code', sa.String, nullable=True),
        sa.Column('quantity', sa.Integer, nullable=False),
        sa.Column('is_commander', sa.Boolean, server_default=sa.text('false')),
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
