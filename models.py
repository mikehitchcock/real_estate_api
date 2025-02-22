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
