from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class LivroCreate(BaseModel):
    titulo: str = Field(..., min_length=2)
    autor: str = Field(..., min_length=2)
    ano: int = Field(..., ge=1000, le=date.today().year)
    disponivel: bool = True


class LivroUpdate(BaseModel):
    titulo: str | None = Field(default=None, min_length=2)
    autor: str | None = Field(default=None, min_length=2)
    ano: int | None = Field(default=None, ge=1000, le=date.today().year)
    disponivel: bool | None = None


class LivroResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    titulo: str
    autor: str
    ano: int
    disponivel: bool
