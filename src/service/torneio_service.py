from models.usuario import Usuario
from models.torneio import Torneio
from models.torneio_usuario import TorneioUsuario
from repositories.usuario_repository import UsuarioRepository
from repositories.torneiro_repository import TorneioRepository
from enums.enums_torneio import EstadoTorneio, TipoTorneio

class TorneioService:

    def __init__(self, torneio_repository: TorneioRepository):
        self.torneio_repository = torneio_repository

    def cadastrarTorneio(self, nome: str, tipo: TipoTorneio):
        torneio = Torneio(
            nome=nome,
            tipo=tipo
        )
        return self.torneio_repository.adicionarTorneio(torneio)
    
    def deletarTorneio(self, torneio: Torneio):
        self.deletarTorneio(torneio)

    def alterarEstado(self, torneio: Torneio, estado: EstadoTorneio):
        if torneio.estado == estado:
            raise ValueError(
                f"O torneio já se encontra no estado {estado.value}."
            )
        
        torneio.estado = estado

        return self.torneio_repository.salvar(torneio)
        


    def adicionarUsuarioTorneio(self, usuario: Usuario, torneio: Torneio):
        if torneio.tipo != TipoTorneio.INDIVIDUAL:
            raise ValueError("Não é possível cadastrar um indivídio nesse torneio")
        
        if torneio.estado != EstadoTorneio.INSCRICOES_ABERTAS:
            raise ValueError(
                "Não é possível adicionar participantes. As inscrições não estão abertas."
            )

        participacao = TorneioUsuario(
            usuario_id = usuario.id,
            torneio_id = torneio.id,
            usuario = usuario,
            torneio = torneio
        )

        self.torneio_repository.adicionarParticiapacaoUsuario(participacao)

    def removerUsuarioTorneio(self, usuario: Usuario, torneio: Torneio):
        p: TorneioUsuario | None = self.torneio_repository.procurarParticipacao(usuario, torneio)
        
        if p is None:
            raise ValueError("O usuário não está participando do torneio")
        
        self.torneio_repository.removerParticipacaoUsuario(p)


    # Alterar etapa do torneio

    def abrirInscricoes(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.CRIADO:
            raise ValueError("Não é possível abrir as incrições.")
        
        self.alterarEstado(torneio, EstadoTorneio.INSCRICOES_ABERTAS)

    def encerrarInscricoes(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.INSCRICOES_ABERTAS:
            raise ValueError("As inscrições não foram abertas para encerrar.")
        
        self.alterarEstado(torneio, EstadoTorneio.INSCRICOES_ENCERRADAS)

    def inicarTorneio(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.INSCRICOES_ENCERRADAS:
            raise ValueError("Não é possível iniciar o torneio.")

        self.alterarEstado(torneio, EstadoTorneio.EM_ANDAMENTO)

    def finalizarTorneio(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.EM_ANDAMENTO:
            raise ValueError("O torneio não está em andamento para finalizar.")
        self.alterarEstado(torneio, EstadoTorneio.FINALIZADO)

    def cancelarTorneio(self, torneio: Torneio):
        self.alterarEstado(torneio, EstadoTorneio.CANCELADO)