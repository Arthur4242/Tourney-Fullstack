from backend.src.models.torneio import Torneio
from backend.src.models.usuario import Usuario
from backend.src.models.torneio_usuario import TorneioUsuario
from backend.src.models.fase import Fase
from backend.src.models.rodada import Rodada
from backend.src.models.partida import Partida
from sqlalchemy.orm import Session
from backend.src.enums.enums_fase import TipoFase
from sqlalchemy import select

class TorneioRepository:

    def __init__(self, session: Session):
        self.session = session

    def listar(self) -> list[Torneio]:
        return self.session.query(Torneio).all()
    
    def buscart_torneio_por_id(self, torneio_id: int) -> Torneio | None:
        return self.session.get(Torneio, torneio_id)
    
    def buscar_torneio_por_nome(self, nome_torneio: str) -> Torneio | None:
        stmt = (
            select(Torneio)
            .where(Torneio.nome == nome_torneio)
        )
        return self.session.scalars(stmt).first()

    def buscar_partida_por_id(self, partida_id: int):
        return self.session.get(Partida, partida_id)

    
    
    def adicionar_torneio(self, torneio: Torneio) -> Torneio:
        self.session.add(torneio)
        self.session.commit()
        self.session.refresh(torneio)

        return torneio
    
    
    def deletar_torneio(self, torneio) -> None:
        self.session.delete(torneio)
        self.session.commit()
        return True
    
    def salvar(self, torneio: Torneio) -> Torneio:
        self.session.commit()
        self.session.refresh(torneio)
        return torneio
    
    def commit(self):
        self.session.commit()
        

    def listar_partidas(self, rodada: Rodada):
        stmt = (
            select(Partida)
            .where(Partida.rodada == rodada)
        )
        return self.session.scalars(stmt).all()
    
    def listar_rodadas(self, fase: Fase) -> list[Rodada]:
        stmt = (
            select(Rodada)
            .where(Rodada.fase == fase)
        )
        return self.session.scalars(stmt).all()

    def adicionar_particiapacao_usuario(self, participacao: TorneioUsuario) -> TorneioUsuario:         
        self.session.add(participacao)
        self.session.commit()
        self.session.refresh(participacao)

        return participacao
    
    def listar_participantes(self, torneio_id: int) -> list[Usuario]:
        stmt = (
            select(Usuario)
            .join(TorneioUsuario)
            .where(TorneioUsuario.torneio_id == torneio_id)
            )

        return self.session.scalars(stmt).all()
    
    def procurar_participacao(self, usuario: Usuario, torneio: Torneio):
        stmt = (
            select(TorneioUsuario)
            .where(
                TorneioUsuario.torneio_id == torneio.id,
                TorneioUsuario.usuario_id == usuario.id)
        )
        return self.session.scalars(stmt).first()

    def remover_participacao_usuario(self, participacao):
        self.session.delete(participacao)
        self.session.commit()

    def adicionar_fase(self, fase: Fase):
        self.session.add(fase)
        self.session.commit()
        self.session.refresh(fase)

        return fase
    
    def listar_fases(self, torneio: Torneio) ->  list[Fase]:
        stmt = (
            select(Fase)
            .where(Fase.torneio_id == torneio.id)
            )

        return self.session.scalars(stmt).all()
    
    def buscar_fase_por_tipo(self, torneio: Torneio, tipo_fase: TipoFase) -> Fase:
        stmt = (
            select(Fase)
            .where(
                Fase.torneio == torneio,
                Fase.tipo == tipo_fase
            )
        )
        return self.session.scalars(stmt).first()
