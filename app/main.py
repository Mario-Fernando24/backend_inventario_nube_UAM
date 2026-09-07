from fastapi import FastAPI

from app.routers import auth, categorias, productos, usuarios

app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para el sistema de gestión de inventarios",
    version="1.0.0",
)

app.include_router(usuarios.router)
app.include_router(auth.router)
app.include_router(categorias.router)
app.include_router(productos.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de inventarios funcionando"
    }
