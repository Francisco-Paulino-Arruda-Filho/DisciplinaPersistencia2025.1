from fastapi import FastAPI
from database import create_db_and_tables
from routers import equipes

app = FastAPI(title="Gerenciamento de Equipes e Projetos")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Banco de dados criado e tabelas criadas com sucesso.")


@app.get("/")
def home():
    return {"message": "Bem-vindo à API de Gerenciamento de Equipes e Projetos!"}

app.include_router(equipes.router)