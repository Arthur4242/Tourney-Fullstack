from models.torneio import Torneio
from models.usuario import Usuario
from models.torneio_usuario import TorneioUsuario
from sqlalchemy.orm import Session
from enums.tipo_torneio import *


class TorneioRepository:

    def __init__(self, session: Session):
        self.session = session

    def listar(self):
        return self.session.query(Torneio).all()
    
    def buscarty_torneio_por_id(self, usuario_id: int) -> Torneio | None:
        return self.session.get(Torneio, usuario_id)
    
    def busar_usuario_por_id(self, usuario_id: int) -> Usuario | None:
        return self.session.get(Usuario, usuario_id)
    
    def adicionarTorneio(self, nome: str, tipo: TipoTorneio | None = None) ->Torneio:
        torneio = Torneio(
            nome = nome,
            tipo = tipo
        )

        self.session.add(torneio)
        self.session.commit()
        self.session.refresh(torneio)

        return torneio
    
    
    def deletartorneio(self, torneio_id) -> None:
        torneio = self.buscar_torneio_por_id(torneio_id)

        if torneio is None:
            return False
        
        self.session.delete(torneio)
        self.session.commit()
        return True
    
    def salvar(self, torneio: Torneio) -> Torneio:
        self.session.commit()
        self.session.refresh(torneio)
        return torneio
    

    def adicionarParticiapacaoUsuario(self, torneio: Torneio, usuario: Usuario):
        
        participacao = TorneioUsuario(
            usuario_id = usuario.id,
            torneio_id = torneio.id,
            usuario = usuario,
            torneio = torneio
        )
         
        self.session.add(participacao)
        self.session.commit()
        self.session.refresh(participacao)

        return participacao
    
    def removerParticipacaoUsuario(self, torneio: Torneio, usuario: Usuario):

        participacao = TorneioUsuario(
            usuario_id = usuario.id,
            torneio_id = torneio.id,
            usuario = usuario,
            torneio = torneio
        )

        self.session.delete(participacao)
        self.session.commit()