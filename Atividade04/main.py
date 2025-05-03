from http import HTTPStatus
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
from pathlib import Path
from logger import logger

app = FastAPI()
XML_FILE = 'data.json'

class Pessoa(BaseModel):
    id: int
    name: str
    age: int

def ler_json(arquivo: Path):
    return json.loads(arquivo.read_text())
    
def escrever_json(arquivo: Path, dados):
    arquivo.write_text(json.dumps(dados, indent=4))

@app.post("/pessoas", response_model=Pessoa, status_code=HTTPStatus.CREATED)
def criar_pessoa(pessoa: Pessoa):
    pessoas = ler_json(Path(XML_FILE))
    if any(p['id'] == pessoa.id for p in pessoas):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Pessoa já existe")
    
    pessoas.append(pessoa.model_dump())
    escrever_json(Path(XML_FILE), pessoas)
    logger.info(f"Pessoa {pessoa.name} criada com sucesso.")
    return pessoa

@app.get("/pessoas", response_model=List[Pessoa])
def listar_pessoas():
    pessoas = ler_json(Path(XML_FILE))
    logger.info("Listando pessoas.")
    return pessoas

@app.get("/pessoas/{pessoa_id}", response_model=Pessoa)
def obter_pessoa(pessoa_id: int):
    pessoas = ler_json(Path(XML_FILE))
    for pessoa in pessoas:
        if pessoa['id'] == pessoa_id:
            logger.info(f"Pessoa {pessoa['name']} encontrada.")
            return pessoa
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Pessoa não encontrada")
