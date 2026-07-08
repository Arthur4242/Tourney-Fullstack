from models.usuario import Usuario
from models.torneio import Torneio
from models.torneio_usuario import TorneioUsuario
from repositories.usuario_repository import UsuarioRepository
from repositories.torneiro_repository import TorneioRepository
from enums.enums_torneio import EstadoTorneio, TipoTorneio

class TorneioService:

    def __init__(self, torneio_repository: TorneioRepository):
        self.torneio_repository = torneio_repository

    def cadastrar_torneio(self, nome: str, tipo: TipoTorneio):
        torneio = Torneio(
            nome=nome,
            tipo=tipo
        )
        return self.torneio_repository.adicionar_torneio(torneio)
    
    def deletar_torneio(self, torneio: Torneio):
        self.torneio_repository.deletar_torneio(torneio)

    def alterar_estado(self, torneio: Torneio, estado: EstadoTorneio):
        if torneio.estado == estado:
            raise ValueError(
                f"O torneio já se encontra no estado {estado.value}."
            )
        
        torneio.estado = estado

        return self.torneio_repository.salvar(torneio)
        


    def adicionar_usuario_torneio(self, usuario: Usuario, torneio: Torneio):
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

        self.torneio_repository.adicionar_particiapacao_usuario(participacao)

    def remover_usuario_torneio(self, usuario: Usuario, torneio: Torneio):
        p: TorneioUsuario | None = self.torneio_repository.procurar_participacao(usuario, torneio)
        
        if p is None:
            raise ValueError("O usuário não está participando do torneio")
        
        self.torneio_repository.remover_participacao_usuario(p)


    # Alterar etapa do torneio

    def abrir_inscricoes(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.CRIADO:
            raise ValueError("Não é possível abrir as incrições.")
        
        self.alterar_estado(torneio, EstadoTorneio.INSCRICOES_ABERTAS)

    def encerrar_inscricoes(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.INSCRICOES_ABERTAS:
            raise ValueError("As inscrições não foram abertas para encerrar.")
        
        self.alterar_estado(torneio, EstadoTorneio.INSCRICOES_ENCERRADAS)

    def inicar_torneio(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.INSCRICOES_ENCERRADAS:
            raise ValueError("Não é possível iniciar o torneio.")

        self.alterar_estado(torneio, EstadoTorneio.EM_ANDAMENTO)

    def finalizar_torneio(self, torneio: Torneio):
        if torneio.estado != EstadoTorneio.EM_ANDAMENTO:
            raise ValueError("O torneio não está em andamento para finalizar.")
        self.alterar_estado(torneio, EstadoTorneio.FINALIZADO)

    def cancelar_torneio(self, torneio: Torneio):
        self.alterar_estado(torneio, EstadoTorneio.CANCELADO)

    