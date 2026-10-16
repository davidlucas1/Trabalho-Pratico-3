from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.schemas.emprestimo import EmprestimoCreate, EmprestimoResponse

router = APIRouter(prefix="/emprestimos", tags=["Empréstimos"])


@router.post("", response_model=EmprestimoResponse, status_code=status.HTTP_201_CREATED)
def criar_emprestimo(dados: EmprestimoCreate, db: Session = Depends(get_db)) -> Emprestimo:
    livro = db.get(Livro, dados.livro_id)
    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    if not livro.disponivel:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Livro já está emprestado.",
        )

    emprestimo = Emprestimo(
        nome_aluno=dados.nome_aluno,
        livro_id=dados.livro_id,
        data_emprestimo=date.today(),
    )
    livro.disponivel = False
    db.add(emprestimo)
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.get("", response_model=list[EmprestimoResponse])
def listar_emprestimos(
    livro_id: int | None = Query(default=None, description="Filtra pelo identificador do livro."),
    ativos: bool | None = Query(
        default=None,
        description="Quando verdadeiro, lista apenas empréstimos sem data de devolução.",
    ),
    db: Session = Depends(get_db),
) -> list[Emprestimo]:
    consulta = select(Emprestimo)
    if livro_id is not None:
        consulta = consulta.where(Emprestimo.livro_id == livro_id)
    if ativos is True:
        consulta = consulta.where(Emprestimo.data_devolucao.is_(None))
    return list(db.scalars(consulta).all())


@router.get("/{emprestimo_id}", response_model=EmprestimoResponse)
def buscar_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)) -> Emprestimo:
    emprestimo = db.get(Emprestimo, emprestimo_id)
    if emprestimo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado.",
        )
    return emprestimo


@router.put("/{emprestimo_id}/devolucao", response_model=EmprestimoResponse)
def registrar_devolucao(emprestimo_id: int, db: Session = Depends(get_db)) -> Emprestimo:
    emprestimo = db.get(Emprestimo, emprestimo_id)
    if emprestimo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado.",
        )
    if emprestimo.data_devolucao is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Empréstimo já foi devolvido.",
        )

    emprestimo.data_devolucao = date.today()
    emprestimo.livro.disponivel = True
    db.commit()
    db.refresh(emprestimo)
    return emprestimo


@router.delete(
    "/{emprestimo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
)
def remover_emprestimo(emprestimo_id: int, db: Session = Depends(get_db)) -> Response:
    emprestimo = db.get(Emprestimo, emprestimo_id)
    if emprestimo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empréstimo não encontrado.",
        )
    if emprestimo.data_devolucao is None:
        emprestimo.livro.disponivel = True

    db.delete(emprestimo)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
