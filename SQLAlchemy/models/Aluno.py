from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    inscricoes = relationship("Inscricao", back_populates="aluno")