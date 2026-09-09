from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.categoria import Categoria
from app.schemas.categoria import CategoriaCreate, CategoriaResponse
from app.services.auth import get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.get("/", response_model=List[CategoriaResponse])
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).order_by(Categoria.id).all()


@router.post(
    "/crearCategoria",
    response_model=CategoriaResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_current_user)],
)
def crear_categoria(datos: CategoriaCreate, db: Session = Depends(get_db)):
    nombre = datos.nombre.strip()
    existe = db.query(Categoria).filter(Categoria.nombre == nombre).first()
    if existe is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con ese nombre",
        )

    nueva = Categoria(
        nombre=nombre,
        descripcion=datos.descripcion.strip() if datos.descripcion else None,
        activo=datos.activo,
    )
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva
