import uuid
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, ConfigDict, Field


# ---------- Users ----------

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72) # plain text in the request; hashed before it ever touches the DB


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # lets this read straight from a SQLAlchemy object

    id: uuid.UUID
    username: str
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: datetime
    # note: password_hash is deliberately NOT here — this is what keeps it out of API responses


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Posts ----------

class PostCreate(BaseModel):
    caption: Optional[str] = None
    # image itself arrives as a file upload (multipart), not in this JSON body


class PostOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    owner_id: uuid.UUID
    caption: Optional[str] = None
    image_url: str
    has_embedding: bool
    created_at: datetime


# ---------- Follows ----------

class FollowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    follower_id: uuid.UUID
    following_id: uuid.UUID
    created_at: datetime


# ---------- Profile (composite response, not a table) ----------

class ProfileOut(BaseModel):
    user: UserOut
    posts: List[PostOut]
    follower_count: int
    following_count: int