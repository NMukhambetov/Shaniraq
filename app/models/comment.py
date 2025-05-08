from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class Comment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    author_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    shanyrak_id = Column(Integer, ForeignKey("shanyraks.shanyrak_id"), nullable=False)

    author = relationship("User", back_populates="comments")
    shanyrak = relationship("Shanyrak", back_populates="comments")