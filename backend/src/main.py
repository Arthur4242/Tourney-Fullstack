from backend.src.database.database import engine, SessionLocal

from backend.src.models.usuario import *
from backend.src.models.time import *
from backend.src.models.torneio import *
from backend.src.models.usuario_time import *
from backend.src.models.torneio_time import *
from backend.src.models.torneio_usuario import *

from backend.src.enums.enums_torneio import TipoTorneio, EstadoTorneio
from backend.src.enums.enums_fase import TipoFase

from backend.src.repositories.usuario_repository import UsuarioRepository
from backend.src.repositories.torneiro_repository import TorneioRepository

from service.usuario_serivce import UsuarioService
from service.torneio_service import TorneioService
from backend.src.models.base import Base
from sqlalchemy import select

# Criar as Entidades
Base.metadata.create_all(engine)

# Session e repositorios
session = SessionLocal()

userRepository = UsuarioRepository(session)
user_service = UsuarioService(userRepository)

torneio_repository = TorneioRepository(session)
torneio_service = TorneioService(torneio_repository) 



# torneio = torneio_service.cadastrar_torneio(
#     nome = "Copa1",
#     tipo = TipoTorneio.INDIVIDUAL
# )

# torneio_service.abrir_inscricoes(torneio)

# nomes = [
#     'Arthur',
#     'Cleiton',
#     'Jhon',
#     'Ronaldo'
# ]
# usuarios = [user_service.cadastrarUsuario(n) for n in nomes] 
# for user in usuarios:
#     torneio_service.adicionar_usuario_torneio(user, torneio)


# torneio_service.encerrar_inscricoes(torneio)
# torneio_service.inicar_torneio(torneio)


# participantes = torneio_service.listar_participantes_torneio(torneio)

# print("Participantes")
# for p in participantes:
#     print(p.nome)


for t in torneio_service.listar_torneios():
    print(t.nome)

copa1 = torneio_service.buscar_torneio_por_nome("Copa1")
torneio_service.adicionar_fase_mata_mata(copa1, 1)
torneio_service.iniciar_chaveamento(copa1)

fase_mata_mata = torneio_repository.buscar_fase_por_tipo(copa1, TipoFase.MATA_MATA)
rodada_atual = torneio_service.listar_rodadas(fase_mata_mata)[-1]

partidas = torneio_service.listar_partidas(rodada_atual)

for p in partidas:
    print(p.jogador1.nome + " vs " + p.jogador2.nome)