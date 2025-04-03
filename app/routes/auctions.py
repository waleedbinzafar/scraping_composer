from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app import schemas, crud, models
from app.database import get_db

router = APIRouter()

@router.post("/create", response_model=schemas.AuctionOut)
def create_auction(auction: schemas.AuctionCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_auction(db, auction)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/random", response_model=schemas.AuctionOut)
def get_random_auction(db: Session = Depends(get_db)):
    random_auction = db.query(models.Auction).order_by(func.random()).first()
    if not random_auction:
        raise HTTPException(status_code=404, detail="No auctions found")
    return random_auction

@router.get("/random-without-lots", response_model=schemas.AuctionOut)
def get_random_auction_without_lots(db: Session = Depends(get_db)):
    random_auction = (
        db.query(models.Auction)
        .outerjoin(models.Lot)
        .filter(models.Lot.id == None)  # Filter auctions with no lots
        .order_by(func.random())
        .first()
    )
    if not random_auction:
        raise HTTPException(status_code=404, detail="No auctions without lots found")
    return random_auction