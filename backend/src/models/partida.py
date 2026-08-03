# from __future__ import annotations

from backend.src.models.base import Base
from backend.src.enums.enums_torneio import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from backend.src.models.usuario import Usuario
    from backend.src.models.rodada import Rodada

class Partida(Base):
    __tablename__ = "partidas"

    id: Mapped[int] = mapped_column(primary_key=True)

    rodada_id: Mapped[int] = mapped_column(
        ForeignKey("rodadas.id")
    )

    jogador1_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    jogador2_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    vencedor_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"),
        nullable=True
    )

    rodada: Mapped["Rodada"] = relationship(
        back_populates="partidas"
    )

    jogador1: Mapped["Usuario"] = relationship(
        foreign_keys=[jogador1_id]
    )

    jogador2: Mapped["Usuario | None"] = relationship(
        foreign_keys=[jogador2_id]
    )

    vencedor: Mapped["Usuario | None"] = relationship(
        foreign_keys=[vencedor_id]
    )
    