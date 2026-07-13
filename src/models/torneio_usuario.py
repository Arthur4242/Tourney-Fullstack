from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.torneio import Torneio
    from models.usuario import Usuario

class TorneioUsuario(Base):

    __tablename__ = "torneio_usuario"

    id: Mapped[int] = mapped_column(primary_key=True)

    torneio_id: Mapped[int] = mapped_column(
        ForeignKey("torneios.id")
    )

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    torneio: Mapped["Torneio"] = relationship(
        back_populates="usuarios_participantes"
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="torneios_participando"
    )