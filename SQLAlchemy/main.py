from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.Aluno import Aluno
from models.Curso import Curso
from models.Inscricao import Inscricao
from database import get_db

app = FastAPI()

app.get("/alunos/")
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(Aluno).all()
    return alunos

@app.get("/alunos/")
def criar_aluno(nome: str, idade: int, db: Session = Depends(get_db)):
    db_aluno = Aluno(nome=nome, idade=idade)
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@app.get("/alunos/{aluno_id}")
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return db_aluno

@app.put("/alunos/{aluno_id}")
def atualizar_aluno(aluno_id: int, nome: str, idade: int, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db_aluno.nome = nome
    db_aluno.idade = idade
    db.commit()
    db.refresh(db_aluno)
    return db_aluno

@app.delete("/alunos/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(db_aluno)
    db.commit()
    return {"message": "Aluno deletado com sucesso"}

@app.post("/cursos/")
def criar_curso(nome: str, descricao: str, db: Session = Depends(get_db)):
    db_curso = Curso(nome=nome, descricao=descricao)
    db.add(db_curso)
    db.commit()
    db.refresh(db_curso)
    return db_curso

@app.get("/cursos/")
def listar_cursos(db: Session = Depends(get_db)):
    cursos = db.query(Curso).all()
    return cursos

@app.get("/cursos/{curso_id}")
def obter_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return db_curso

@app.put("/cursos/{curso_id}")
def atualizar_curso(curso_id: int, nome: str, descricao: str, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db_curso.nome = nome
    db_curso.descricao = descricao
    db.commit()
    db.refresh(db_curso)
    return db_curso

@app.delete("/cursos/{curso_id}")
def deletar_curso(curso_id: int, db: Session = Depends(get_db)):
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db.delete(db_curso)
    db.commit()
    return {"message": "Curso deletado com sucesso"}

@app.post("/inscricoes/")
def criar_inscricao(aluno_id: int, curso_id: int, db: Session = Depends(get_db)):
    db_aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db_curso = db.query(Curso).filter(Curso.id == curso_id).first()
    if db_curso is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    db_inscricao = Inscricao(aluno_id=aluno_id, curso_id=curso_id)
    db.add(db_inscricao)
    db.commit()
    db.refresh(db_inscricao)
    return db_inscricao

@app.get("/inscricoes/")
def listar_inscricoes(db: Session = Depends(get_db)):
    inscricoes = db.query(Inscricao).all()
    return inscricoes