"""create ventas y detalle_ventas

Revision ID: 004_create_ventas
Revises: 003_create_productos
Create Date: 2026-09-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = "004_create_ventas"
down_revision: Union[str, Sequence[str], None] = "003_create_productos"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    tablas = inspect(bind).get_table_names()

    if "ventas" not in tablas:
        op.create_table(
            "ventas",
            sa.Column("id_venta", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_usuario", sa.Integer(), nullable=False),
            sa.Column("total", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.Column("activo", sa.Boolean(), nullable=False, server_default=sa.true()),
            sa.Column(
                "fecha_venta",
                sa.DateTime(timezone=True),
                server_default=sa.func.now(),
                nullable=False,
            ),
            sa.ForeignKeyConstraint(["id_usuario"], ["usuarios.id_usuario"]),
            sa.PrimaryKeyConstraint("id_venta"),
        )
        op.create_index(op.f("ix_ventas_id_venta"), "ventas", ["id_venta"], unique=False)
        op.create_index(op.f("ix_ventas_id_usuario"), "ventas", ["id_usuario"], unique=False)

    if "detalle_ventas" not in inspect(bind).get_table_names():
        op.create_table(
            "detalle_ventas",
            sa.Column("id_detalle", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("id_venta", sa.Integer(), nullable=False),
            sa.Column("id_producto", sa.Integer(), nullable=False),
            sa.Column("cantidad", sa.Integer(), nullable=False),
            sa.Column("precio_unitario", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.Column("subtotal", sa.Numeric(precision=12, scale=2), nullable=False),
            sa.ForeignKeyConstraint(["id_venta"], ["ventas.id_venta"]),
            sa.ForeignKeyConstraint(["id_producto"], ["productos.id_producto"]),
            sa.PrimaryKeyConstraint("id_detalle"),
        )
        op.create_index(op.f("ix_detalle_ventas_id_detalle"), "detalle_ventas", ["id_detalle"], unique=False)
        op.create_index(op.f("ix_detalle_ventas_id_venta"), "detalle_ventas", ["id_venta"], unique=False)
        op.create_index(op.f("ix_detalle_ventas_id_producto"), "detalle_ventas", ["id_producto"], unique=False)


def downgrade() -> None:
    bind = op.get_bind()
    tablas = inspect(bind).get_table_names()

    if "detalle_ventas" in tablas:
        op.drop_index(op.f("ix_detalle_ventas_id_producto"), table_name="detalle_ventas")
        op.drop_index(op.f("ix_detalle_ventas_id_venta"), table_name="detalle_ventas")
        op.drop_index(op.f("ix_detalle_ventas_id_detalle"), table_name="detalle_ventas")
        op.drop_table("detalle_ventas")

    if "ventas" in inspect(bind).get_table_names():
        op.drop_index(op.f("ix_ventas_id_usuario"), table_name="ventas")
        op.drop_index(op.f("ix_ventas_id_venta"), table_name="ventas")
        op.drop_table("ventas")
