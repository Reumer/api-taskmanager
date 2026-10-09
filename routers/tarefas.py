from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from database import get_db

router = APIRouter(
    prefix="/tarefas",
    tags=["Tarefas"]
)


@router.get("", response_model=List[schemas.TarefaResponse])
def listar_tarefas(db: Session = Depends(get_db)):
    return crud.get_tarefas(db)


@router.post("", response_model=schemas.TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar_tarefa(tarefa: schemas.TarefaCreate, db: Session = Depends(get_db)):
    return crud.create_tarefa(db, tarefa)


@router.get("/{tarefa_id}", response_model=schemas.TarefaResponse)
def obter_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = crud.get_tarefa_by_id(db, tarefa_id)
    if not db_tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )
    return db_tarefa


@router.put("/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar_tarefa(tarefa_id: int, dados: schemas.TarefaUpdate, db: Session = Depends(get_db)):
    db_tarefa = crud.update_tarefa(db, tarefa_id, dados)
    if not db_tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )
    return db_tarefa


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_tarefa(tarefa_id: int, db: Session = Depends(get_db)):
    db_tarefa = crud.delete_tarefa(db, tarefa_id)
    if not db_tarefa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tarefa com ID {tarefa_id} não encontrada."
        )
    return