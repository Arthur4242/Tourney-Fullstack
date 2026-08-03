from pydantic import BaseModel

class CriarUsuarioRequest(BaseModel):
    nome: str
    email: str | None = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str | None = None