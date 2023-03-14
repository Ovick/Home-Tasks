from datetime import date
from typing import Optional
from pydantic import BaseModel, Field


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    born_date: Optional[date] = None
    email: str = Field(max_length=50)
    phone_number: str = Field(max_length=50)


class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True
