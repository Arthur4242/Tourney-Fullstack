from fastapi import Depends

from backend.src.database.database import engine, SessionLocal

from backend.src.repositories.usuario_repository import UsuarioRepository
from backend.src.repositories.torneiro_repository import TorneioRepository

from backend.src.services.usuario_serivce import UsuarioService
from backend.src.services.torneio_service import TorneioService

def get_session():
    session = SessionLocal()
    return session

    
def get_usuario_repository(
        session = Depends(get_session)
    ):

    return UsuarioRepository(session)

def get_usuario_service(
        repository = Depends(get_usuario_repository)
):
    return UsuarioService(repository)


def get_torneio_repository(
        session = Depends(get_session),
):

    return TorneioRepository(session)

def get_torneio_service(
        torneio_repository = Depends(get_usuario_repository),
        user_repository = Depends(get_usuario_repository)
):
    return TorneioService(torneio_repository, user_repository)
