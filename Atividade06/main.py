from fastapi import FastAPI
from models.database import create_db_and_tables
from routers import users, posts, categories, comments, likes

app = FastAPI(title="API de Blog Pessoal")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(users.router, prefix="/users", tags=["Usuários"])
app.include_router(posts.router, prefix="/posts", tags=["Posts"])
app.include_router(categories.router, prefix="/categories", tags=["Categorias"])
app.include_router(comments.router, prefix="/comments", tags=["Comentários"])
app.include_router(likes.router, prefix="/likes", tags=["Curtidas"])
