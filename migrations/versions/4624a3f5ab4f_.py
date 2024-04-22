"""empty message

Revision ID: 4624a3f5ab4f
Revises: 
Create Date: 2024-04-11 10:24:14.433735

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4624a3f5ab4f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('demo_case',
    sa.Column('title', sa.VARCHAR(length=128), nullable=False),
    sa.Column('date_created', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('body', sa.String(), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('length(title) >= 2'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('demo_user',
    sa.Column('email', sa.VARCHAR(length=128), nullable=False),
    sa.Column('password', sa.CHAR(length=60), nullable=False),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('length(email) >= 5'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('demo_comment',
    sa.Column('text', sa.VARCHAR(length=128), nullable=False),
    sa.Column('date_created', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('case_id', sa.INTEGER(), nullable=True),
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.CheckConstraint('length(text) >= 2'),
    sa.ForeignKeyConstraint(['case_id'], ['demo_case.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_demo_comment_case_id'), 'demo_comment', ['case_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_demo_comment_case_id'), table_name='demo_comment')
    op.drop_table('demo_comment')
    op.drop_table('demo_user')
    op.drop_table('demo_case')
    # ### end Alembic commands ###
