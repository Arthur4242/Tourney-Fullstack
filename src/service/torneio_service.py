from models.usuario import Usuario
from models.torneio import Torneio
from models.torneio_usuario import TorneioUsuario
from models.fase_mata_mata import FaseMataMata
from models.rodada import Rodada
from models.partida import Partida
from models.fase import Fase

from repositories.torneiro_repository import TorneioRepository
from enums.enums_torneio import EstadoTorneio, TipoTorneio
from enums.enums_fase import TipoFase

import random

class TorneioService:

    def __init__(self, torneio_repository: TorneioRepository):
        self.torneio_repository = torneio_repository

    # CRUD

    def cadastrar_torneio(self, nome: str, tipo: TipoTorneio):
        torneio = Torneio(
            nome=nome,
            tipo=tipo,
            estado=EstadoTorneio.CRIADO
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

    
    def adicionar_fase_mata_mata(self, torneio: Torneio, melhor_de: int) -> Torneio:

        if melhor_de <= 0 or melhor_de % 2 == 0:
            raise ValueError("Melhor de deve ser um número ímpar maior que zero.")
        
        fase = FaseMataMata(
            tipo=TipoFase.MATA_MATA,
            melhor_de=melhor_de
        )

        torneio.fases_torneio.append(fase)

        
        torneio = self.torneio_repository.salvar(torneio)

        return torneio


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

    def listar_torneios(self) -> list[Torneio]:
        return self.torneio_repository.listar()
    
    def finalizar_partida(self, partida: Partida, vencedor: Usuario):

        if vencedor is not partida.jogador1 or partida.jogador2:
            print("Este usuário não faz parte desta partida")

        partida.vencedor = vencedor

    def verificar_fim_da_rodada(self, rodada: Rodada) -> bool:
        return all(partida.vencedor is not None for partida in rodada.partidas)
    
    # Lógica de Torneio

    def iniciar_chaveamento(self, torneio: Torneio):
                
        if torneio.fases_torneio.len() == 0:
            raise ValueError("As fases do torneio ainda não foram preenchidas")

        for fase in torneio.fases_torneio:
            
            match fase.tipo:
                
                case TipoFase.MATA_MATA:
                    
                    participantes = list(torneio.usuarios_participantes)
                    random.shuffle(participantes)

                    rodada = Rodada()

                    while len(participantes) >= 2:
                        jogador1 = participantes.pop()
                        jogador2 = participantes.pop()

                        partida = Partida(
                            jogador1 = jogador1,
                            jogador2 = jogador2
                        )
                        rodada.partidas.append(partida)

                    # Caso sobrar um participante

                    if participantes:
                        jogador = participantes.pop()

                        partida = Partida(
                            jogador1=jogador,
                            jogador2=None,
                            vencedor=jogador
                        )

                        rodada.partidas.append(partida)

                    fase.append(rodada)

                case TipoFase.SWISS:
                    # lógica de chaveamento para swiss
                    pass
        
        # Salvar após chaveamento inicial
        self.torneio_repository.salvar(torneio)
        return torneio

    # Lógica de mata_mata

    def criar_proxima_rodada_mata_mata(self, rodada_atual: Rodada):
        
        vencedores = [
            partida.vencedor
            for partida in rodada_atual.partidas
        ]

        # Varificar se há apenas um vencedor e o torneio terminou
        if len(vencedores) == 1:
            # Corrigir futuramente
            # rodada_atual.fase.torneio. = vencedores[0]
            # torneio.estado = EstadoTorneio.FINALIZADO
            return ("O torneio terminou e o campeão é" + vencedores[0].nome)

        nova_rodada = Rodada()

        for i in range(0, len(vencedores), 2):
            partida = Partida(
                jogador1 = vencedores[i],
                jogador2 = vencedores[i + 1]
            )
            nova_rodada.partidas.append(partida)

        return nova_rodada
    
