from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship


class Equipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    descricao: Optional[str] = None

    membros: List["Membro"] = Relationship(back_populates="equipe")
    projetos: List["Projeto"] = Relationship(back_populates="equipe")


class Membro(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    equipe_id: int = Field(foreign_key="equipe.id")

    equipe: Optional["Equipe"] = Relationship(back_populates="membros")
    memberships: List["Membership"] = Relationship(back_populates="membro")


class Projeto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    descricao: Optional[str] = None
    equipe_id: int = Field(foreign_key="equipe.id")

    equipe: Optional["Equipe"] = Relationship(back_populates="projetos")
    tarefas: List["Tarefa"] = Relationship(back_populates="projeto")
    memberships: List["Membership"] = Relationship(back_populates="projeto")


class Tarefa(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descricao: Optional[str] = None
    projeto_id: int = Field(foreign_key="projeto.id")

    projeto: Optional["Projeto"] = Relationship(back_populates="tarefas")


class Membership(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    membro_id: int = Field(foreign_key="membro.id")
    projeto_id: int = Field(foreign_key="projeto.id")

    membro: Optional["Membro"] = Relationship(back_populates="memberships")
    projeto: Optional["Projeto"] = Relationship(back_populates="memberships")