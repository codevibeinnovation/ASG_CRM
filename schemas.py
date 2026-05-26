from pydantic import (
    BaseModel,
    EmailStr
)

from datetime import (
    date,
    time
)

from typing import Optional


# =========================
# USER SCHEMAS
# =========================

class UserCreate(BaseModel):

    name: str

    email: EmailStr

    password: str

    role: str = "user"


class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr

    role: str

    class Config:

        from_attributes = True


# =========================
# LOGIN SCHEMAS
# =========================

class LoginSchema(BaseModel):

    email: EmailStr

    password: str


class Token(BaseModel):

    access_token: str

    token_type: str


# =========================
# CITY SCHEMAS
# =========================

class CityCreate(BaseModel):

    name: str


class CityResponse(BaseModel):

    id: int

    name: str

    class Config:

        from_attributes = True


# =========================
# AREA SCHEMAS
# =========================

class AreaCreate(BaseModel):

    name: str

    city_id: int


class AreaResponse(BaseModel):

    id: int

    name: str

    city_id: int

    class Config:

        from_attributes = True


# =========================
# CLIENT SCHEMAS
# =========================

class ClientCreate(BaseModel):

    pharmacy_name: str

    contact_person: Optional[str] = None

    Mobile_No: str

    email: Optional[EmailStr] = None

    lead_source: Optional[str] = None

    address: Optional[str] = None

    city_id: int

    area_id: int


class ClientResponse(BaseModel):

    id: int

    pharmacy_name: str

    contact_person: Optional[str]

    Mobile_No: str

    email: Optional[EmailStr]

    lead_source: Optional[str]

    address: Optional[str]

    city_id: int

    area_id: int

    created_by: int

    class Config:

        from_attributes = True


# =========================
# EXISTING PRODUCT
# =========================

class ExistingProductCreate(BaseModel):

    product_name: str


class ExistingProductResponse(BaseModel):

    id: int

    product_name: str

    class Config:

        from_attributes = True


# =========================
# CALL LOG SCHEMAS
# =========================

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

    class Config:

        from_attributes = True


# =========================
# DEMO SCHEMAS
# =========================

class DemoCreate(BaseModel):

    client_id: int

    assigned_employee_id: int

    demo_date: date

    demo_time: time

    demo_feedback: Optional[str] = None

    meeting_notes: Optional[str] = None

    demo_status: str

    demo_location: Optional[str] = None

    demo_installed: str = "no"

    installation_date: Optional[date] = None

    trial_days: int = 10


class DemoResponse(BaseModel):

    id: int

    client_id: int

    assigned_employee_id: int

    demo_date: date

    demo_time: time

    demo_feedback: Optional[str]

    meeting_notes: Optional[str]

    demo_status: str

    demo_location: Optional[str]

    demo_installed: str

    installation_date: Optional[date]

    trial_days: int

    trial_expiry_date: Optional[date]

    trial_status: str

    class Config:

        from_attributes = True


# =========================
# DEAL SCHEMAS
# =========================

class DealCreate(BaseModel):

    client_id: int

    deal_owner_id: int

    deal_name: str

    software_type: str

    amount: float

    number_of_devices: int

    start_date: date

    end_date: date

    notes: Optional[str] = None


class DealResponse(BaseModel):

    id: int

    client_id: int

    deal_owner_id: int

    deal_name: str

    software_type: str

    amount: float

    number_of_devices: int

    start_date: date

    end_date: date

    renewal_reminder_date: Optional[date]

    renewal_status: str

    notes: Optional[str]

    class Config:

        from_attributes = True


# =========================
# REMINDER SCHEMAS
# =========================

class ReminderCreate(BaseModel):

    title: str

    description: str | None = None

    reminder_date: date

    reminder_time: time | None = None

    user_id: int

    client_id: int | None = None

class ReminderResponse(BaseModel):

    id: int

    title: str

    description: str | None = None

    reminder_date: date

    reminder_time: time | None = None

    status: str

    user_id: int

    client_id: int | None = None

    created_date: date

    class Config:

        from_attributes = True