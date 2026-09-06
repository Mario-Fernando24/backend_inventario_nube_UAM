from pydantic import BaseModel, EmailStr, Field


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str


class UsuarioResponse(BaseModel):
    id_usuario: int
    nombre: str
    email: EmailStr
    rol: str

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str
