from models.base import Base
from enums.enums_fase import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey

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

    partidas: Mapped[list["Partida"]] = relationship(
        back_populates='fase',
        cascade="all, delete-orphan"
    )
