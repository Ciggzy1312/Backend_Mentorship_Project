from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    password: str

class UserCreate(BaseModel):
    name: str
    email: str
    password: str