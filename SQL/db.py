import psycopg2
from psycopg2 import OperationalError

def get_connection() :
    return psycopg2.connect(
        database="ydb4",
        user="postgres",
        password="pf040502004",
        host="localhost",
        port="5432"
    )

def create_tables(): 
    try:
        connection = get_connection()
        cursor = connection.cursor()

        
        commands = [
                    """
                    CREATE TABLE IF NOT EXISTS usuario (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        email VARCHAR(100) UNIQUE NOT NULL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS pedido (
                        id SERIAL PRIMARY KEY,
                        usuario_id INT REFERENCES usuario(id),
                        data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status VARCHAR(20) NOT NULL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS produto (
                        id SERIAL PRIMARY KEY,
                        nome VARCHAR(100) NOT NULL,
                        preco DECIMAL(10, 2) NOT NULL
                    )
                    """,
                    """
                    CREATE TABLE IF NOT EXISTS pedido_produto (
                        pedido_id INT REFERENCES pedido(id),
                        produto_id INT REFERENCES produto(id),
                        quantidade INT NOT NULL,
                        PRIMARY KEY (pedido_id, produto_id)
                    )
                    """
                ]
        for command in commands:
            cursor.execute(command)

        connection.commit()
        print("Tabelas criadas com sucesso.")
    except OperationalError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        cursor.close()
        connection.close()