from database.database import engine, SessionLocal

from models.usuario import *
from models.time import *
from models.torneio import *
from models.usuario_time import *
from models.torneio_time import *
from models.torneio_usuario import *

from enums.enums_torneio import TipoTorneio, EstadoTorneio

from repositories.usuario_repository import UsuarioRepository
from repositories.torneiro_repository import TorneioRepository

from service.usuario_serivce import UsuarioService
from service.torneio_service import TorneioService
from models.base import Base
from sqlalchemy import select

# Criar as Entidades
Base.metadata.create_all(engine)

# Session e repositorios
session = SessionLocal()

userRepository = UsuarioRepository(session)
user_service = UsuarioService(userRepository)

torneio_repository = TorneioRepository(session)
torneio_service = TorneioService(torneio_repository)

torneio = torneio_service.cadastrar_torneio(
    nome = "Copa3",
    tipo = TipoTorneio.INDIVIDUAL
)

for t in torneio_service.listar_torneios():
    print(t.nome)






