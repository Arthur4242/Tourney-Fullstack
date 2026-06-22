from models.base import Base
from enums.tipo_torneio import *
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLEnum

class Torneio(Base):
    __tablename__ = "torneios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    tipo: Mapped[TipoTorneio] = mapped_column(
        SQLEnum(TipoTorneio)
    )

    times_participantes: Mapped[list["TorneioTime"]] = relationship(
        back_populates='torneio',
        cascade="all, delete-orphan"
    )

    usuarios_participantes: Mapped[list["TorneioUsuario"]] = relationship(
        back_populates='torneio',
        cascade="all, delete-orphan"
    )
    
    
