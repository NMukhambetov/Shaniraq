from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Shanyrak(Base):
    __tablename__ = 'shanyraks'

    shanyrak_id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    address = Column(String, nullable=False)
    area = Column(Float, nullable=False)
    rooms_count = Column(Integer, nullable=False)
    description = Column(String, nullable=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    user = relationship("User", back_populates="shanyraks")
    comments = relationship("Comment", back_populates="shanyrak")