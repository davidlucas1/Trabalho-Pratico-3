from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.emprestimo import Emprestimo
from app.models.livro import Livro
from app.schemas.emprestimo import EmprestimoResponse
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)) -> Livro:
    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("", response_model=list[LivroResponse])
def listar_livros(
    disponivel: bool | None = Query(default=None, description="Filtra por disponibilidade."),
    db: Session = Depends(get_db),
) -> list[Livro]:
    consulta = select(Livro)
    if disponivel is not None:
        consulta = consulta.where(Livro.disponivel == disponivel)
    return list(db.scalars(consulta).all())


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)) -> Livro:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return livro


@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(
    livro_id: int,
    dados: LivroUpdate,
    db: Session = Depends(get_db),
) -> Livro:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(livro, campo, valor)

    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
def remover_livro(livro_id: int, db: Session = Depends(get_db)) -> Response:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")

    possui_emprestimo = db.scalar(
        select(Emprestimo.id).where(Emprestimo.livro_id == livro_id).limit(1)
    )
    if possui_emprestimo is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Não é possível excluir o livro porque existem empréstimos vinculados.",
        )

    db.delete(livro)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{livro_id}/emprestimos", response_model=list[EmprestimoResponse])
def listar_emprestimos_do_livro(livro_id: int, db: Session = Depends(get_db)) -> list[Emprestimo]:
    livro = db.get(Livro, livro_id)
    if livro is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Livro não encontrado.")
    return list(livro.emprestimos)
