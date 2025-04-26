

import os
import xml.etree.ElementTree as ET
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from http import HTTPStatus

class Produto(BaseModel):
    id: int
    nome: str   
    preco: float
    qtd: int

XML_FILE = 'dados.xml'
app = FastAPI()

def ler_dados_xml():
    produtos = []
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for elem in root.findall("produto"):
            produto = Produto(
                id=int(elem.find("id").text),
                nome=elem.find("nome").text,
                preco=float(elem.find("preco").text),
                quantidade=int(elem.find("quantidade").text)
            )
            produtos.append(produto)
        return produtos

def escrever_dados_xml(produtos):
    root = ET.Element("produtos")
    for produto in produtos:
        produto_elem = ET.SubElement(root, "produto")
        ET.SubElement(produto_elem, "id").text = str(produto.id)
        ET.SubElement(produto_elem, "nome").text = produto.nome
        ET.SubElement(produto_elem, "preco").text = str(produto.preco)
        ET.SubElement(produto_elem, "quantidade").text = str(produto.quantidade)
        tree = ET.ElementTree(root)
        tree.write(XML_FILE)

@app.get("/produtos/{produto_id}", response_model=Produto)
def ler_produto(produto_id: int):
    produtos = ler_dados_xml()
    for produto in produtos:
        if produto.id == produto_id:
            return produto
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")

@app.get("/produtos", response_model=list[Produto])
def listar_produtos():
    produtos = ler_dados_xml()
    return produtos

@app.get("/produtos/{produto_id}", response_model=Produto)
def obter_produto(produto_id: int):
    produtos = ler_dados_xml()
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
    escrever_dados_xml(produtos)
    return produto

@app.put("/produtos/{produto_id}", response_model=Produto)
def atualizar_produto(produto_id: int, produto: Produto):
    produtos = listar_produtos()
    for i, p in enumerate(produtos):
        if p.id == produto_id:
            produtos[i] = produto
            escrever_dados_xml(produtos)
            return produto
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")

@app.delete("/produtos/{produto_id}", response_model=Produto)
def deletar_produto(produto_id: int):
    produtos = listar_produtos()
    for i, p in enumerate(produtos):
        if p.id == produto_id:
            produto_deletado = produtos.pop(i)
            escrever_dados_xml(produtos)
            return produto_deletado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Produto não encontrado.")