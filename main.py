from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, Base, get_db

# Initialize FastAPI app
app = FastAPI()

# Create tables in the database
Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to the Real Estate API"}

# Add new property
@app.post("/properties/", response_model=schemas.PropertyResponse)
def create_property(property: schemas.PropertyCreate, db: Session = Depends(get_db)):
    db_property = models.Property(**property.dict())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property

# Fetch all properties
@app.get("/properties/", response_model=list[schemas.PropertyResponse])
def get_properties(db: Session = Depends(get_db)):
    return db.query(models.Property).all()
