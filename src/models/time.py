from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from models.base import Base

class Time(Base):
    __tablename__ = "times"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str]

    membros: Mapped[list["UsuarioTime"]] = relationship(
        back_populates="time",
        cascade="all, delete-orphan"
    )

    torneios_participando: Mapped[list["TorneioTime"]] = relationship(
        back_populates="time",
        cascade="all, delete-orphan"
    )

    @property
    def integrantes(self):
        return [membro.usuario for membro in self.membros]