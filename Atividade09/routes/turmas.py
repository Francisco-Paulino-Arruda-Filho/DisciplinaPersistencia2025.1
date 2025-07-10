from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from models import TurmaCreate, TurmaOut
from database import turmas_collection

router = APIRouter(prefix="/turmas", tags=["Turmas"])

# Utilitário para validar ObjectId
def objectid_or_404(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    return ObjectId(id)

# Criar turma
@router.post("/", response_model=TurmaOut, status_code=status.HTTP_201_CREATED)
async def criar_turma(turma: TurmaCreate):
    nova = turma.dict()
    resultado = await turmas_collection.insert_one(nova)
    turma_salva = await turmas_collection.find_one({"_id": resultado.inserted_id})
    return TurmaOut(**turma_salva)

# Listar turmas
@router.get("/", response_model=list[TurmaOut])
async def listar_turmas():
    turmas = await turmas_collection.find().to_list(1000)
    return [TurmaOut(**t) for t in turmas]

# Buscar turma por ID
@router.get("/{id}", response_model=TurmaOut)
async def obter_turma(id: str):
    obj_id = objectid_or_404(id)
    turma = await turmas_collection.find_one({"_id": obj_id})
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return TurmaOut(**turma)

# Atualizar turma
@router.put("/{id}", response_model=TurmaOut)
async def atualizar_turma(id: str, turma: TurmaCreate):
    obj_id = objectid_or_404(id)
    resultado = await turmas_collection.update_one({"_id": obj_id}, {"$set": turma.dict()})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    turma_atualizada = await turmas_collection.find_one({"_id": obj_id})
    return TurmaOut(**turma_atualizada)

# Deletar turma
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_turma(id: str):
    obj_id = objectid_or_404(id)
    resultado = await turmas_collection.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return
