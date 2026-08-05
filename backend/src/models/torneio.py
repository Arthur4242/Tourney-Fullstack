# from __future__ import annotations

from backend.src.models.base import Base
from backend.src.enums.enums_torneio import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.src.models.fase import Fase
    from backend.src.models.torneio_time import TorneioTime
    from backend.src.models.torneio_usuario import TorneioUsuario
    from backend.src.models.usuario import Usuario



class Torneio(Base):
    __tablename__ = "torneios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    vencedor_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True
    )

    vencedor: Mapped["Usuario | None"] = relationship()     

    tipo: Mapped[TipoTorneio] = mapped_column(
        SQLEnum(TipoTorneio)
    )

    estado: Mapped[EstadoTorneio] = mapped_column(
        SQLEnum(EstadoTorneio)
    )

    times_participantes: Mapped[list["TorneioTime"]] = relationship(
        back_populates='torneio',
        cascade="all, delete-orphan"
    )

    usuarios_participantes: Mapped[list["TorneioUsuario"]] = relationship(
        back_populates='torneio',
        cascade="all, delete-orphan"
    )
    
    fases_torneio: Mapped[list["Fase"]] = relationship(
        back_populates='torneio',
        cascade="all, delete-orphan"
    )
