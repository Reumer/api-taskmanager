from fastapi import FastAPI
import models
from database import engine
from routers import tarefas

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TaskManager API",
    description="API modularizada para gestão de tarefas",
    version="0.3.0"
)

# Inclui as rotas do módulo de tarefas
app.include_router(tarefas.router)


@app.get("/", tags=["Geral"])
def home():
    return {"mensagem": "API TaskManager refatorada e pronta!"}