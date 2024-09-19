from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    name: str
    pin: str
    balance: float = Field(default=0.0)
    card_type: str = Field(index=True)
    bank_account: str = Field(index=True, unique=True, max_length=6)


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: Optional[int] = Field(default=None, primary_key=True)


class User(UserRead, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
