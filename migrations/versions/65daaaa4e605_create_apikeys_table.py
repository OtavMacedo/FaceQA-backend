"""Create APIKeys Table

Revision ID: 65daaaa4e605
Revises: 8049c1cd4f0d
Create Date: 2025-03-12 21:43:08.553381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '65daaaa4e605'
down_revision: Union[str, None] = '8049c1cd4f0d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_keys',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('encrypted_token', sa.String(), nullable=False),
    sa.Column('last_request', sa.DateTime(timezone=True), nullable=False),
    sa.Column('request_count', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('encrypted_token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('api_keys')
    # ### end Alembic commands ###
