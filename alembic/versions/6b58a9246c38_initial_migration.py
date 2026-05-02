"""Initial migration

Revision ID: 6b58a9246c38
Revises: 
Create Date: 2026-04-30 09:18:07.253310

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6b58a9246c38'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('hashed_password', sa.String(length=255), nullable=False),
    sa.Column('roles', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('email')
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=False)
    
    # Create danh_muc_may_cao table
    op.create_table('danh_muc_may_cao',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ten_thiet_bi', sa.String(length=100), nullable=False),
    sa.Column('loai_thiet_bi', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_danh_muc_may_cao_id'), 'danh_muc_may_cao', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_danh_muc_may_cao_id'), table_name='danh_muc_may_cao')
    op.drop_table('danh_muc_may_cao')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
