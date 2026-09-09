from fastapi import FastAPI
from app.database import engine, Base
from app import models
from app.routers import auth, categorias, productos, usuarios, ventas

# Genera en PostgreSQL todas las tablas declaradas si no existen al iniciar la app
try:
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas exitosamente en la base de datos.")
except Exception as e:
    print(f"Error al crear las tablas en la base de datos: {e}")

app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para el sistema de gestión de inventarios",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(productos.router)
app.include_router(ventas.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de inventarios funcionando"
    }