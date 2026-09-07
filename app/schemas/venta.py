from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class DetalleVentaCreate(BaseModel):
    id_producto: int
    cantidad: int = Field(..., gt=0)


class VentaCreate(BaseModel):
    detalles: List[DetalleVentaCreate] = Field(..., min_length=1)


class VentaEstado(BaseModel):
    activo: bool


class ProductoVentaResponse(BaseModel):
    id_producto: int
    nombre: str

    model_config = {"from_attributes": True}


class DetalleVentaResponse(BaseModel):
    id_detalle: int
    id_producto: int
    cantidad: int
    precio_unitario: Decimal
    subtotal: Decimal
    producto: ProductoVentaResponse

    model_config = {"from_attributes": True}


class VentaResponse(BaseModel):
    id_venta: int
    id_usuario: int
    total: Decimal
    activo: bool
    fecha_venta: datetime
    detalles: List[DetalleVentaResponse]

    model_config = {"from_attributes": True}
