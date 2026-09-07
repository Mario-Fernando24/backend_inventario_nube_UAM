from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.categoria import Categoria
from app.models.producto import Producto
from app.schemas.producto import (
    ProductoCreate,
    ProductoEstado,
    ProductoResponse,
    ProductoUpdate,
)

router = APIRouter(prefix="/productos", tags=["Productos"])

#   Verificar si la categoría existe y está activa
def _obtener_categoria_activa(id_categoria: int, db: Session) -> Categoria:
    categoria = db.query(Categoria).filter(Categoria.id == id_categoria).first()
    if categoria is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría no existe",
        )
    if not categoria.activo:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La categoría no está activa",
        )
    return categoria


# Obtener un producto por su ID, incluyendo la categoría asociada   
def _obtener_producto(id_producto: int, db: Session) -> Producto:
    producto = (
        db.query(Producto)
        .options(joinedload(Producto.categoria))
        .filter(Producto.id_producto == id_producto)
        .first()
    )
    if producto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="El producto no existe",
        )
    return producto


#   Crear un nuevo producto
@router.post("/crearProducto", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    _obtener_categoria_activa(producto.id_categoria, db)

    nuevo = Producto(
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        id_categoria=producto.id_categoria,
        activo=producto.activo,
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    db.refresh(nuevo, attribute_names=["categoria"])
    return nuevo


#  Listar todos los productos, con opción de filtrar por estado activo
@router.get("/", response_model=List[ProductoResponse])
def listar_productos(activo: Optional[bool] = None, db: Session = Depends(get_db)):
    consulta = db.query(Producto).options(joinedload(Producto.categoria))
    if activo is not None:
        consulta = consulta.filter(Producto.activo == activo)
    return consulta.order_by(Producto.id_producto).all()


@router.get("/{id_producto}", response_model=ProductoResponse)
def obtener_producto(id_producto: int, db: Session = Depends(get_db)):
    return _obtener_producto(id_producto, db)

# Actualizar un producto existente
@router.put("/actualizarProducto/{id_producto}", response_model=ProductoResponse)
def actualizar_producto(
    id_producto: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
):
    producto = _obtener_producto(id_producto, db)
    cambios = datos.model_dump(exclude_unset=True)

    if "id_categoria" in cambios:
        _obtener_categoria_activa(cambios["id_categoria"], db)

    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    db.commit()
    db.refresh(producto)
    db.refresh(producto, attribute_names=["categoria"])
    return producto


# Cambiar el estado activo de un producto
@router.patch("/cambiarEstado/{id_producto}", response_model=ProductoResponse)
def cambiar_estado_producto(
    id_producto: int,
    datos: ProductoEstado,
    db: Session = Depends(get_db),
):
    producto = _obtener_producto(id_producto, db)
    producto.activo = datos.activo
    db.commit()
    db.refresh(producto)
    db.refresh(producto, attribute_names=["categoria"])
    return producto
