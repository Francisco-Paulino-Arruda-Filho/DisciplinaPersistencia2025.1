from fastapi import APIRouter, HTTPException, status
from bson import ObjectId

from models import MatriculaCreate, MatriculaOut
from database import matriculas_collection, alunos_collection, turmas_collection

router = APIRouter(prefix="/matriculas", tags=["Matrículas"])

def objectid_or_404(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="ID inválido")
    return ObjectId(id)

# Criar uma matrícula
@router.post("/", response_model=MatriculaOut, status_code=status.HTTP_201_CREATED)
async def criar_matricula(matricula: MatriculaCreate):
    nova = matricula.dict()
    
    # Verifica se aluno e turma existem
    aluno = await alunos_collection.find_one({"_id": objectid_or_404(nova["aluno_id"])})
    turma = await turmas_collection.find_one({"_id": objectid_or_404(nova["turma_id"])})
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    resultado = await matriculas_collection.insert_one(nova)
    matricula_salva = await matriculas_collection.find_one({"_id": resultado.inserted_id})
    return MatriculaOut(**matricula_salva)

# Listar todas as matrículas
@router.get("/", response_model=list[MatriculaOut])
async def listar_matriculas():
    matriculas = await matriculas_collection.find().to_list(1000)
    return [MatriculaOut(**m) for m in matriculas]

# Buscar matrícula por ID
@router.get("/{id}", response_model=MatriculaOut)
async def obter_matricula(id: str):
    obj_id = objectid_or_404(id)
    matricula = await matriculas_collection.find_one({"_id": obj_id})
    if not matricula:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return MatriculaOut(**matricula)

# Atualizar matrícula
@router.put("/{id}", response_model=MatriculaOut)
async def atualizar_matricula(id: str, matricula: MatriculaCreate):
    obj_id = objectid_or_404(id)

    # Verifica se aluno e turma existem
    if not await alunos_collection.find_one({"_id": objectid_or_404(matricula.aluno_id)}):
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    if not await turmas_collection.find_one({"_id": objectid_or_404(matricula.turma_id)}):
        raise HTTPException(status_code=404, detail="Turma não encontrada")

    resultado = await matriculas_collection.update_one({"_id": obj_id}, {"$set": matricula.dict()})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    atualizada = await matriculas_collection.find_one({"_id": obj_id})
    return MatriculaOut(**atualizada)

# Deletar matrícula
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_matricula(id: str):
    obj_id = objectid_or_404(id)
    resultado = await matriculas_collection.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Matrícula não encontrada")
    return
