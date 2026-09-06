from fastapi import FastAPI

app = FastAPI(
    title="API Gestión de Inventarios",
    description="Backend para el sistema de gestión de inventarios",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensaje": "API de inventarios funcionando"
    }