from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from database import alunos_collection, cursos_collection
from models import AlunoCreate, AlunoOut
from typing import List, Optional
from bson.errors import InvalidId

router = APIRouter()
@router.post("/alunos", response_model=AlunoOut)

@router.post("/", response_model=AlunoOut)
async def criar_aluno(aluno: AlunoCreate):
    aluno_dict = aluno.model_dump(exclude_unset=True)
    resultado = await alunos_collection.insert_one(aluno_dict)
    aluno_id = str(resultado.inserted_id)
    curso_id = aluno.curso_id
    update_result = await cursos_collection.update_one(
        {"_id": curso_id},
        {"$push": {"alunos": aluno_id}}
    )

    if update_result.modified_count == 0:
        await alunos_collection.delete_one({"_id": resultado.inserted_id})
        raise HTTPException(status_code=404, detail="Curso informado não existe")
    
    created = await alunos_collection.find_one({"_id": resultado.inserted_id})
    if created:
        created["_id"] = str(created["_id"])
        return created
    else:
        raise HTTPException(status_code=404, detail="Aluno não encontrado após criação")
    
@router.get("/", response_model=List[AlunoOut])
async def listar_alunos(skip: int = 0, limit: int = 10):
    alunos = await alunos_collection.find().skip(skip).limit(limit).to_list(length=limit)
    for aluno in alunos:
        aluno["_id"] = str(aluno["_id"])
    return alunos

@router.get("/{aluno_id}", response_model=AlunoOut)
async def obter_aluno(aluno_id: str):
    try:
        aluno_id = str(aluno_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    aluno = await alunos_collection.find_one({"_id": aluno_id})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    aluno["_id"] = str(aluno["_id"])
    return aluno

@router.delete("/{aluno_id}", response_model=dict)
async def deletar_aluno(aluno_id: str):
    aluno_id = str(aluno_id)
    aluno = await alunos_collection.find_one({"_id": aluno_id})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    curso_id = aluno.get("curso_id")
    resultado = await alunos_collection.delete_one({"_id": aluno_id})

    if curso_id:
        try:
            oid = ObjectId(curso_id)
            await cursos_collection.update_one(
                {"_id": oid},
                {"$pull": {"alunos": aluno_id}}
            )
        except InvalidId:
            pass
        return {"detail": "Aluno deletado com sucesso"}
    
@router.put("/{aluno_id}", response_model=AlunoOut)
async def atualizar_aluno(aluno_id: str, dados: AlunoOut):
    try:
        oid = ObjectId(aluno_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    aluno = await alunos_collection.find_one({"_id": oid})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    curso_antigo = aluno.get("curso_id")
    curso_novo = dados.curso_id

    update_result = await alunos_collection.update_one(
        {"_id": oid},
        {"$set": dados.model_dump(exclude_unset=True)}  # Se estiver no Pydantic v1 use .dict(...)
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Nenhum campo atualizado")

    # Atualizar cursos, se mudou
    if curso_antigo != curso_novo:
        try:
            oid_antigo = ObjectId(curso_antigo)
            oid_novo = ObjectId(curso_novo)

            await cursos_collection.update_one(
                {"_id": oid_antigo},
                {"$pull": {"alunos": aluno_id}}
            )
            await cursos_collection.update_one(
                {"_id": oid_novo},
                {"$push": {"alunos": aluno_id}}
            )
        except InvalidId:
            raise HTTPException(status_code=400, detail="ID de curso inválido")

    updated_aluno = await alunos_collection.find_one({"_id": oid})
    updated_aluno["_id"] = str(updated_aluno["_id"])
    return updated_aluno

@router.patch("/{aluno_id}", response_model=AlunoOut)
async def atualizar_aluno_parcial(aluno_id: str, dados: AlunoOut):
    try:
        oid = ObjectId(aluno_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

    aluno = await alunos_collection.find_one({"_id": oid})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    update_result = await alunos_collection.update_one(
        {"_id": oid},
        {"$set": dados.model_dump(exclude_unset=True)}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Nenhum campo atualizado")

    updated_aluno = await alunos_collection.find_one({"_id": oid})
    updated_aluno["_id"] = str(updated_aluno["_id"])
    return updated_aluno
