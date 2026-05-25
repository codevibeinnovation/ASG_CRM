from sqlalchemy import Column, ForeignKey, Integer, String,Date, Time
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    email = Column(String, unique=True, nullable=False)

    password = Column(String, nullable=False)

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    pharmacy_name = Column(String, nullable=False)
    contact_person = Column(String, nullable=True)
    Mobile_No = Column(String(10), nullable=False)
    email = Column(String, nullable=True)
    lead_source = Column(String, nullable=True)
    address = Column(String, nullable=True)
    city_id = Column(Integer, ForeignKey("cities.id"))
    area_id = Column(Integer, ForeignKey("areas.id"))
    city = relationship("City")
    area = relationship("Area")
    call_logs = relationship("CallLog", back_populates="client")
    demos = relationship("Demo",back_populates="client")

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

    areas = relationship("Area", back_populates="city")

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    city_id = Column(Integer, ForeignKey("cities.id"))

    city = relationship("City", back_populates="areas")


class ExistingProduct(Base):
    __tablename__ = "existing_products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String, unique=True, nullable=False)

class CallLog(Base):
    __tablename__ = "call_logs"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(Integer, ForeignKey("clients.id"))

    existing_product_id = Column(
        Integer,
        ForeignKey("existing_products.id"),
        nullable=True
    )


    lead_status = Column(String, nullable=False)

    remarks = Column(String, nullable=True)

    follow_up_date = Column(Date, nullable=True)

    created_date = Column(Date,default=lambda: datetime.now().date())

    created_time = Column(Time,default=lambda: datetime.now().time())

    # client = relationship("Client")

    existing_product = relationship("ExistingProduct")
    
    client = relationship("Client", back_populates="call_logs")

class Demo(Base):

    __tablename__ = "demos"

    id = Column(Integer, primary_key=True, index=True)

    client_id = Column(
        Integer,
        ForeignKey("clients.id")
    )

    assigned_employee = Column(String, nullable=False)

    demo_date = Column(Date, nullable=False)

    demo_time = Column(Time, nullable=False)

    demo_feedback = Column(String, nullable=True)

    meeting_notes = Column(String, nullable=True)

    demo_status = Column(String, nullable=False)

    demo_location = Column(String, nullable=True)

    created_date = Column(
        Date,
        default=lambda: datetime.now().date()
    )

    created_time = Column(
        Time,
        default=lambda: datetime.now().time()
    )

    client = relationship("Client", back_populates="demos")