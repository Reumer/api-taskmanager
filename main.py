from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="TaskManager API",
    description="API para gestão de tarefas e projetos",
    version="0.1.0"
)

# --- BANCO DE DADOS EM MEMÓRIA (SIMULAÇÃO) ---
# Em produção usaremos um Banco de Dados real (PostgreSQL via SQLAlchemy)
db_tarefas = []
contador_id = 1


# --- MODELOS DE DADOS (PYDANTIC) ---
class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=100, example="Estudar FastAPI")
    descricao: Optional[str] = Field(None, example="Aprender sobre Pydantic e validação de dados")
    concluida: bool = Field(default=False)


class TarefaResponse(TarefaCreate):
    id: int


# --- ROTAS DA API ---

@app.get("/", tags=["Geral"])
def home():
    return {"mensagem": "API TaskManager está online e operacional!"}


# 1. LISTAR TODAS AS TAREFAS (GET)
@app.get("/tarefas", response_model=List[TarefaResponse], tags=["Tarefas"])
def listar_tarefas():
    return db_tarefas


# 2. CRIAR UMA NOVA TAREFA (POST)
@app.post("/tarefas", response_model=TarefaResponse, status_code=status.HTTP_201_CREATED, tags=["Tarefas"])
def criar_tarefa(tarefa: TarefaCreate):
    global contador_id

    nova_tarefa = {
        "id": contador_id,
        "titulo": tarefa.titulo,
        "descricao": tarefa.descricao,
        "concluida": tarefa.concluida
    }

    db_tarefas.append(nova_tarefa)
    contador_id += 1
    return nova_tarefa


# 3. BUSCAR TAREFA POR ID (GET)
@app.get("/tarefas/{tarefa_id}", response_model=TarefaResponse, tags=["Tarefas"])
def obter_tarefa(tarefa_id: int):
    for tarefa in db_tarefas:
        if tarefa["id"] == tarefa_id:
            return tarefa

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Tarefa com ID {tarefa_id} não encontrada."
    )