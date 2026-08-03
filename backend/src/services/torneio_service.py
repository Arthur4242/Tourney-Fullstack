from backend.src.models.usuario import Usuario
from backend.src.models.torneio import Torneio
from backend.src.models.torneio_usuario import TorneioUsuario
from backend.src.models.fase_mata_mata import FaseMataMata
from backend.src.models.rodada import Rodada
from backend.src.models.partida import Partida
from backend.src.models.fase import Fase

from backend.src.repositories.torneiro_repository import TorneioRepository
from backend.src.repositories.usuario_repository import UsuarioRepository
from backend.src.enums.enums_torneio import EstadoTorneio, TipoTorneio
from backend.src.enums.enums_fase import TipoFase

import random

class TorneioService:

    def __init__(self, torneio_repository: TorneioRepository, usuario_repository: UsuarioRepository):
        self.torneio_repository = torneio_repository
        self.usuario_repository = usuario_repository


    # CRUD

    def buscar_torneio_por_nome(self, nome: str) -> Torneio:
        torneio = self.torneio_repository.buscar_torneio_por_nome(nome)
        if not torneio:
            raise ValueError("Não há um torneio com este nome.")
        return torneio

    def buscar_torneio_por_id(self, torneio_id: int) -> Torneio:
        torneio = self.torneio_repository.buscart_torneio_por_id(torneio_id)
        if not torneio:
            raise ValueError("Não há um torneio com este id.")
        return torneio

    def buscar_fase_por_tipo(self, torneio: Torneio, tipo_fase: TipoFase) -> Fase:
        fase = self.torneio_repository.buscar_fase_por_tipo(torneio,tipo_fase)
        if not fase:
            raise ValueError("Não existe uma fase desse tipo neste torneio")
        
        return fase

    def cadastrar_torneio(self, nome: str, tipo: TipoTorneio):
        if self.buscar_torneio_por_nome(nome):
            raise ValueError("Já existe um torneio com este nome.")
        
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
        


    def adicionar_usuario_torneio(self, usuario_id: int, torneio_id: int):

        usuario = self.usuario_repository.busar_usuario_por_id(usuario_id)

        if not usuario:
            raise ValueError("Usuario não encontrado.") 

        torneio = self.torneio_repository.buscart_torneio_por_id(torneio_id)

        if not torneio:
            raise ValueError("Torneio não encontrado.")


        if torneio.tipo != TipoTorneio.INDIVIDUAL:
            raise ValueError("Não é possível cadastrar um indivídio nesse torneio")
        
        if torneio.estado != EstadoTorneio.INSCRICOES_ABERTAS:
            raise ValueError(
                "Não é possível adicionar participantes. As inscrições não estão abertas."
            )

        participacao = TorneioUsuario(
            usuario = usuario,
            torneio = torneio
        )

        return self.torneio_repository.adicionar_particiapacao_usuario(participacao)

    def remover_usuario_torneio(self, usuario: Usuario, torneio: Torneio):
        p: TorneioUsuario | None = self.torneio_repository.procurar_participacao(usuario, torneio)
        
        if p is None:
            raise ValueError("O usuário não está participando do torneio")
        
        self.torneio_repository.remover_participacao_usuario(p)

    def listar_participantes_torneio(self, torneio: Torneio) -> list[Usuario]:
        l_usuario = self.torneio_repository.listar_participantes(torneio.id)

        if not l_usuario:
            return []

        return l_usuario

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

    def listar_torneios(self) -> list[Torneio]:
        return self.torneio_repository.listar()
    
    def finalizar_partida(self, partida_id: int, vencedor_id: int) -> Partida:

        partida = self.torneio_repository.buscar_partida_por_id(partida_id)

        vencedor = self.usuario_repository.busar_usuario_por_id(vencedor_id)
        
        if vencedor is not partida.jogador1 or partida.jogador2:
            raise ValueError("Este usuário não faz parte desta partida")
        
        if partida.vencedor:
            raise ValueError("Esta partida já possui um vencedor")

        partida.vencedor = vencedor
        self.torneio_repository.commit()
        return partida


    def verificar_fim_da_rodada(self, rodada: Rodada) -> bool:
        return all(partida.vencedor is not None for partida in rodada.partidas)
    
    def adicionar_fase_mata_mata(self, torneio: Torneio, melhor_de: int) -> Torneio:

        if melhor_de <= 0 or melhor_de % 2 == 0:
            raise ValueError("Variavel 'melhor_de' deve ser um número ímpar maior que zero.")
        

        fase = FaseMataMata(
            melhor_de=melhor_de
        )
        
        torneio.fases_torneio.append(fase)

        
        torneio = self.torneio_repository.salvar(torneio)

        return torneio

    def listar_partidas(self, rodada: Rodada) -> list[Partida]:
        partidas = self.torneio_repository.listar_partidas(rodada)

        if not partidas:
            raise ValueError("Não há partidas nessa rodada.")
        
        return partidas
        

    # Lógica de Torneio

    def iniciar_chaveamento(self, torneio: Torneio):
                
        if len(torneio.fases_torneio) == 0:
            raise ValueError("As fases do torneio ainda não foram preenchidas")

        for fase in torneio.fases_torneio:
            
            match fase.tipo:
                
                case TipoFase.MATA_MATA:
                    
                    l_torenio_usuario = list(torneio.usuarios_participantes)

                    participantes = [tu.usuario for tu in l_torenio_usuario]
                    
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

                    fase.rodadas.append(rodada)

                case TipoFase.SWISS:
                    # lógica de chaveamento para swiss
                    pass
        
        # Salvar após chaveamento inicial
        self.torneio_repository.salvar(torneio)
        return torneio

    def verificar_fim_de_rodada(self, rodada: Rodada) -> bool:
        for partida in rodada.partidas:
            if not partida.vencedor:
                return False
        return True

    def listar_rodadas(self, fase: Fase) -> list[Rodada]:
        rodadas = self.torneio_repository.listar_rodadas(fase)
        if not rodadas:
            raise ValueError("Ainda não há rodadas nesta fase.")
        return rodadas
    
    # Lógica de mata_mata

    def criar_proxima_rodada_mata_mata(self, rodada_atual: Rodada):
        
        if not self.verificar_fim_da_rodada(rodada_atual):
            raise ValueError("As partidas da rodada atual ainda não foram concluídas.")

        vencedores = [
            partida.vencedor
            for partida in rodada_atual.partidas
        ]

        # Varificar se há apenas um vencedor e o torneio terminou
        if len(vencedores) == 1:
            # Corrigir futuramente
            # rodada_atual.fase.torneio. = vencedores[0]
            # torneio.estado = EstadoTorneio.FINALIZADO
            return ("O torneio terminou e o campeão é: " + vencedores[0].nome)

        nova_rodada = Rodada()

        for i in range(0, len(vencedores), 2):
            partida = Partida(
                jogador1 = vencedores[i],
                jogador2 = vencedores[i + 1]
            )
            nova_rodada.partidas.append(partida)

        return nova_rodada
    
