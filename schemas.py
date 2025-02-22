from pydantic import BaseModel
from typing import Optional
from datetime import date

class PropertyCreate(BaseModel):
    address: str
    city: str
    state: str
    zip_code: str
    purchase_price: float
    estimated_value: Optional[float] = None
    renovation_cost: Optional[float] = None
    status: str
    acquisition_date: Optional[date] = None
    sale_date: Optional[date] = None
    notes: Optional[str] = None

class PropertyResponse(PropertyCreate):
    id: int
    class Config:
        from_attributes = True
