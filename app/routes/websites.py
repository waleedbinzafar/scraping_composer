from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter()

@router.post("/create", response_model=schemas.WebsiteOut)
def create_website(website: schemas.WebsiteCreate, db: Session = Depends(get_db)):
    existing = crud.get_website_by_name(db, website.name)
    if existing:
        raise HTTPException(status_code=400, detail="Website already exists")
    return crud.create_website(db, website)