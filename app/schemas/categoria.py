from typing import Optional

from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = Field(None, max_length=255)
    activo: bool = True


class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool

    model_config = {"from_attributes": True}
