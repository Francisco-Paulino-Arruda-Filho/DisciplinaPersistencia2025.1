from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import Column, Integer, ForeignKey

Base = declarative_base()

class Inscricao(Base):
    __tablename__ = "inscricoes"

    id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"), nullable=False)

    aluno = relationship("Aluno", back_populates="inscricoes")
    curso = relationship("Curso", back_populates="inscricoes")