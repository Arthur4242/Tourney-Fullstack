# from __future__ import annotations
from typing import TYPE_CHECKING

from backend.src.models.base import Base
from backend.src.enums.enums_fase import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey


if TYPE_CHECKING:
    from backend.src.models.torneio import Torneio
    from backend.src.models.rodada import Rodada
    
class Fase(Base):
    __tablename__ = "fases"

    id: Mapped[int] = mapped_column(primary_key=True)

    tipo: Mapped[TipoFase] = mapped_column(
        SQLEnum(TipoFase)
    )

    torneio_id: Mapped[int] = mapped_column(
        ForeignKey("torneios.id")
    )

    torneio: Mapped["Torneio"] = relationship(
        back_populates="fases_torneio"
    )

    rodadas: Mapped[list["Rodada"]] = relationship(
        back_populates='fase',
        cascade="all, delete-orphan"
    )

    __mapper_args__ = {
        "polymorphic_on": tipo,
    }

