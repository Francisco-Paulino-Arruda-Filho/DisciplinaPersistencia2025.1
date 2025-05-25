from fastapi_crudrouter import SQLAlchemyCRUDRouter
from fastapi import Depends, Query
from sqlmodel import Select, Session
from models.user import User, UserCreate, UserRead

router = SQLAlchemyCRUDRouter(
    schema=UserRead,
    create_schema=UserCreate,
    db_model=User,
    db=Session,
    prefix="users",
    tags=["users"],
)

@router.get("/paginado", response_model=list[UserRead])
async def get_paginated_users(
    db: Session = Depends(Session),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
):
    """
    Get paginated users
    """
    users = db.exec(Select(User).offset(skip).limit(limit)).all()
    return users