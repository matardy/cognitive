from pydantic import BaseModel

class UserBase(BaseModel):
    user_id: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
