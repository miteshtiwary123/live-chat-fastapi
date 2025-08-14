from pydantic import BaseModel
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    sender_id: int

class MessageResponse(MessageBase):
    id: int
    timestamp: datetime
    senser: UserResponse
    class Config:
        orm_mode = True