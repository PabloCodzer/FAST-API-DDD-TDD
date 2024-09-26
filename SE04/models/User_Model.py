from typing import Optional, List
from sqlmodel import Field, SQLModel # type: ignore
from sqlmodel import Relationship # type: ignore

class User_Model(SQLModel, table=True):
    __tablename__ = 'users'

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str
    password: str

class Photo_Model(SQLModel, table=True):
    __tablename__ = 'photos'
    id: Optional[int] = Field(default=None, primary_key=True)
    nome: str
    user_id: int