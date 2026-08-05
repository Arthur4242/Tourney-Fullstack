from fastapi import APIRouter
from fastapi import Depends

from backend.src.api.schemas.usuario import (
    CriarUsuarioRequest,
    UsuarioResponse
)
from backend.src.services.usuario_serivce import UsuarioService


from backend.src.api.dependencies import get_usuario_service

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)


@router.post("/", response_model=UsuarioResponse)
def criar_usuario(
    user: CriarUsuarioRequest,
    usuario_service: UsuarioService = Depends(get_usuario_service)
):
    usuario = usuario_service.cadastrar_usuario(user.nome, user.email)
    
    return UsuarioResponse(
        id=usuario.id,
        nome=usuario.nome,
        email=usuario.email
    )

