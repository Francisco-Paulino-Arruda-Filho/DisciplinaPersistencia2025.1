from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    inscricoes = relationship("Inscricao", back_populates="curso")