from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Projeto

router = APIRouter(prefix="/projetos", tags=["Projetos"])

@router.post("", response_model=Projeto)
def criar_projeto(projeto: Projeto, session: Session = Depends(get_session)):
    session.add(projeto)
    session.commit()
    session.refresh(projeto)
    return projeto

@router.get("", response_model=list[Projeto])
def listar_projetos(session: Session = Depends(get_session)):
    projetos = session.exec(select(Projeto)).all()
    return projetos

@router.get("/{projeto_id}", response_model=Projeto)
def obter_projeto(projeto_id: int, session: Session = Depends(get_session)):
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projeto

@router.put("/{projeto_id}", response_model=Projeto)
def atualizar_projeto(projeto_id: int, projeto: Projeto, session: Session = Depends(get_session)):
    db_projeto = session.get(Projeto, projeto_id)
    if not db_projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    projeto_data = projeto.model_dump(exclude_unset=True)
    for key, value in projeto_data.items():
        setattr(db_projeto, key, value)  
    session.add(db_projeto)
    session.commit()
    session.refresh(db_projeto)
    return db_projeto

@router.delete("/{projeto_id}", response_model=Projeto)
def deletar_projeto(projeto_id: int, session: Session = Depends(get_session)):
    projeto = session.get(Projeto, projeto_id)
    if not projeto:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    session.delete(projeto)
    session.commit()
    return projeto