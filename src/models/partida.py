from models.base import Base
from enums.enums_torneio import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import ForeignKey

class Partida(Base):
    __tablename__ = "partidas"

    id: Mapped[int] = mapped_column(primary_key=True)

    fase_id: Mapped[int] = mapped_column(
        ForeignKey("fases.id")
    )
    
    fase: Mapped['Fase'] = relationship(
        back_populates='partidas'
    )

    