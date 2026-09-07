from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.routers.usuarios import leer_usuario_actual
from app.schemas.usuario import Token, UsuarioLogin
from app.services.auth import create_access_token, get_current_user, verify_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=Token)
def login(datos: UsuarioLogin, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == datos.email).first()

    print(f"Usuario encontrado: {usuario}")  # Depuración: imprime el usuario encontrado
    # valida si el usuario existe y si la contraseña es correcta
    # 
    if usuario is None or not verify_password(datos.password, usuario.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"Usuario autenticado: {usuario}")  # Depuración: imprime el usuario autenticado

    access_token = create_access_token(
        {
            "id_usuario": usuario.id_usuario,
            "email": usuario.email,
            "rol": usuario.rol,
        }
    )

    usuarioLogueado =  leer_usuario_actual(usuario=usuario)  # Llama a la función para obtener el usuario actual

    print(f"Usuario logueado: {usuarioLogueado.nombre}")  # Depuración: imprime el usuario logueado
  

    return {"usuario": usuarioLogueado, "access_token": access_token, "token_type": "bearer"}
