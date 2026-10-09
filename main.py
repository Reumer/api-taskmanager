from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

import models
from database import engine, get_db

# Cria automaticamente as tabelas no banco de dados SQLite ao iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskManager API",
    description="API para gestão de tarefas e projetos com persistência em banco de dados",
    version="0.2.0"
)


# --- MODELOS DE DADOS (PYDANTIC / DTOs) ---
class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, example="Estudar SQLAlchemy")
    descricao: Optional[str] = Field(None, example="Aprender sobre ORM e integração com banco de dados")
    concluida: bool = Field(default=False)


class TarefaUpdate(BaseModel):
    titulo: Optional[str] = Field(None, min_length=3, max_length=100, example="Estudar SQLAlchemy Avançado")
    descricao: Optional[str] = Field(None, example="Nova descrição atualizada")
    concluida: Optional[bool] = Field(None)


class TarefaResponse(TarefaCreate):
    id: int

    class Config:
        from_attributes = True


# --- ROTAS DA API ---

@app.get("/", tags=["Geral"])
def home():
    return {"mensagem": "API TaskManager com Banco de Dados está online!"}


# 1. LISTAR TODAS AS TAREFAS (GET)
@app.get("/tarefas", response_model=List[TarefaResponse], tags=["Tarefas"])
def listar_tarefas(db: Session = Depends(get_db)):
    tarefas = db.query(models.TarefaDB).all()
    return tarefas


# 2. CRIAR UMA NOVA TAREFA (POST)
@app.post("/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    nova_tarefa = models.TarefaDB(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    return nova_tarefa


# 3. BUSCAR TAREFA POR ID (GET)
@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse, tags=["Tarefas"])
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )
    return tarefa


# 4. ATUALIZAR TAREFA (PUT)
@app.put("/tarefas/{tarefa_id}", response_model=TarefaResponse, tags=["Tarefas"])
def atualizar_tarefa(tarefa_id: int, dados_atualizados: TarefaUpdate, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )

    if dados_atualizados.titulo is not None:
        tarefa.titulo = dados_atualizados.titulo
    if dados_atualizados.descricao is not None:
        tarefa.descricao = dados_atualizados.descricao
    if dados_atualizados.concluida is not None:
        tarefa.concluida = dados_atualizados.concluida

    db.commit()
    db.refresh(tarefa)
    return tarefa


# 5. ELIMINAR TAREFA (DELETE)
@app.delete("/tarefas/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Tarefas"])
def eliminar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    tarefa = db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()
    if not tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )

    db.delete(tarefa)
    db.commit()
    return