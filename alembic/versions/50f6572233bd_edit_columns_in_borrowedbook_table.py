"""edit columns in borrowedBook table

Revision ID: 50f6572233bd
Revises: 50389e0c7476
Create Date: 2025-01-16 14:42:34.639027

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50f6572233bd'
down_revision: Union[str, None] = '50389e0c7476'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed_books', sa.Column('username', sa.String(), nullable=True))
    op.add_column('borrowed_books', sa.Column('quantity_book_taken', sa.Integer(), nullable=True))
    op.drop_constraint('borrowed_books_user_name_fkey', 'borrowed_books', type_='foreignkey')
    op.create_foreign_key(None, 'borrowed_books', 'users', ['username'], ['username'])
    op.drop_column('borrowed_books', 'user_name')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('borrowed_books', sa.Column('user_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'borrowed_books', type_='foreignkey')
    op.create_foreign_key('borrowed_books_user_name_fkey', 'borrowed_books', 'users', ['user_name'], ['username'])
    op.drop_column('borrowed_books', 'quantity_book_taken')
    op.drop_column('borrowed_books', 'username')
    # ### end Alembic commands ###
