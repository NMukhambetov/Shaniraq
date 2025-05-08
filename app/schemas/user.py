from pydantic import BaseModel, Field

class UserBase(BaseModel):
    user_email: str
    phone: str = Field(..., pattern=r"^(\+7|8)\d{10}$")
    name: str
    city: str

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(BaseModel):
    phone: str = Field(..., pattern=r"^(\+7|8)\d{10}$")
    name: str
    city: str

class UserRead(UserBase):
    user_id: int

    class Config:
        from_attributes = True