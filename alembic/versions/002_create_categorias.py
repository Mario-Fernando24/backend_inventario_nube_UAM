"""create categorias y datos por defecto

Revision ID: 002_create_categorias
Revises: 001_create_usuarios
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "002_create_categorias"
down_revision: Union[str, Sequence[str], None] = "001_create_usuarios"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

categorias_table = sa.table(
    "categorias",
    sa.column("nombre", sa.String),
    sa.column("descripcion", sa.String),
    sa.column("activo", sa.Boolean),
)

CATEGORIAS_INICIALES = [
    {"nombre": "Electrónica", "descripcion": "Productos electrónicos", "activo": True},
    {"nombre": "Hogar", "descripcion": "Productos para el hogar", "activo": True},
    {"nombre": "Oficina", "descripcion": "Productos de oficina", "activo": True},
    {"nombre": "Ropa", "descripcion": "Prendas de vestir", "activo": True},
    {"nombre": "Alimentos", "descripcion": "Productos alimenticios", "activo": True},
]


def upgrade() -> None:
    bind = op.get_bind()
    if "categorias" not in inspect(bind).get_table_names():
        op.create_table(
            "categorias",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("nombre", sa.String(length=100), nullable=False),
            sa.Column("descripcion", sa.String(length=255), nullable=True),
            sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("nombre"),
        )
        op.create_index(op.f("ix_categorias_id"), "categorias", ["id"], unique=False)

    count = bind.execute(sa.text("SELECT COUNT(*) FROM categorias")).scalar()
    if count == 0:
        op.bulk_insert(categorias_table, CATEGORIAS_INICIALES)


def downgrade() -> None:
    bind = op.get_bind()
    if "categorias" not in inspect(bind).get_table_names():
        return

    op.drop_index(op.f("ix_categorias_id"), table_name="categorias")
    op.drop_table("categorias")
