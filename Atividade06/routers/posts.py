# routers/posts.py

from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from requests import Session
from sqlalchemy import func
from models.models import Category, Comment, Post, PostCategory
from models.database import get_db
from models.schemas import PostSchema, PostCreate

router = SQLAlchemyCRUDRouter(
    schema=PostSchema,
    create_schema=PostCreate,
    db_model=Post,
    db=get_db,
    prefix="posts"
)

@router.get("/posts/")
async def list_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post).offset(skip).limit(limit).all()

@router.get("/posts/most_commented/")
def most_commented(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Post, func.count(Comment.id).label("comment_count"))\
             .join(Comment)\
             .group_by(Post.id)\
             .order_by(func.count(Comment.id).desc())\
             .offset(skip).limit(limit).all()

@router.get("/categories/with_post_count/")
def categories_with_post_count(db: Session = Depends(get_db)):
    return db.query(Category.name, func.count(PostCategory.post_id).label("post_count"))\
             .join(PostCategory, Category.id == PostCategory.category_id)\
             .group_by(Category.id)\
             .order_by(func.count(PostCategory.post_id).desc()).all()
