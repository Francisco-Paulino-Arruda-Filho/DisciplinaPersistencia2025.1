from fastapi import APIRouter, Depends, UploadFile, HTTPException
import unicodedata
from typing import List
from sqlmodel import select
from database import get_session
from models import BensEDireitos
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

router = APIRouter()

COLUNAS_BENS_E_DIREITOS = {
    "ano_calendario": "ano_calendario",
    "rendimentos_tributaveis": "rendimentos_tributaveis",
    "redimentos_isentos": "rendimentos_isentos",
    "deducoes_previdenciarias_totais": "deducoes_previdenciarias_totais",
    "imposto_devido": "imposto_devido",
    "bens_e_direitos": "bens_e_direitos",
    "capital_estado_id": "capital_estado_id",
}

def normalize_column_name(column_name: str) -> str:
    """
    Normalize the column name by removing accents and converting to lowercase.
    """
    normalized_name = unicodedata.normalize('NFKD', column_name).encode('ASCII', 'ignore').decode('utf-8')
    return normalized_name.lower().replace(" ", "_")

@router.post("/upload/bens_e_direitos/")
async def bens_e_direitos_upload(file: UploadFile, session: AsyncSession = Depends(get_session)):
    try:
        df = pd.read_csv(file.file, sep=';', encoding='utf-8')
        df.columns = [normalize_column_name(col) for col in df.columns]
        colunas_para_usar = {csv: model_col for csv, model_col in COLUNAS_BENS_E_DIREITOS.items() if csv in df.columns}
        df = df.rename(columns=colunas_para_usar)[list(colunas_para_usar.values())]

        registros = [BensEDireitos(**row) for index, row in df.iterrows()]

        session.add_all(registros)
        await session.commit()
        return {"message": "Dados de bens e direitos carregados com sucesso."}  
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao processar o arquivo: {str(e)}")
    
@router.get("/bens_e_direitos/", response_model=List[BensEDireitos])
async def get_bens_e_direitos(session: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100):
    try:
        statement = select(BensEDireitos).offset(skip).limit(limit)
        result = await session.execute(statement)
        bens_e_direitos = result.scalars().all()
        return bens_e_direitos
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao buscar bens e direitos: {str(e)}")
    
