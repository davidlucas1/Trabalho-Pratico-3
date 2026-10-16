"""criar tabelas livros e emprestimos

Revision ID: 101492953d6a
Revises: 
Create Date: 2026-10-16 11:54:35.812744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '101492953d6a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('livros',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('titulo', sa.String(), nullable=False),
    sa.Column('autor', sa.String(), nullable=False),
    sa.Column('ano', sa.Integer(), nullable=False),
    sa.Column('disponivel', sa.Boolean(), server_default=sa.text('1'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('emprestimos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nome_aluno', sa.String(), nullable=False),
    sa.Column('data_emprestimo', sa.Date(), server_default=sa.text('(CURRENT_DATE)'), nullable=False),
    sa.Column('data_devolucao', sa.Date(), nullable=True),
    sa.Column('livro_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['livro_id'], ['livros.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('emprestimos')
    op.drop_table('livros')
