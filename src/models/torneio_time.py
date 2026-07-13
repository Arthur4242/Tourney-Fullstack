from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.time import Time
    from models.torneio import Torneio

class TorneioTime(Base):

    __tablename__ = "torneio_time"

    id: Mapped[int] = mapped_column(primary_key=True)

    torneio_id: Mapped[int] = mapped_column(
        ForeignKey("torneios.id")
    )

    time_id: Mapped[int] = mapped_column(
        ForeignKey("times.id")
    )

    torneio: Mapped["Torneio"] = relationship(
        back_populates="times_participantes"
    )

    time: Mapped["Time"] = relationship(
        back_populates="torneios_participando"
    )