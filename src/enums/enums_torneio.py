from enum import Enum


class TipoTorneio(Enum):
    INDIVIDUAL = "INDIVIDUAL"
    EQUIPE = "EQUIPE"

class EstadoTorneio(Enum):
    CRIADO = "Criado"
    INSCRICOES_ABERTAS = "Inscrições Abertas"
    INSCRICOES_ENCERRADAS = "Inscrições Encerradas"
    EM_ANDAMENTO = "Em andamento"
    FINALIZADO = "Finalizado"
    CANCELADO = "Cancelado"