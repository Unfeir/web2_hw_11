from datetime import date
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone_number: str = Field(max_length=20)
    birthday: date = Field(default=date(year=1900, month=1, day=1))
    address: str = Field(max_length=200)


class ContactsResponse(ContactModel):

    class Config:
        orm_mode = True