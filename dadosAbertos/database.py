from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

DATABASE_URL = "postgresql+asyncpg://postgres:pf04052004@localhost:5432/dados_abertos"

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:  
        await conn.run_sync(SQLModel.metadata.create_all) 

async def get_session():
    async with SessionLocal() as session:
        yield session
