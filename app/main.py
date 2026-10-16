from fastapi import FastAPI

from app.routers import emprestimos, livros

app = FastAPI(
    title="Biblioteca Escolar",
    description="API REST para o controle de acervo e empréstimos de uma biblioteca escolar.",
    version="1.0.0",
)

app.include_router(livros.router)
app.include_router(emprestimos.router)
