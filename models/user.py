from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class UserAddress(BaseModel):
    addStreet1: str
    addrStreet2: str
    city: str
    state: str
    country: str
    zip: int

class UserCreate(UserBase):
    password: str
    address: UserAddress

class UserLogin(BaseModel):
    email: str
    password: str


