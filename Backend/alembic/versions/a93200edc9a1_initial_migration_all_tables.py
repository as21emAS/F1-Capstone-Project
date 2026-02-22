"""Initial migration - all tables

Revision ID: a93200edc9a1
Revises: 
Create Date: 2026-02-15 17:12:11.031652

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from models import Base

revision: str = 'a93200edc9a1'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())