from typing import Optional
from pydantic import BaseModel, Field


class TarefaBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, example="Estudar SQLAlchemy")
    descricao: Optional[str] = Field(None, example="Aprender sobre ORM e integração com banco de dados")
    concluida: bool = Field(default=False)


class TarefaCreate(TarefaBase):
    pass


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=100, example="Estudar SQLAlchemy Avançado")
    descricao: Optional[str] = Field(None, example="Nova descrição atualizada")
    concluida: Optional[bool] = Field(None)


class TarefaResponse(TarefaBase):
    id: int

    class Config:
        from_attributes = True