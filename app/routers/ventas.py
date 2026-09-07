from collections import defaultdict
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.producto import Producto
from app.models.usuario import Usuario
from app.models.venta import DetalleVenta, Venta
from app.schemas.venta import VentaCreate, VentaEstado, VentaResponse
from app.services.auth import get_current_user

router = APIRouter(
    prefix="/ventas",
    tags=["Ventas"],
    dependencies=[Depends(get_current_user)],
)


def _cargar_venta(id_venta: int, db: Session) -> Venta:
    venta = (
        db.query(Venta)
        .options(
            joinedload(Venta.detalles).joinedload(DetalleVenta.producto),
        )
        .filter(Venta.id_venta == id_venta)
        .first()
    )
    if venta is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La venta no existe",
        )
    return venta


@router.post("/crearVenta", response_model=VentaResponse, status_code=status.HTTP_201_CREATED)
def crear_venta(
    datos: VentaCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(get_current_user),
):
    cantidades = defaultdict(int)
    for item in datos.detalles:
        cantidades[item.id_producto] += item.cantidad

    detalles_creados = []
    total = Decimal("0.00")

    for id_producto, cantidad in cantidades.items():
        producto = (
            db.query(Producto)
            .filter(Producto.id_producto == id_producto)
            .with_for_update()
            .first()
        )
        if producto is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto {id_producto} no existe",
            )
        if not producto.activo:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El producto {producto.nombre} no está activo",
            )
        if producto.stock < cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Stock insuficiente para {producto.nombre}. "
                    f"Disponible: {producto.stock}, solicitado: {cantidad}"
                ),
            )

        precio_unitario = Decimal(producto.precio)
        subtotal = precio_unitario * cantidad
        total += subtotal
        producto.stock -= cantidad

        detalles_creados.append(
            DetalleVenta(
                id_producto=id_producto,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                subtotal=subtotal,
            )
        )

    venta = Venta(
        id_usuario=usuario.id_usuario,
        total=total,
        activo=True,
        detalles=detalles_creados,
    )
    db.add(venta)
    db.commit()
    return _cargar_venta(venta.id_venta, db)


@router.get("/", response_model=List[VentaResponse])
def listar_ventas(activo: Optional[bool] = None, db: Session = Depends(get_db)):
    consulta = db.query(Venta).options(
        joinedload(Venta.detalles).joinedload(DetalleVenta.producto),
    )
    if activo is not None:
        consulta = consulta.filter(Venta.activo == activo)
    return consulta.order_by(Venta.id_venta.desc()).all()


@router.get("/obtenerVenta/{id_venta}", response_model=VentaResponse)
def obtener_venta(id_venta: int, db: Session = Depends(get_db)):
    return _cargar_venta(id_venta, db)


@router.patch("/cambiarEstado/{id_venta}", response_model=VentaResponse)
def cambiar_estado_venta(
    id_venta: int,
    datos: VentaEstado,
    db: Session = Depends(get_db),
):
    venta = _cargar_venta(id_venta, db)
    if venta.activo == datos.activo:
        return venta

    if datos.activo is False:
        for detalle in venta.detalles:
            producto = (
                db.query(Producto)
                .filter(Producto.id_producto == detalle.id_producto)
                .with_for_update()
                .first()
            )
            producto.stock += detalle.cantidad
    else:
        for detalle in venta.detalles:
            producto = (
                db.query(Producto)
                .filter(Producto.id_producto == detalle.id_producto)
                .with_for_update()
                .first()
            )
            if producto is None or not producto.activo:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se puede reactivar: un producto ya no está disponible",
                )
            if producto.stock < detalle.cantidad:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stock insuficiente para reactivar la venta ({producto.nombre})",
                )
            producto.stock -= detalle.cantidad

    venta.activo = datos.activo
    db.commit()
    return _cargar_venta(id_venta, db)
