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

from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str

from typing import Optional
from datetime import date

class DealCreate(BaseModel):
    property_address: str
    purchase_price: float
    estimated_value: Optional[float] = None
    renovation_cost: Optional[float] = None
    status: str
    closing_date: Optional[date] = None
    investor_id: Optional[int] = None
    notes: Optional[str] = None

class DealResponse(DealCreate):
    id: int

from pydantic import BaseModel, EmailStr
from typing import Optional

class InvestorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    total_investment: float = 0

class InvestorResponse(InvestorCreate):
    id: int
