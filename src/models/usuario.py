from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.usuario_time import UsuarioTime
    from models.torneio_usuario import TorneioUsuario

class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    email: Mapped[str | None] = mapped_column(
        nullable=True
    )

    time_id: Mapped[int] = mapped_column

    participacoes: Mapped[list["UsuarioTime"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )

    torneios_participando: Mapped[list["TorneioUsuario"]] = relationship(
        back_populates="usuario",
        cascade="all, delete-orphan"
    )