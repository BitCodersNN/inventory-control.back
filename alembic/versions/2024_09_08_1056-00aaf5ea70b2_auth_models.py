"""auth_models

Revision ID: 00aaf5ea70b2
Revises: 
Create Date: 2024-09-08 10:56:15.819259

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '00aaf5ea70b2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('login', sa.String(length=32), nullable=False),
    sa.Column('pass_hash', sa.String(length=32), nullable=False),
    sa.Column('role', sa.Enum('reader', 'writer', 'admin', name='user_roles'), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.PrimaryKeyConstraint('user_id')
    )
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.create_table('refresh_sessions',
    sa.Column('token_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('refresh_token', sa.UUID(), nullable=False),
    sa.Column('expires_in', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('token_id')
    )
    op.create_index(op.f('ix_refresh_sessions_refresh_token'), 'refresh_sessions', ['refresh_token'], unique=False)
    op.create_index(op.f('ix_refresh_sessions_token_id'), 'refresh_sessions', ['token_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_refresh_sessions_token_id'), table_name='refresh_sessions')
    op.drop_index(op.f('ix_refresh_sessions_refresh_token'), table_name='refresh_sessions')
    op.drop_table('refresh_sessions')
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
