from fastapi import APIRouter, HTTPException
from database import professores_collection
from models import ProfessorCreate, ProfessorOut
from bson import ObjectId
from typing import List

router = APIRouter()

@router.post("/", response_model=ProfessorOut)
async def criar_professor(professor: ProfessorCreate):
    professor_dict = professor.dict(exclude_unset=True)
    result = await professores_collection.insert_one(professor_dict)
    created = await professores_collection.find_one({"_id": result.inserted_id})
    created["_id"] = str(created["_id"])  # Convert ObjectId to string
    return created

@router.get("/", response_model=List[ProfessorOut])
async def listar_professores(skip: int = 0, limit: int = 10):
    professores = await professores_collection.find().skip(skip).limit(limit).to_list(length=limit)
    for p in professores:
        p["_id"] = str(p["_id"])
    return professores

@router.get("/{professor_id}", response_model=ProfessorOut)
async def obter_professor(professor_id: str):
    try:
        professor_id = ObjectId(professor_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")
    
    professor = await professores_collection.find_one({"_id": professor_id})
    if not professor:
        raise HTTPException(status_code=404, detail="Professor não encontrado")
    
    professor["_id"] = str(professor["_id"])

    return professor

@router.put("/{professor_id}", response_model=ProfessorOut)
async def atualizar_professor(professor_id: str, professor: ProfessorCreate):
    try:
        professor_id = ObjectId(professor_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    update_result = await professores_collection.update_one(
        {"_id": professor_id},
        {"$set": professor.dict(exclude_unset=True)}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado ou nenhum campo atualizado")

    updated_professor = await professores_collection.find_one({"_id": professor_id})
    updated_professor["_id"] = str(updated_professor["_id"])

    return updated_professor

@router.delete("/{professor_id}", response_model=dict)
async def deletar_professor(professor_id: str):
    try:
        professor_id = ObjectId(professor_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    delete_result = await professores_collection.delete_one({"_id": professor_id})

    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Professor não encontrado")

    return {"message": "Professor deletado com sucesso"}

