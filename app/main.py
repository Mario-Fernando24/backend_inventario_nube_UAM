from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.models.usuario import Usuario  # noqa: F401
from app.routers import auth, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para el sistema de gestión de inventarios",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(usuarios.router)
app.include_router(auth.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de inventarios funcionando"
    }
