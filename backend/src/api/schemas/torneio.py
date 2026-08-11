from pydantic import BaseModel
from backend.src.enums.enums_torneio import TipoTorneio, EstadoTorneio
from backend.src.enums.enums_fase import TipoFase

# Requests

class CriarTorneioRequest(BaseModel):
    nome: str
    tipo_torneio: TipoTorneio


class InscreverUsuarioRequest(BaseModel):
    usuario_id: int
    torneio_id: int


class FinalizarPartidaRequest(BaseModel):
    partida_id: int
    vencedor_id: int


class FinalizarTorneioRequest(BaseModel):
    torneio_id: int
    vencedor_id: int

class CadastrarFaseTorneio(BaseModel):
    torneio_id: int
    tipo_fase: TipoFase

class TorneioIdRequest(BaseModel):
    torneio_id: int

# Responses

class MensagemResponse(BaseModel):
    msg: str

class TorneioResponse(BaseModel):
    id: int
    nome: str
    tipo_torneio: TipoTorneio
    estado_torneio: EstadoTorneio

class InscreverUsuarioResponse(BaseModel):
    id: int
    usuario_id: int
    torneio_id: int