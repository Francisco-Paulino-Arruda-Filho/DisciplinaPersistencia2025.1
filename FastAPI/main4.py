from http import HTTPStatus
from typing import Union, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import csv

app = FastAPI()
CSV_FILE = 'produtos.csv'

class Produto(BaseModel):
    id: int
    nome: str   
    preco: float
    qtd: int

def ler_dados_csv():
    global produtos
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            produtos = [Produto(**row) for row in reader]
    except FileNotFoundError:
        produtos = []
        return HTTPStatus.NOT_FOUND, "Arquivo CSV não encontrado."
    
def escrever_dados_csv(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['id', 'nome', 'preco', 'qtd']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for produto in produtos:
            writer.writerow(produto.model_dump())
            # writer.writerow(produto.dict())

@app.get("/produtos/{produto_id}", response_model=Produto)
def ler_produto(produto_id: int):
    ler_dados_csv()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")

@app.get("/produtos", response_model=List[Produto])
def listar_produtos():
    produtos = ler_dados_csv()
    return produtos

@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    ler_dados_csv()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")

@app.post("/produtos/", response_model=Produto)
def criar_produto(produto: Produto):
    produtos = listar_produtos()    
    if any(p.id == produto.id for p in produtos):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Produto já existe.")
    produtos.append(produto)
    escrever_dados_csv(CSV_FILE)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto_atualizado: Produto):
    produtos = listar_produtos()
    for i, p in enumerate(produtos):
        if p.id == produto_id:
            produtos[i] = produto_atualizado
            escrever_dados_csv(produtos)
            return produto_atualizado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")

'''
@app.delete("/produtos/{produto_id}", response_model=Produto)
def deletar_produto(produto_id: int):
    produtos = listar_produtos()
    for i, p in enumerate(produtos):
        if p.id == produto_id:
            produto_deletado = produtos.pop(i)
            escrever_dados_csv(produtos)
            return produto_deletado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")
'''
@app.delete("/produtos/{produto_id}", response_model=Produto)
def deletar_produto(produto_id: int):
    produtos = listar_produtos()   
    produtos_filtrados = [p for p in produtos if p.id != produto_id]
    if len(produtos) == len(produtos_filtrados):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")
    escrever_dados_csv(produtos_filtrados)
    return {"message": "Produto deletado com sucesso."}