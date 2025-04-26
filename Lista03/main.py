from http import HTTPStatus
from typing import List
from fastapi import FastAPI, HTTPException
import os
import xml.etree.ElementTree as ET
from pydantic import BaseModel

app = FastAPI()
XML_FILE = 'Livros.xml'

class Livro(BaseModel):
    id: int
    titulo: str
    autor: str
    ano: int
    genero: str


def ler_dados_xml() -> List[Livro]:
    livros = []
    if os.path.exists(XML_FILE):
        tree = ET.parse(XML_FILE)
        root = tree.getroot()
        for elem in root.findall("livro"):
            livro = Livro(
                id=int(elem.find("id").text),
                titulo=elem.find("titulo").text,
                autor=elem.find("autor").text,
                ano=int(elem.find("ano").text),
                genero=elem.find("genero").text
            )
            livros.append(livro)
    return livros


def escrever_dados_xml(livros: List[Livro]):
    root = ET.Element("livros")
    for livro in livros:
        livro_elem = ET.SubElement(root, "livro")
        ET.SubElement(livro_elem, "id").text = str(livro.id)
        ET.SubElement(livro_elem, "titulo").text = livro.titulo
        ET.SubElement(livro_elem, "autor").text = livro.autor
        ET.SubElement(livro_elem, "ano").text = str(livro.ano)
        ET.SubElement(livro_elem, "genero").text = livro.genero
    tree = ET.ElementTree(root)
    tree.write(XML_FILE, encoding='utf-8', xml_declaration=True)


@app.post("/livros", response_model=Livro)
def criar_livro(livro: Livro):
    livros = ler_dados_xml()
    if any(l.id == livro.id for l in livros):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="ID já existente.")
    livros.append(livro)
    escrever_dados_xml(livros)
    return livro


@app.get("/livros", response_model=List[Livro])
def listar_livros():
    return ler_dados_xml()


@app.get("/livros/{livro_id}", response_model=Livro)
def buscar_livro(livro_id: int):
    livros = ler_dados_xml()
    for livro in livros:
        if livro.id == livro_id:
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro: Livro):
    livros = ler_dados_xml()
    for i, l in enumerate(livros):
        if l.id == livro_id:
            livros[i] = livro
            escrever_dados_xml(livros)
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")


@app.delete("/livros/{livro_id}", response_model=Livro)
def deletar_livro(livro_id: int):
    livros = ler_dados_xml()
    for i, l in enumerate(livros):
        if l.id == livro_id:
            livro_deletado = livros.pop(i)
            escrever_dados_xml(livros)
            return livro_deletado
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado.")
