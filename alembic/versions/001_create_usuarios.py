"""create usuarios

Revision ID: 001_create_usuarios
Revises:
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "001_create_usuarios"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if "usuarios" in inspect(bind).get_table_names():
        return

    op.create_table(
        "usuarios",
        sa.Column("id_usuario", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("rol", sa.String(length=50), nullable=False, server_default="usuario"),
        sa.Column(
            "fecha_registro",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id_usuario"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_usuarios_id_usuario"), "usuarios", ["id_usuario"], unique=False)
    op.create_index(op.f("ix_usuarios_email"), "usuarios", ["email"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    if "usuarios" not in inspect(bind).get_table_names():
        return

    op.drop_index(op.f("ix_usuarios_email"), table_name="usuarios")
    op.drop_index(op.f("ix_usuarios_id_usuario"), table_name="usuarios")
    op.drop_table("usuarios")
