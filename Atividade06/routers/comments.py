from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from requests import Session
from sqlalchemy import func
from models.models import Category, Comment, Post, PostCategory
from models.database import get_db
from models.schemas import CommentCreate, CommentSchema

router = SQLAlchemyCRUDRouter(
    schema=CommentCreate,
    create_schema=CommentSchema,
    db_model=Post,
    db=get_db,
    prefix="posts"
)