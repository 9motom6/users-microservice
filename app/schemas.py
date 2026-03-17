from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    external_id: UUID
    name: str
    email: EmailStr
    date_of_birth: datetime

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

