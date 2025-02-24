from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db
from auth import hash_password, create_access_token, verify_password, decode_access_token
from fastapi.security import OAuth2PasswordRequestForm

# Initialize FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure all tables are created in the database
Base.metadata.create_all(bind=engine)

# OAuth2 authentication scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Helper function to get the current logged-in user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Extract user from token and verify authentication"""
    try:
        payload = decode_access_token(token)
        user = db.query(models.User).filter(models.User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

# Welcome route
@app.get("/")
def home():
    return {"message": "Welcome to the Real Estate API"}

# User registration
@app.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = models.User(username=user.username, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

# User login and token generation
@app.post("/token/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and receive an access token."""
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

# Protected route example
@app.get("/protected/")
def protected_route(token: str = Depends(oauth2_scheme)):
    """Protected route that requires authentication."""
    payload = decode_access_token(token)
    return {"message": "You are authorized", "user": payload["sub"]}

# =========================
#  Properties Endpoints
# =========================
@app.post("/properties/", response_model=schemas.PropertyResponse)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

@app.get("/properties/", response_model=list[schemas.PropertyResponse])
def get_properties(db: Session = Depends(get_db)):
    return db.query(models.Property).all()

# =========================
#  Deals Endpoints
# =========================
@app.post("/deals/", response_model=schemas.DealResponse)
def create_deal(deal: schemas.DealCreate, db: Session = Depends(get_db)):
    """Create a new real estate deal."""
    new_deal = models.Deal(**deal.dict())
    db.add(new_deal)
    db.commit()
    db.refresh(new_deal)
    return new_deal

@app.get("/deals/", response_model=list[schemas.DealResponse])
def get_deals(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all deals (Login Required)."""
    return db.query(models.Deal).all()

@app.get("/deals/{deal_id}", response_model=schemas.DealResponse)
def get_deal(deal_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve a single deal by ID (Login Required)."""
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    return deal

@app.put("/deals/{deal_id}", response_model=schemas.DealResponse)
def update_deal(deal_id: int, updated_deal: schemas.DealCreate, db: Session = Depends(get_db)):
    """Update an existing deal."""
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    for key, value in updated_deal.dict(exclude_unset=True).items():
        setattr(deal, key, value)

    db.commit()
    db.refresh(deal)
    return deal

@app.delete("/deals/{deal_id}")
def delete_deal(deal_id: int, db: Session = Depends(get_db)):
    """Delete a deal."""
    deal = db.query(models.Deal).filter(models.Deal.id == deal_id).first()
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")

    db.delete(deal)
    db.commit()
    return {"message": "Deal deleted successfully"}

# =========================
#  Investors Endpoints
# =========================
@app.post("/investors/", response_model=schemas.InvestorResponse)
def create_investor(investor: schemas.InvestorCreate, db: Session = Depends(get_db)):
    """Create a new investor."""
    new_investor = models.Investor(**investor.dict())
    db.add(new_investor)
    db.commit()
    db.refresh(new_investor)
    return new_investor

@app.get("/investors/", response_model=list[schemas.InvestorResponse])
def get_investors(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve all investors (Login Required)."""
    return db.query(models.Investor).all()

@app.get("/investors/{investor_id}", response_model=schemas.InvestorResponse)
def get_investor(investor_id: int, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve a single investor by ID (Login Required)."""
    investor = db.query(models.Investor).filter(models.Investor.id == investor_id).first()
    if not investor:
        raise HTTPException(status_code=404, detail="Investor not found")
    return investor

import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", $PORT))  # Use PORT environment variable, fallback to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=port)
