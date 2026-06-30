from database.database import engine, SessionLocal
from models.usuario import *
from models.time import *
from models.torneio import *
from models.usuario_time import *
from models.torneio_time import *
from models.torneio_usuario import *
from enums.tipo_torneio import *
from repositories.usuario_repository import UsuarioRepository

from models.base import Base
from sqlalchemy import select


# Criar as Entidades
Base.metadata.create_all(engine)

session = SessionLocal()
userRepository = UsuarioRepository(session)

userRepository.adicionarUsuario("Cleiton", "teste@email.com")
userRepository.adicionarUsuario("Arthur")

usuarios: list[Usuario] = userRepository.listar()
for u in usuarios:
    print(u.nome)
    print(u.email)


session.close()