from pydantic import BaseModel, EmailStr
from typing import Optional


class SignupSchema(BaseModel):

    name: str

    email: EmailStr

    phone: str

    password: str

class LoginSchema(BaseModel):

    email: EmailStr

    password: str

class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    phone: str

    class Config:

        from_attributes = True

class ClientCreate(BaseModel):
    pharmacy_name: str
    contact_person: Optional[str] = None
    phone_number: str
    email: Optional[str] = None
    city: Optional[str] = None


class ClientResponse(BaseModel):
    id: int
    pharmacy_name: str
    contact_person: Optional[str]
    phone_number: str
    email: Optional[str]
    city: Optional[str]

    class Config:
        from_attributes = True