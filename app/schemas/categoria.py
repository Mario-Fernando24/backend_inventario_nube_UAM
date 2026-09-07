from typing import Optional

from pydantic import BaseModel


class CategoriaResponse(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str] = None
    activo: bool

    model_config = {"from_attributes": True}
