from fastapi import FastAPI
from app.routers import auth, categorias, productos, usuarios, ventas

# Creación dinámica y segura de tablas para evitar caídas en el startup
try:
    from app.database import engine, Base
    import app.models
    Base.metadata.create_all(bind=engine)
    print("Tablas verificadas/creadas exitosamente.")
except Exception as e:
    print(f"Advertencia: No se pudieron auto-crear las tablas al iniciar: {e}")

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