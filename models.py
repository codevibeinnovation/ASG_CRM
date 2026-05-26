from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Date,
    Time,
    Float
)

from sqlalchemy.orm import relationship

from database import Base

from datetime import datetime


# =========================
# USER MODEL
# =========================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True
    )

    name = Column(String)

    email = Column(
        String,
        unique=True
    )

    password = Column(String)

    role = Column(String, nullable=False)

    clients = relationship(
        "Client",
        back_populates="creator"
    )


# =========================
# CLIENT MODEL
# =========================

class Client(Base):

    __tablename__ = "clients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    pharmacy_name = Column(
        String,
        nullable=False
    )

    contact_person = Column(String)

    Mobile_No = Column(
        String(10),
        nullable=False
    )

    email = Column(String)

    lead_source = Column(String)

    address = Column(String)

    city_id = Column(
        Integer,
        ForeignKey("cities.id")
    )

    area_id = Column(
        Integer,
        ForeignKey("areas.id")
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id")
    )

    creator = relationship(
        "User",
        back_populates="clients"
    )
    created_by = Column(
    Integer,
    ForeignKey("users.id")
    )

    city = relationship("City")

    area = relationship("Area")

    call_logs = relationship(
        "CallLog",
        back_populates="client"
    )

    demos = relationship(
        "Demo",
        back_populates="client"
    )

    deals = relationship(
        "Deal",
        back_populates="client"
    )

    reminders = relationship(
        "Reminder",
        back_populates="client"
    )


# =========================
# CITY MODEL
# =========================

class City(Base):

    __tablename__ = "cities"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True
    )

    areas = relationship(
        "Area",
        back_populates="city"
    )


# =========================
# AREA MODEL
# =========================

class Area(Base):

    __tablename__ = "areas"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    city_id = Column(
        Integer,
        ForeignKey("cities.id")
    )

    city = relationship(
        "City",
        back_populates="areas"
    )


# =========================
# EXISTING PRODUCT
# =========================

class ExistingProduct(Base):

    __tablename__ = "existing_products"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_name = Column(
        String,
        unique=True,
        nullable=False
    )


# =========================
# CALL LOG MODEL
# =========================

class CallLog(Base):

    __tablename__ = "call_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    existing_product_id = Column(
        Integer,
        ForeignKey("existing_products.id"),
        nullable=True
    )

    lead_status = Column(
        String,
        nullable=False
    )

    remarks = Column(String)

    follow_up_date = Column(Date)

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    created_time = Column(
        Time,
        default=lambda: datetime.now().time()
    )

    existing_product = relationship(
        "ExistingProduct"
    )

    client = relationship(
        "Client",
        back_populates="call_logs"
    )


# =========================
# DEMO MODEL
# =========================

class Demo(Base):

    __tablename__ = "demos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    assigned_employee_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    demo_date = Column(Date)

    demo_time = Column(Time)

    demo_feedback = Column(String)

    meeting_notes = Column(String)

    demo_status = Column(String)

    demo_location = Column(String)

    # NEW INSTALLATION SYSTEM

    demo_installed = Column(
        String,
        default="no"
    )

    installation_date = Column(Date)

    trial_days = Column(
        Integer,
        default=10
    )

    trial_expiry_date = Column(Date)

    trial_status = Column(
        String,
        default="active"
    )

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    created_time = Column(
        Time,
        default=lambda: datetime.now().time()
    )

    client = relationship(
        "Client",
        back_populates="demos"
    )

    assigned_employee = relationship(
        "User"
    )


# =========================
# DEAL MODEL
# =========================

class Deal(Base):

    __tablename__ = "deals"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    deal_owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    deal_name = Column(String)

    software_type = Column(String)

    amount = Column(Float)

    number_of_devices = Column(Integer)

    start_date = Column(Date)

    end_date = Column(Date)

    renewal_reminder_date = Column(Date)

    renewal_status = Column(
        String,
        default="active"
    )

    notes = Column(String)

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    created_time = Column(
        Time,
        default=lambda: datetime.now().time()
    )

    client = relationship(
        "Client",
        back_populates="deals"
    )

    deal_owner = relationship(
        "User"
    )


# =========================
# REMINDER MODEL
# =========================

class Reminder(Base):

    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String, nullable=True)

    reminder_date = Column(Date, nullable=False)

    reminder_time = Column(Time, nullable=True)

    status = Column(String, default="pending")

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    client_id = Column(
        Integer,
        ForeignKey("clients.id"),
        nullable=True
    )

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    user = relationship("User")

    client = relationship("Client")