from pydantic import *

class ShanyrakCreate(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str

class ShanyrakRead(BaseModel):
    shanyrak_id: int
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str
    user_id: int
    total_comments: int = 0

    model_config = ConfigDict(from_attributes=True)

class ShanyrakUpdate(BaseModel):
    type: str
    price: int
    address: str
    area: float
    rooms_count: int
    description: str