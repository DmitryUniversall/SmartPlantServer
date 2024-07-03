from datetime import datetime

from sqlalchemy import Column, Integer, String, Boolean, DateTime

from src.core.db import BaseModel


class UserModel(BaseModel):
    __tablename__ = 'users'
    __secured_fields__ = ('password',)

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(300), nullable=False)
    is_device = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
