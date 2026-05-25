from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import date, time

class UserCreate(BaseModel):

    name: str

    email: EmailStr

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

    class Config:

        from_attributes = True

class ClientCreate(BaseModel):
    pharmacy_name: str
    contact_person: Optional[str] = None
    Mobile_No: str
    email: Optional[str] = None
    lead_source: Optional[str] = None
    address: Optional[str] = None
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
    lead_source: Optional[str] = None
    address: Optional[str] = None
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

    lead_status: str

    remarks: Optional[str] = None

    follow_up_date: Optional[date] = None

class CallLogResponse(BaseModel):
    id: int

    client_id: int

    existing_product_id: Optional[int]

    lead_status: str

    remarks: Optional[str]

    follow_up_date: Optional[date]

    created_date: date

    created_time: time

    existing_product: Optional[ExistingProductResponse]

    class Config:
        from_attributes = True

class DemoCreate(BaseModel):

    client_id: int

    assigned_employee: str

    demo_date: date

    demo_time: time

    demo_feedback: Optional[str] = None

    meeting_notes: Optional[str] = None

    demo_status: str

    
class DemoResponse(BaseModel):

    id: int

    client_id: int

    assigned_employee: str

    demo_date: date

    demo_time: time

    demo_feedback: Optional[str]

    meeting_notes: Optional[str]

    demo_location: Optional[str]

    demo_status: str

    created_date: date

    created_time: time

    class Config:

        from_attributes = True

class DealCreate(BaseModel):

    client_id: int

    deal_person_name: str

    deal_name: str

    contact_person_name: Optional[str] = None

    amount: float

    closing_date: Optional[date] = None

    description: Optional[str] = None

    number_of_devices: Optional[int] = None

    software_type: str


class DealResponse(DealCreate):

    id: int

    created_date: date

    created_time: time

    class Config:

        from_attributes = True