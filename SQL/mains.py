from fastapi import FastAPI
from crud import create_usuario, listar_usuarios, create_produto, list_produtos, create_pedido, list_pedidos, create_pedido_produto, list_pedido_produto, delete_pedido_produto, add_produto_pedido, delete_pedido_produto, update_pedido_produto, get_pedido_produto
from models import Usuario, Produto, Pedido
from db import get_connection
from psycopg2.extras import RealDictCursor

app = FastAPI()

@app.post("/usuarios/", response_model=Usuario)
def criar_usuario(nome: str, email: str):
    user_id = create_usuario(nome, email)
    return Usuario(id=user_id, nome=nome, email=email)

@app.get("/usuarios/", response_model=list[Usuario])
def pegar_usuarios():
    usuarios = listar_usuarios()
    return usuarios

@app.post("/produtos/", response_model=Produto)
def criar_produto(nome: str, preco: float):
    produto_id = create_produto(nome, preco)
    return Produto(id=produto_id, nome=nome, preco=preco)

@app.get("/produtos/", response_model=list[Produto])
def pegar_produtos():
    produtos = list_produtos()
    return produtos

@app.post("/pedidos/", response_model=Pedido)
def criar_pedido(usuario_id: int, status: str, data_pedido: str = None):
    pedido_id = create_pedido(usuario_id, status)
    return {
        "id": pedido_id,
        "usuario_id": usuario_id,
        "data_pedido": data_pedido,
        "status": status
    }

@app.get("/pedidos/", response_model=list[Pedido])
def pegar_pedidos():
    pedidos = list_pedidos()
    return pedidos

@app.post("/pedidos/{pedido_id}/produtos/")
def adicionar_produto_ao_pedido(pedido_id: int, produto_id: int, quantidade: int):
    add_produto_pedido(pedido_id, produto_id, quantidade)
    return {"message": "Produto adicionado ao pedido com sucesso."}

@app.get("usuarios/{usuario_id}/pedidos/")
def usuarios_com_pedidos(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    query = """
    SELECT u.nome, p.id, p.data_pedido
    FROM usuario u
    LEFT JOIN pedido p ON u.id = p.usuario_id
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios