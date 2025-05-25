from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

from CRUDRouter.models.user import User

class ProductBase(SQLModel):
    nome: str
    descricao: str
    preco: float

class ProductCreate(ProductBase, table=True):
    __tablename__ = "produtos"
    id: Optional[int] = Field(default=None, primary_key=True)
    vendedor: Optional["User"] = Field(default=None, foreign_key="user")
    pedidos: List["Orders"] = Relationship(back_populates="produtos")

class ProductRead(ProductBase):
    id: int
    vendedor: Optional["User"] = None
    pedidos: List["Orders"] = []