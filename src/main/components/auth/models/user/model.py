from sqlalchemy import Column, Integer, String

from src.core.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    __secured_fields__ = ('password',)

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
