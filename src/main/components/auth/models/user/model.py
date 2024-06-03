from sqlalchemy import Column, Integer, String, Boolean, DateTime, func

from src.core.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    __secured_fields__ = ('password',)

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    is_device = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
