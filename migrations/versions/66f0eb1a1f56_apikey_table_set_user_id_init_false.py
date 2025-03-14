"""APIKey table set user.id init=false

Revision ID: 66f0eb1a1f56
Revises: 65daaaa4e605
Create Date: 2025-03-13 21:41:16.958061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '66f0eb1a1f56'
down_revision: Union[str, None] = '65daaaa4e605'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_keys', sa.Column('hashed_key', sa.String(), nullable=False))
    op.alter_column('api_keys', 'last_request',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True)
    op.drop_constraint('api_keys_encrypted_token_key', 'api_keys', type_='unique')
    op.create_unique_constraint(None, 'api_keys', ['hashed_key'])
    op.drop_column('api_keys', 'encrypted_token')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('api_keys', sa.Column('encrypted_token', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'api_keys', type_='unique')
    op.create_unique_constraint('api_keys_encrypted_token_key', 'api_keys', ['encrypted_token'])
    op.alter_column('api_keys', 'last_request',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False)
    op.drop_column('api_keys', 'hashed_key')
    # ### end Alembic commands ###
