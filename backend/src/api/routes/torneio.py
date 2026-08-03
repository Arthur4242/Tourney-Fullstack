from fastapi import APIRouter
from fastapi import Depends


from schemas.torneio import CriarTorneioRequest, TorneioResponse, InscreverUsuarioRequest, InscreverUsuarioResponse, FinalizarPartidaRequest, MensagemResponse

from backend.src.services.torneio_service import TorneioService

from dependencies import get_torneio_service

router = APIRouter(
    prefix="torneios",
    tags=["Torneios"]
)


@router.post("/", response_model=TorneioResponse)
def criar_torneio(
    torneio_request: CriarTorneioRequest,
    torneio_service: TorneioService = Depends(get_torneio_service)
):
    torneio = torneio_service.cadastrar_torneio(
        torneio_request.nome,
        torneio_request.tipo_torneio)

    return TorneioResponse(
        id=torneio.id,
        nome=torneio.nome,
        tipo_torneio=torneio.tipo
    )

@router.post("/inscrever", response_model=InscreverUsuarioResponse)
def inscrever_usuario(
    inscricao_request: InscreverUsuarioRequest,
    torneio_service: TorneioService = Depends(get_torneio_service)
):
    torneio_usuario = torneio_service.adicionar_usuario_torneio(
        inscricao_request.usuario_id,
        inscricao_request.torneio_id
    )

    return InscreverUsuarioResponse(
        id=torneio_usuario.id,
        usuario_id=torneio_usuario.usuario_id,
        torneio_id=torneio_usuario.torneio_id
    )

@router.post("/finalizar_partida", response_model=MensagemResponse)
def finalizar_partida(
    request: FinalizarPartidaRequest,
    torneio_service: TorneioService = Depends(get_torneio_service)
):
    partida = torneio_service.finalizar_partida(request.partida_id, request.vencedor_id)

    return MensagemResponse(
        msg= "Partida finalizada com sucesso."
    )

@router.get("/{id}")
def get_torneio(
    torneio_service: TorneioService = Depends(get_torneio_service)
):
    torneio = torneio_service.buscar_torneio_por_id(id)
    return