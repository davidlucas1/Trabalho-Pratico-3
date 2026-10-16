from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Emprestimo(Base):
    __tablename__ = "emprestimos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome_aluno: Mapped[str] = mapped_column(String, nullable=False)
    data_emprestimo: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        default=date.today,
        server_default=text("(CURRENT_DATE)"),
    )
    data_devolucao: Mapped[date | None] = mapped_column(Date, nullable=True)
    livro_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("livros.id"),
        nullable=False,
    )

    livro: Mapped["Livro"] = relationship("Livro", back_populates="emprestimos")
