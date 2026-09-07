from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from app.schemas.categoria import CategoriaResponse


class ProductoCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: Decimal = Field(..., gt=0)
    stock: int = Field(0, ge=0)
    id_categoria: int
    activo: bool = True


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    precio: Optional[Decimal] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    id_categoria: Optional[int] = None


class ProductoEstado(BaseModel):
    activo: bool


class ProductoResponse(BaseModel):
    id_producto: int
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    stock: int
    id_categoria: int
    activo: bool
    categoria: CategoriaResponse

    model_config = {"from_attributes": True}
