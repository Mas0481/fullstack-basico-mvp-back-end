"""Cria tabela funcionarios

Revision ID: 001_initial
Revises:
Create Date: 2026-06-20

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "funcionarios",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nome", sa.String(), nullable=False),
        sa.Column("data_nascimento", sa.Date(), nullable=False),
        sa.Column("genero", sa.String(), nullable=True),
        sa.Column("cpf", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=True),
        sa.Column("telefone", sa.String(), nullable=True),
        sa.Column("cargo", sa.String(), nullable=False),
        sa.Column("departamento", sa.String(), nullable=False),
        sa.Column("data_admissao", sa.Date(), nullable=False),
        sa.Column("salario", sa.Numeric(12, 2), nullable=True),
        sa.Column("tipo_contrato", sa.String(), nullable=True),
        sa.Column("horario_entrada", sa.Time(), nullable=True),
        sa.Column("horario_saida_almoco", sa.Time(), nullable=True),
        sa.Column("horario_retorno_almoco", sa.Time(), nullable=True),
        sa.Column("horario_saida", sa.Time(), nullable=True),
        sa.Column("dias_trabalho", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cpf"),
    )


def downgrade() -> None:
    op.drop_table("funcionarios")
