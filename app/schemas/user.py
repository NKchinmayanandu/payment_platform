from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    phone_number: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}    