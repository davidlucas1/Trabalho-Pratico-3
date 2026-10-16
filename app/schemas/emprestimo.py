from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class EmprestimoCreate(BaseModel):
    nome_aluno: str = Field(..., min_length=3)
    livro_id: int


class EmprestimoUpdate(BaseModel):
    nome_aluno: str | None = Field(default=None, min_length=3)
    data_emprestimo: date | None = None
    data_devolucao: date | None = None
    livro_id: int | None = None


class EmprestimoResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome_aluno: str
    data_emprestimo: date
    data_devolucao: date | None
    livro_id: int
