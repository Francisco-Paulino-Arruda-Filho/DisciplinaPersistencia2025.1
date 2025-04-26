from http import HTTPStatus
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from logger import logger

app = FastAPI()
XML_FILE = 'Livros.json'
PASTA_DADOS = Path("dados")
PASTA_DADOS.mkdir(exist_ok=True)

ARQUIVO_AUTORES = PASTA_DADOS / "autores.json"
ARQUIVO_LIVROS = PASTA_DADOS / "livros.json"

for arquivo in [ARQUIVO_AUTORES, ARQUIVO_LIVROS]:
    if not arquivo.exists():
        arquivo.write_text("[]")


class Autor(BaseModel):
    id: int
    nome: str

class Livro(BaseModel):
    id: int
    titulo: str
    autor_id: int

def ler_json(arquivo: Path):
    return json.loads(arquivo.read_text())
    
def escrever_json(arquivo: Path, dados):
    arquivo.write_text(json.dumps(dados, indent=4))

@app.post("/autores", response_model=Autor, status_code=HTTPStatus.CREATED)
def criar_autor(autor: Autor):
    autores = ler_json(ARQUIVO_AUTORES)
    if any(a['id'] == autor.id for a in autores):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Autor já existe")
    
    autores.append(autor.model_dump())
    escrever_json(ARQUIVO_AUTORES, autores)
    logger.info(f"Autor {autor.nome} criado com sucesso.")
    return autor

@app.get("/autores", response_model=List[Autor])
def listar_autores():
    autores = ler_json(ARQUIVO_AUTORES)
    logger.info("Listando autores.")
    return autores

@app.get("/autores/{autor_id}", response_model=Autor)
def obter_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    for autor in autores:
        if autor['id'] == autor_id:
            logger.info(f"Autor {autor['nome']} encontrado.")
            return autor
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Autor não encontrado")

'''
@app.get("/autores", response_model=List[Autor])
def listar_autores():
    return ler_json(ARQUIVO_AUTORES)
'''

@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(autor_id: int, autor: Autor):
    autores = ler_json(ARQUIVO_AUTORES)
    for i, a in enumerate(autores):
        if a['id'] == autor_id:
            autores[i] = autor.model_dump()
            escrever_json(ARQUIVO_AUTORES, autores)
            logger.info(f"Autor {autor.nome} atualizado com sucesso.")
            return autor
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Autor não encontrado")

@app.delete("/autores/{autor_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    for i, a in enumerate(autores):
        if a['id'] == autor_id:
            del autores[i]
            escrever_json(ARQUIVO_AUTORES, autores)
            logger.info(f"Autor {a['nome']} deletado com sucesso.")
            return
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Autor não encontrado")

'''
@app.delete("/autores/{autor_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    autores = [a for a in autores if a['id'] != autor_id]
    escrever_json(ARQUIVO_AUTORES, autores)
    logger.info(f"Autor {autor_id} deletado com sucesso.")
'''

'''
@app.put("/autores/{autor_id}", response_model=Autor)
def atualizar_autor(autor_id: int, autor: Autor):
    autores = ler_json(ARQUIVO_AUTORES)
    for idx, a in enumerate(autores):
        if a['id'] == autor_id:
            autores[idx] = autor.model_dump()
            escrever_json(ARQUIVO_AUTORES, autores)
            logger.info(f"Autor {autor.nome} atualizado com sucesso.")
            return autor
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Autor não encontrado")
'''
@app.post("/livros", response_model=Livro, status_code=HTTPStatus.CREATED)
def criar_livro(livro: Livro):
    autores = ler_json(ARQUIVO_AUTORES)
    if not any(a['id'] == livro.autor_id for a in autores):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Autor não encontrado")
    livros = ler_json(ARQUIVO_LIVROS)
    if any(l['id'] == livro.id for l in livros):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Livro já existe")
    livros.append(livro.model_dump())
    escrever_json(ARQUIVO_LIVROS, livros)
    logger.info(f"Livro {livro.titulo} criado com sucesso.")
    return livro

@app.get("/livros", response_model=List[Livro])
def listar_livros():
    livros = ler_json(ARQUIVO_LIVROS)
    logger.info("Listando livros.")
    return livros

@app.get("/livros/{livro_id}", response_model=Livro)
def obter_livro(livro_id: int):
    livros = ler_json(ARQUIVO_LIVROS)
    for livro in livros:
        if livro['id'] == livro_id:
            logger.info(f"Livro {livro['titulo']} encontrado.")
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado")

@app.put("/livros/{livro_id}", response_model=Livro)
def atualizar_livro(livro_id: int, livro: Livro):
    livros = ler_json(ARQUIVO_LIVROS)
    for i, l in enumerate(livros):
        if l['id'] == livro_id:
            livros[i] = livro.model_dump()
            escrever_json(ARQUIVO_LIVROS, livros)
            logger.info(f"Livro {livro.titulo} atualizado com sucesso.")
            return livro
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado")

@app.delete("/livros/{livro_id}", status_code=HTTPStatus.NO_CONTENT)
def deletar_livro(livro_id: int):
    livros = ler_json(ARQUIVO_LIVROS)
    for i, l in enumerate(livros):
        if l['id'] == livro_id:
            del livros[i]
            escrever_json(ARQUIVO_LIVROS, livros)
            logger.info(f"Livro {l['titulo']} deletado com sucesso.")
            return
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Livro não encontrado")

@app.get("/livros/autor/{autor_id}", response_model=List[Livro])
def listar_livros_por_autor(autor_id: int):
    livros = ler_json(ARQUIVO_LIVROS)
    livros_autor = [livro for livro in livros if livro['autor_id'] == autor_id]
    if not livros_autor:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Nenhum livro encontrado para este autor")
    logger.info(f"Listando livros do autor {autor_id}.")
    return livros_autor

'''
@app.get("/livros/autor/{autor_id}", response_model=List[Livro])
def listar_livros_por_autor(autor_id: int):
    autores = ler_json(ARQUIVO_AUTORES)
    if not any(a['id'] == autor_id for a in autores):
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Autor não encontrado")
    livros = ler_json(ARQUIVO_LIVROS)
    livros_autor = [livro for livro in livros if livro['autor_id'] == autor_id]
    logger.info(f"Listando livros do autor {autor_id}.")
    return livros_autor
'''