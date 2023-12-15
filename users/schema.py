from pydantic import BaseModel, Field
from typing import Optional


class UserProfile(BaseModel):
    id: int = Field(alias="_id")
    profile_picture: str


class UserBase(BaseModel):
    full_name: str
    email: str
    phone: str
    profile_picture: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
