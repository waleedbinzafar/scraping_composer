from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from app import schemas, crud, models
from app.database import get_db
from typing import List
import re
from datetime import datetime
from datetime import timedelta

router = APIRouter()

@router.post("/create", response_model=schemas.LotOut)
def create_lot(lot: schemas.LotCreate, db: Session = Depends(get_db)):
    # Check if the auction exists
    auction = crud.get_auction_by_id(db, lot.auction_id)
    if not auction:
        raise HTTPException(status_code=404, detail="Auction not found")
    # Check if the lot already exists
    existing_lot = crud.get_lot_by_link(db, str(lot.lot_link))
    if existing_lot:
        raise HTTPException(status_code=400, detail="Lot already exists")

    # Create the lot
    return crud.create_lot(db, lot)

@router.get("/random-main-lot", response_model=schemas.LotOut)
def get_random_main_lot(db: Session = Depends(get_db)):
    random_lot = (
        db.query(models.Lot)
        .filter(models.Lot.is_scraped == False)  # Only unscripted lots
        .filter(models.Lot.status == "pending")  # Only pending lots
        .filter(models.Lot.lot_number.op("~")("[a-zA-Z]$"))  # Lot number does not end with an alphabet
        .order_by(func.random())  # Randomize the order
        .first()
    )
    if not random_lot:
        raise HTTPException(status_code=404, detail="No matching lots found")
    return random_lot

@router.get("/random-main-lot-batch", response_model=List[schemas.LotOut])
def get_random_main_lot_batch(db: Session = Depends(get_db)):
    random_lots = (
        db.query(models.Lot)
        .filter(models.Lot.is_scraped == False)  # Only unscripted lots
        .filter(models.Lot.status == "pending")  # Only pending lots
        .filter(models.Lot.lot_number.op("~")("[a-zA-Z]$"))  # Lot number does not end with an alphabet
        .order_by(func.random())  # Randomize the order
        .limit(15)  # Limit to 10 results
        .all()
    )

    if not random_lots:
        raise HTTPException(status_code=404, detail="No matching lots found")
    else:
        # set the status against these lots to "processing"
        for lot in random_lots:
            lot.status = "processing"
            lot.updated_at = datetime.now()
            db.commit()
            db.refresh(lot)

    # Return the list of random lots
    return random_lots

@router.post("/reset-dangling-lots")
def reset_dangling_lots(db: Session = Depends(get_db)):
    # Update all lots with status "processing" with updated_at timestamp older than 60 minutes to "pending"
    sixty_minutes_ago = datetime.now() - timedelta(minutes=60)
    updated_rows = (
        db.query(models.Lot)
        .filter(models.Lot.status == "processing")
        .filter(models.Lot.updated_at < sixty_minutes_ago)
        .update({"status": "pending"}, synchronize_session=False)
    )
    # Commit the changes
    db.commit()
    return {"message": f"Reset {updated_rows} lots from 'processing' to 'pending'"}

@router.post("/submit-scraped-info")
def submit_scraped_info(
    lot_data: schemas.LotScrapedInfo, db: Session = Depends(get_db)
):
    # Fetch the lot by ID
    lot = db.query(models.Lot).filter(models.Lot.id == lot_data.lot_id).first()
    if not lot:
        raise HTTPException(status_code=404, detail="Lot not found")

    # Update the lot fields
    lot.price = lot_data.price
    lot.image_links = lot_data.image_links
    lot.status = "scraped"
    lot.is_scraped = True
    lot.scraped_at = datetime.now()

    # Commit the changes
    db.commit()
    db.refresh(lot)

    return {"message": "Lot updated successfully", "lot_id": lot.id}

@router.post("/reset-processing-lots")
def reset_processing_lots(db: Session = Depends(get_db)):
    # Update all lots with status "processing" to "pending"
    updated_rows = (
        db.query(models.Lot)
        .filter(models.Lot.status == "processing")
        .update({"status": "pending"}, synchronize_session=False)
    )

    # Commit the changes
    db.commit()

    return {"message": f"Reset {updated_rows} lots from 'processing' to 'pending'"}