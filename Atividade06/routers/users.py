from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from models.database import get_db
from models.models import Category, Comment, Post, PostCategory, User
from models.schemas import UserSchema, UserCreate

# Roteador CRUD automático para User
router = SQLAlchemyCRUDRouter(
    schema=UserSchema,
    create_schema=UserCreate,
    db_model=User,
    db=get_db,
    prefix="users"
)

@router.get("/posts/", tags=["Posts"])
def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post).offset(skip).limit(limit).all()

# Posts mais comentados
@router.get("/posts/most_commented/", tags=["Posts"])
def most_commented(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post, func.count(Comment.id).label("comment_count"))\
             .join(Comment)\
             .group_by(Post.id)\
             .order_by(func.count(Comment.id).desc())\
             .offset(skip).limit(limit).all()

# Contagem de posts por categoria
@router.get("/categories/with_post_count/", tags=["Categorias"])
def categories_with_post_count(db: Session = Depends(get_db)):
    return db.query(Category.name, func.count(PostCategory.post_id).label("post_count"))\
             .join(PostCategory, Category.id == PostCategory.category_id)\
             .group_by(Category.id)\
             .order_by(func.count(PostCategory.post_id).desc()).all()