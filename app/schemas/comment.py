from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str

class CommentRead(BaseModel):
    comment_id: int
    content: str
    created_at: datetime
    author_id: int

    model_config = ConfigDict(from_attributes=True)

class CommentListResponse(BaseModel):
    comments: List[CommentRead]
