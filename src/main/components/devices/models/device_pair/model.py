from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.core.db import BaseModel


class DevicePairModel(BaseModel):  # TODO: Validators
    __tablename__ = 'device_pairs'

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    device_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("UserModel", foreign_keys=[user_id])
    device = relationship("UserModel", foreign_keys=[device_id])
