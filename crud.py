from sqlalchemy.orm import Session
import models
import schemas


def get_tarefas(db: Session):
    return db.query(models.TarefaDB).all()


def get_tarefa_by_id(db: Session, tarefa_id: int):
    return db.query(models.TarefaDB).filter(models.TarefaDB.id == tarefa_id).first()


def create_tarefa(db: Session, tarefa: schemas.TarefaCreate):
    db_tarefa = models.TarefaDB(
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        concluida=tarefa.concluida
    )
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


def update_tarefa(db: Session, tarefa_id: int, dados: schemas.TarefaUpdate):
    db_tarefa = get_tarefa_by_id(db, tarefa_id)
    if not db_tarefa:
        return None

    if dados.titulo is not None:
        db_tarefa.titulo = dados.titulo
    if dados.descricao is not None:
        db_tarefa.descricao = dados.descricao
    if dados.concluida is not None:
        db_tarefa.concluida = dados.concluida

    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa


def delete_tarefa(db: Session, tarefa_id: int):
    db_tarefa = get_tarefa_by_id(db, tarefa_id)
    if not db_tarefa:
        return None

    db.delete(db_tarefa)
    db.commit()
    return db_tarefa