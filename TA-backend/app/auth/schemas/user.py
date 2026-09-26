from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    email: EmailStr
    created_at: datetime

class TokenResponse(BaseModel):
    access_token: str
    token_type: str