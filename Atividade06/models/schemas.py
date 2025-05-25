from typing import List, Optional
from pydantic import BaseModel

# === USER ===
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserSchema(UserBase):
    id: int
    class Config:
        orm_mode = True

# === CATEGORY ===
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategorySchema(CategoryBase):
    id: int
    class Config:
        orm_mode = True

# === POST ===
class PostBase(BaseModel):
    title: str
    content: str
    author_id: int
    category_ids: Optional[List[int]] = []  # IDs das categorias vinculadas

class PostCreate(PostBase):
    pass

class PostSchema(PostBase):
    id: int
    class Config:
        orm_mode = True

# === COMMENT ===
class CommentBase(BaseModel):
    content: str
    post_id: int
    user_id: int

class CommentCreate(CommentBase):
    pass

class CommentSchema(CommentBase):
    id: int
    class Config:
        orm_mode = True

# === LIKE ===
class LikeBase(BaseModel):
    user_id: int
    post_id: int

class LikeCreate(LikeBase):
    pass

class LikeSchema(LikeBase):
    id: int
    class Config:
        orm_mode = True
