from models.torneio import Torneio
from models.usuario import Usuario
from models.torneio_usuario import TorneioUsuario
from models.fase import Fase
from sqlalchemy.orm import Session
from enums.enums_torneio import *
from sqlalchemy import select

class TorneioRepository:

    def __init__(self, session: Session):
        self.session = session

    def listar(self) -> list[Torneio]:
        return self.session.query(Torneio).all()
    
    def buscart_torneio_por_id(self, usuario_id: int) -> Torneio | None:
        return self.session.get(Torneio, usuario_id)
    
    def busar_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        return self.session.get(Usuario, usuario_id)
    
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
    

    def adicionar_particiapacao_usuario(self, participacao: TorneioUsuario) -> TorneioUsuario:         
        self.session.add(participacao)
        self.session.commit()
        self.session.refresh(participacao)

        return participacao
    
    def listar_participantes(self, torneio_id: int) -> list[TorneioUsuario]:
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