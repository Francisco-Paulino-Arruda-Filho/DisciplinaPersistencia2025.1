from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Equipe, Membro

router = APIRouter(prefix="/equipes", tags=["Equipes"])

@router.post("", response_model=Equipe)
def criar_equipe(equipe: Equipe, session: Session = Depends(get_session)):
    session.add(equipe)
    session.commit()
    session.refresh(equipe)
    return equipe

@router.get("", response_model=list[Equipe])
def listar_equipes(session: Session = Depends(get_session)):
    equipes = session.exec(select(Equipe)).all()
    return equipes

@router.get("/{equipe_id}", response_model=Equipe)
def obter_equipe(equipe_id: int, session: Session = Depends(get_session)):
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    return equipe

@router.put("/{equipe_id}", response_model=Equipe)  
def atualizar_equipe(equipe_id: int, equipe: Equipe, session: Session = Depends(get_session)):
    db_equipe = session.get(Equipe, equipe_id)
    if not db_equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    equipe_data = equipe.model_dump(exclude_unset=True)
    for key, value in equipe_data.items():
        setattr(db_equipe, key, value)  
    session.add(db_equipe)
    session.commit()
    session.refresh(db_equipe)
    return db_equipe

@router.delete("/{equipe_id}", response_model=Equipe)
def deletar_equipe(equipe_id: int, session: Session = Depends(get_session)):
    equipe = session.get(Equipe, equipe_id)
    if not equipe:
        raise HTTPException(status_code=404, detail="Equipe não encontrada")
    session.delete(equipe)
    session.commit()
    return equipe