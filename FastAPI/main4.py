from http import HTTPStatus
from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv

app = FastAPI()
produtos = []

class Produto(BaseModel):
    id: int
    nome: str   
    preco: float
    qtd: int

def ler_dados_csv(CSV_FILE):
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            produto = Produto(nome=row['nome'], preco=float(row['preco']), qtd=int(row['qtd']))
            produtos.append(Produto(**row))
        return produtos
    
def escrever_dados_csv(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'nome', 'preco', 'qtd']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.dict())

@app.get("/produtos/{produto_id}", response_model=Produto)
def ler_produto(produto_id: int):
    ler_dados_csv