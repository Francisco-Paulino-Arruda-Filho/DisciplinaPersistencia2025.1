"""criacao tabelas autor e livro

Revision ID: 50bdcc957de8
Revises: 
Create Date: 2025-06-06 14:44:52.891259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50bdcc957de8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('autor',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_autor_email'), 'autor', ['email'], unique=False)
    op.create_table('livro',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('autor_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['autor_id'], ['autor.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('livro')
    op.drop_index(op.f('ix_autor_email'), table_name='autor')
    op.drop_table('autor')
    # ### end Alembic commands ###
