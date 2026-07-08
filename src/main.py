from database.database import engine, SessionLocal
from models.usuario import *
from models.time import *
from models.torneio import *
from models.usuario_time import *
from models.torneio_time import *
from models.torneio_usuario import *
from enums.enums_torneio import *
from repositories.usuario_repository import UsuarioRepository
from service.usuario_serivce import UsuarioService

from models.base import Base
from sqlalchemy import select

# Criar as Entidades
Base.metadata.create_all(engine)

# Session e repositorios
session = SessionLocal()
userRepository = UsuarioRepository(session)
userService = UsuarioService(userRepository)

