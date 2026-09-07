"""create productos con relacion a categorias

Revision ID: 003_create_productos
Revises: 002_create_categorias
Create Date: 2026-09-06

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "003_create_productos"
down_revision: Union[str, Sequence[str], None] = "002_create_categorias"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    if "productos" in inspect(bind).get_table_names():
        return

    op.create_table(
        "productos",
        sa.Column("id_producto", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("descripcion", sa.String(length=255), nullable=True),
        sa.Column("precio", sa.Numeric(precision=12, scale=2), nullable=False),
        sa.Column("stock", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("id_categoria", sa.Integer(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column(
            "fecha_registro",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["id_categoria"], ["categorias.id"]),
        sa.PrimaryKeyConstraint("id_producto"),
    )
    op.create_index(op.f("ix_productos_id_producto"), "productos", ["id_producto"], unique=False)
    op.create_index(op.f("ix_productos_id_categoria"), "productos", ["id_categoria"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    if "productos" not in inspect(bind).get_table_names():
        return

    op.drop_index(op.f("ix_productos_id_categoria"), table_name="productos")
    op.drop_index(op.f("ix_productos_id_producto"), table_name="productos")
    op.drop_table("productos")
