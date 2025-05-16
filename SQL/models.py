from pytdantic import BaseModel # type: ignore

class Usuario(BaseModel):
    id: int
    nome: str
    email: str

class Pedido(BaseModel):
    id: int
    usuario_id: int
    data_pedido: str  # Use str to represent datetime in JSON
    status: str

class Produto(BaseModel):
    id: int
    nome: str
    preco: float