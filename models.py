from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database import Base

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    zip_code = Column(String, nullable=False)
    purchase_price = Column(Float, nullable=False)
    estimated_value = Column(Float)
    renovation_cost = Column(Float)
    status = Column(String, nullable=False)
    acquisition_date = Column(Date)
    sale_date = Column(Date)
    notes = Column(String)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")  # New role field

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Investor(Base):
    __tablename__ = "investors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    total_investment = Column(Float, default=0)

    deals = relationship("Deal", back_populates="investor") # Links investors to deals

class Deal(Base):
    __tablename__ = "deals"

    id = Column(Integer, primary_key=True, index=True)
    property_address = Column(String, nullable=False)
    purchase_price = Column(Float, nullable=False)
    estimated_value = Column(Float)
    renovation_cost = Column(Float)
    status = Column(String, nullable=False)  # e.g., "Under Contract", "Closed"
    closing_date = Column(Date)
    investor_id = Column(Integer, ForeignKey("investors.id"), nullable=True)
    notes = Column(String)

    investor = relationship("Investor", back_populates="deals") 
