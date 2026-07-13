# from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.time import Time
    from models.usuario import Usuario

class UsuarioTime(Base):
    __tablename__ = "usuario_time"

    id: Mapped[int] = mapped_column(primary_key=True)

    usuario_id: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id")
    )

    time_id: Mapped[int] = mapped_column(
        ForeignKey("times.id")
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="participacoes"
    )

    time: Mapped["Time"] = relationship(
        back_populates="membros"
    )