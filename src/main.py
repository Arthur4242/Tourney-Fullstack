from database.database import engine, SessionLocal
from models.usuario import *
from models.time import *
from models.torneio import *
from models.usuario_time import *
from models.torneio_time import *
from enums.tipo_torneio import *
from models.base import Base
from sqlalchemy import select


# Criar as Entidades
Base.metadata.create_all(engine)

session = SessionLocal()


arthur = Usuario(nome="Arthur")
flamengo = Time(nome="Flamengo")
bostaclube = Time(nome="Bostaclube")

participacao = UsuarioTime(
    usuario=arthur,
    time=flamengo
)

participacao2 = UsuarioTime(
    usuario=arthur,
    time=bostaclube
)

session.add(participacao)
session.add(arthur)
session.commit()


timao = session.scalars(
    select(Time).where(Time.id == 2)
).one()


torneio = Torneio(nome ="hentai da silva", tipo = TipoTorneio.EQUIPE)

time_participacao = TorneioTime(
    time=timao,
    torneio=torneio

)

# session.add(torneio)
session.add(time_participacao)
session.commit()

campeonatos = session.scalars(
    select(Torneio)
).all()

for campeonato in campeonatos:
    print(campeonato.nome)
    print()
    for p in campeonato.times_participantes:
        print(p.time.nome)
    print()

# for time in times:
#     print(time.nome)
#     print(time.id)
#     print("Membros")
#     for integrante in time.integrantes:
#         print(integrante.nome)
    

