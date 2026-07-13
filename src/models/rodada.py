from models.base import Base
from enums.enums_fase import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey

# from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.fase import Fase
    from models.partida import Partida

class Rodada(Base):
    __tablename__ = "rodadas"

    id: Mapped[int] = mapped_column(primary_key=True)

    fase_id: Mapped[int] = mapped_column(
        ForeignKey("fases.id")
    )

    fase: Mapped["Fase"] = relationship(
        back_populates="rodadas"
    )

    partidas: Mapped[list["Partida"]] = relationship(
        back_populates='rodada',
        cascade="all, delete-orphan"
    )