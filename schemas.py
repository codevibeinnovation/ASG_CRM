from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, time

class SignupSchema(BaseModel):

    name: str

    email: EmailStr

    phone: str

    password: str

class AdminLogin(BaseModel):
    email: str
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
    Mobile_No: str
    email: Optional[str] = None
    city_id: int
    area_id: int

    @field_validator("Mobile_No")
    @classmethod
    def validate_phone(cls, v):

        if not v.isdigit():
            raise ValueError(
                "Phone number must contain only numbers"
            )

        if len(v) != 10:
            raise ValueError(
                "Phone number must be 10 digits"
            )

        return v

class CityCreate(BaseModel):
    name: str

class AreaCreate(BaseModel):
    name: str
    city_id: int

class CityResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class AreaResponse(BaseModel):
    id: int
    name: str
    city_id: int

    class Config:
        from_attributes = True

class ClientResponse(BaseModel):
    id: int
    pharmacy_name: str
    contact_person: Optional[str]
    Mobile_No: str
    email: Optional[str]

    city_id: int
    area_id: int

    city: CityResponse
    area: AreaResponse

    class Config:
        from_attributes = True

class ExistingProductCreate(BaseModel):
    product_name: str


class ExistingProductResponse(BaseModel):
    id: int
    product_name: str

    class Config:
        from_attributes = True

class CallLogCreate(BaseModel):

    client_id: int

    existing_product_id: Optional[int] = None

    lead_source: Optional[str] = None

    lead_status: str

    remarks: Optional[str] = None

    follow_up_date: Optional[date] = None

class CallLogResponse(BaseModel):
    id: int

    client_id: int

    existing_product_id: Optional[int]

    lead_source: Optional[str]

    lead_status: str

    remarks: Optional[str]

    follow_up_date: Optional[date]

    created_date: date

    created_time: time

    existing_product: Optional[ExistingProductResponse]

    class Config:
        from_attributes = True