from models.fase import Fase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

class FaseMataMata(Fase):
    __tablename__ = "fases_mata_mata"

    __mapper_args__ = {
        "polymorphic_identity": "mata_mata"
    }

    id: Mapped[int] = mapped_column(
        ForeignKey("fases.id"),
        primary_key=True
    )

    melhor_de: Mapped[int]