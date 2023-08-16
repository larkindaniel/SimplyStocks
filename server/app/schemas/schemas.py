from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

# For use with Cognito
class User(BaseModel):
    email: str
    password: str

class AccountBase(BaseModel):
    name: str
    email: str

class AccountCreate(AccountBase):
    password: str

class Account(AccountBase):
    id: UUID
    equity: float
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True