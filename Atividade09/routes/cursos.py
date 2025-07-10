from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from models import CursoCreate, CursoOut
from database import cursos_collection

router = APIRouter(prefix="/cursos", tags=["Cursos"])

# Função utilitária para validar ObjectId
def objectid_or_404(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    return ObjectId(id)

# Criar curso
@router.post("/", response_model=CursoOut, status_code=status.HTTP_201_CREATED)
async def criar_curso(curso: CursoCreate):
    novo = curso.dict()
    result = await cursos_collection.insert_one(novo)
    curso_salvo = await cursos_collection.find_one({"_id": result.inserted_id})
    return CursoOut(**curso_salvo)

# Listar cursos
@router.get("/", response_model=list[CursoOut])
async def listar_cursos():
    cursos = await cursos_collection.find().to_list(1000)
    return [CursoOut(**curso) for curso in cursos]

# Buscar por ID
@router.get("/{id}", response_model=CursoOut)
async def obter_curso(id: str):
    obj_id = objectid_or_404(id)
    curso = await cursos_collection.find_one({"_id": obj_id})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return CursoOut(**curso)

# Atualizar curso
@router.put("/{id}", response_model=CursoOut)
async def atualizar_curso(id: str, curso: CursoCreate):
    obj_id = objectid_or_404(id)
    resultado = await cursos_collection.update_one(
        {"_id": obj_id}, {"$set": curso.dict()}
    )
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    atualizado = await cursos_collection.find_one({"_id": obj_id})
    return CursoOut(**atualizado)

# Deletar curso
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_curso(id: str):
    obj_id = objectid_or_404(id)
    resultado = await cursos_collection.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return
