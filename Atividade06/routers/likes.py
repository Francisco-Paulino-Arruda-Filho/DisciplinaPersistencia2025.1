from fastapi import Depends
from fastapi_crudrouter import SQLAlchemyCRUDRouter
from requests import Session
from sqlalchemy import func
from models.models import Category, Comment, Post, PostCategory
from models.database import get_db
from models.schemas import LikeSchema, LikeBase

router = SQLAlchemyCRUDRouter(
    schema=LikeBase,
    create_schema=LikeSchema,
    db_model=Post,
    db=get_db,
    prefix="posts"
)