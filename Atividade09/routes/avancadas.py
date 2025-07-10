






from fastapi import APIRouter, HTTPException
from database import alunos_collection, cursos_collection, turmas_collection, departamentos_collection, professores_collection, matriculas_collection
from bson import ObjectId

router = APIRouter(prefix="/avancadas")

@router.get("/cursos/{curso_id}/alunos-com-turmas")
async def listar_alunos(curso_id: str):
    try:
        curso_obj_id = ObjectId(curso_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de curso inválido")
    curso = await cursos_collection.find_one({"_id": curso_obj_id})
    if not curso:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    curso = fix_objectid(curso)
    
    alunos_cursor = await alunos_collection.find({"curso_id": curso_id})
    alunos = await alunos_cursor.to_list(length=None)
    alunos = [fix_objectid(aluno) for aluno in alunos]
    
    turmas_cursor = await turmas_collection.find({"curso_id": curso_id})
    turmas = await turmas_cursor.to_list(length=None)
    turmas = [fix_objectid(turma) for turma in turmas]
    turmas_dict = {str(turma["_id"]): turma for turma in turmas}

    resultado = []
    for aluno in alunos:
        aluno_turmas_ids = aluno.get("turmas", [])
        aluno_turmas = [turmas_dict[str(turma_id)] for turma_id in aluno_turmas_ids if str(turma_id) in turmas_dict]
        aluno_info = {
            "nome": aluno,
            "curso": curso,
            "turmas": aluno_turmas
        }
        resultado.append(aluno_info)

        return fix_objectid(resultado)
    
@router.get("departamentos/{departamento_id}/professores-com-turmas")
async def listar_professores_cursos_alunos(departamento_id: str):
    try:
        departamento_obj_id = ObjectId(departamento_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de departamento inválido")
    
    departamento = await departamentos_collection.find_one({"_id": departamento_obj_id})
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento não encontrado")
    
    departamento = fix_objectid(departamento)
    
    cursos_cursor = await cursos_collection.find({"departamento_id": departamento_id})
    cursos = await cursos_cursor.to_list(length=None)
    cursos = [fix_objectid(curso) for curso in cursos]

    resultado = []
    
    for curso in cursos:
        professor = await professores_collection.find_one({"_id": ObjectId(curso["professor_id"])})
        if not professor:
            continue
        professor = fix_objectid(professor) if professor else None

        alunos_cursor = await alunos_collection.find({"curso_id": str(curso["_id"])})
        alunos = await alunos_cursor.to_list(length=None)
        alunos = [fix_objectid(aluno) for aluno in alunos]

        resultado.append({
            "Curso": curso,
            "Coordenador": professor,
            "Alunos": alunos
        })

    return {
        "Departamento": departamento,
        "Cursos_professores_alunos": resultado
    }

def fix_objectid(doc):
    if isinstance(doc, list):
        return [fix_objectid(i) for i in doc]
    if isinstance(doc, dict):
        out = {}
        for k, v in doc.items():
            if isinstance(v, ObjectId):
                out[k] = str(v)
            else:
                out[k] = fix_objectid(v)
        return out
    return doc

@router.get("/alunos/{aluno_id}/matriculas-detalhadas")
async def listar_matriculas_detalhadas(aluno_id: str):
    try:
        aluno_obj_id = ObjectId(aluno_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID de aluno inválido")

    aluno = await alunos_collection.find_one({"_id": aluno_obj_id})
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    aluno = fix_objectid(aluno)

    matriculas = await matriculas_collection.find({"aluno_id": aluno_id}).to_list(length=None)
    resultado = []

    for matricula in matriculas:
        turma = await turmas_collection.find_one({"_id": ObjectId(matricula["turma_id"])})
        turma = fix_objectid(turma) if turma else None

        curso = None
        if turma:
            curso = await cursos_collection.find_one({"_id": ObjectId(turma["curso_id"])})
            curso = fix_objectid(curso) if curso else None

        resultado.append({
            "matricula_id": str(matricula["_id"]),
            "turma": turma,
            "curso": curso
        })

    return {
        "aluno": aluno,
        "matriculas": resultado
    }

@router.get("/cursos-com-total-alunos")
async def cursos_com_total_alunos():
    cursos = await cursos_collection.find().to_list(length=None)
    cursos = fix_objectid(cursos)

    resultado = []
    for curso in cursos:
        total = await alunos_collection.count_documents({"curso_id": str(curso["_id"])})
        resultado.append({
            "curso": curso,
            "total_alunos": total
        })

    return resultado

@router.get("/professores-com-cursos-e-turmas")
async def professores_com_detalhes():
    professores = await professores_collection.find().to_list(length=None)
    professores = fix_objectid(professores)

    resultado = []

    for prof in professores:
        cursos = await cursos_collection.find({"professor_id": str(prof["_id"])}).to_list(length=None)
        cursos = fix_objectid(cursos)

        cursos_com_turmas = []
        for curso in cursos:
            turmas = await turmas_collection.find({"curso_id": str(curso["_id"])}).to_list(length=None)
            turmas = fix_objectid(turmas)
            cursos_com_turmas.append({
                "curso": curso,
                "turmas": turmas
            })

        resultado.append({
            "professor": prof,
            "cursos_e_turmas": cursos_com_turmas
        })

    return resultado
