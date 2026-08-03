from pydantic import BaseModel
from backend.src.enums.enums_torneio import TipoTorneio

class MensagemResponse(BaseModel):
    msg: str
    
class CriarTorneioRequest(BaseModel):
    nome: str
    tipo_torneio: TipoTorneio

class TorneioResponse(BaseModel):
    id: int
    nome: str
    tipo_torneio: TipoTorneio

class InscreverUsuarioRequest(BaseModel):
    usuario_id: int
    torneio_id: int

class InscreverUsuarioResponse(BaseModel):
    id: int
    usuario_id: int
    torneio_id: int

class FinalizarPartidaRequest(BaseModel):
    partida_id: int
    vencedor_id: int

