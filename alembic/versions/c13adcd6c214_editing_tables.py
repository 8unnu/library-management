"""editing tables

Revision ID: c13adcd6c214
Revises: 85993e159cf9
Create Date: 2025-01-13 17:02:35.572300

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c13adcd6c214'
down_revision: Union[str, None] = '85993e159cf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('borrowed_books',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('book_title', sa.String(), nullable=True),
    sa.Column('taken_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
    sa.Column('back_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['book_title'], ['books.title'], ),
    sa.ForeignKeyConstraint(['user_name'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('is_admin', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('quan_books_taken', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'quan_books_taken')
    op.drop_column('users', 'is_admin')
    op.drop_table('borrowed_books')
    # ### end Alembic commands ###
