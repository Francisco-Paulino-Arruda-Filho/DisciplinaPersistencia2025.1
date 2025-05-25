from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Membro

router = APIRouter(prefix="/membros", tags=["Membros"])

@router.post("", response_model=Membro)
def criar_membro(membro: Membro, session: Session = Depends(get_session)):
    session.add(membro)
    session.commit()
    session.refresh(membro)
    return membro

@router.get("", response_model=list[Membro])
def listar_membros(session: Session = Depends(get_session)):
    membros = session.exec(select(Membro)).all()
    return membros

@router.get("/{membro_id}", response_model=Membro)
def obter_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    return membro

@router.put("/{membro_id}", response_model=Membro)
def atualizar_membro(membro_id: int, membro: Membro, session: Session = Depends(get_session)):
    db_membro = session.get(Membro, membro_id)
    if not db_membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    membro_data = membro.model_dump(exclude_unset=True)
    for key, value in membro_data.items():
        setattr(db_membro, key, value)  
    session.add(db_membro)
    session.commit()
    session.refresh(db_membro)
    return db_membro

@router.delete("/{membro_id}", response_model=Membro)
def deletar_membro(membro_id: int, session: Session = Depends(get_session)):
    membro = session.get(Membro, membro_id)
    if not membro:
        raise HTTPException(status_code=404, detail="Membro não encontrado")
    session.delete(membro)
    session.commit()
    return membro