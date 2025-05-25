
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List

class UserBase(SQLModel):
    name: str
    email: str

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    profile: Optional["Profile"] = Field(default=None, foreign_key="user")
    produtos: List["Product"] = Relationship(back_populates="vendedor")
    pedidos: Optional["Orders"] = Relationship(back_populates="comprador")

class UserCreate(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    profile: Optional["Profile"] = Field(default=None, foreign_key="user")
    produtos: List["Product"] = Relationship(back_populates="vendedor")
    pedidos: Optional["Orders"] = Relationship(back_populates="comprador")

class UserRead(UserBase):
    id: int
    profile: Optional["Profile"] = None
    produtos: List["Product"] = []
    pedidos: Optional["Orders"] = None


    