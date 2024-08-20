"""auth_models

Revision ID: 91d206d13800
Revises: 9559ab726779
Create Date: 2024-08-19 14:40:08.677950

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op
from alembic.ddl import postgresql

# revision identifiers, used by Alembic.
revision: str = '91d206d13800'
down_revision: Union[str, None] = '9559ab726779'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";")

    op.add_column('users', sa.Column('new_user_id', sa.UUID(), nullable=True))
    op.execute("""
        UPDATE users
        SET new_user_id = uuid_generate_v4()  -- Replace with your conversion logic
        WHERE new_user_id IS NULL;
    """)
    op.drop_column('users', 'user_id')
    op.alter_column('users', 'new_user_id', new_column_name='user_id')
    op.create_primary_key('pk_users', 'users', ['user_id'])

    op.create_table('refresh_tokens',
                    sa.Column('token_id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('refresh_token', sa.UUID(), nullable=False),
                    sa.Column('expires_in', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                              nullable=False),
                    sa.Column('revoked', sa.Boolean(), nullable=False),
                    sa.Column('user_id', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('token_id')
                    )
    op.create_index(op.f('ix_refresh_tokens_refresh_token'), 'refresh_tokens', ['refresh_token'], unique=False)
    op.create_index(op.f('ix_refresh_tokens_token_id'), 'refresh_tokens', ['token_id'], unique=False)
    op.drop_constraint('users_login_key', 'users', type_='unique')
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=False)
    op.drop_column('users', 'salt')
    # ### end Alembic commands ###


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS \"uuid-ossp\";")

    op.drop_constraint('pk_users', 'users', type_='primary')
    op.alter_column('users', 'user_id', new_column_name='new_user_id')
    op.add_column('users', sa.Column('user_id', sa.UUID(), nullable=True))
    op.execute("""
        UPDATE users
        SET user_id = new_user_id;
    """)
    op.drop_column('users', 'new_user_id')
    op.create_primary_key('pk_users', 'users', ['user_id'])

    op.alter_column('users', 'user_id',
                    existing_type=sa.UUID(),
                    type_=sa.INTEGER(),
                    existing_nullable=False)
    op.add_column('users', sa.Column('salt', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.create_unique_constraint('users_login_key', 'users', ['login'])
    op.drop_index(op.f('ix_refresh_tokens_token_id'), table_name='refresh_tokens')
    op.drop_index(op.f('ix_refresh_tokens_refresh_token'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
    # ### end Alembic commands ###
