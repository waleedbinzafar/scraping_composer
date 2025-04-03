from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from datetime import datetime, timedelta
from app.database import get_db
from app import models

router = APIRouter()

@router.get("/total-lots")
def total_lots(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Lot.id)).scalar()
    return {"total_lots": count}

@router.get("/total-auctions")
def total_auctions(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Auction.id)).scalar()
    return {"total_auctions": count}

@router.get("/total-lots-pending")
def total_lots_pending(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "pending").scalar()
    return {"total_lots_pending": count}

@router.get("/total-lots-processing")
def total_lots_processing(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "processing").scalar()
    return {"total_lots_processing": count}

@router.get("/total-lots-scraped")
def total_lots_scraped(db: Session = Depends(get_db)):
    count = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "scraped").scalar()
    return {"total_lots_scraped": count}

@router.get("/total-lots-scraped-in-10-minutes")
def total_lots_scraped_in_10_minutes(db: Session = Depends(get_db)):
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    count = db.query(func.count(models.Lot.id)).filter(
        models.Lot.status == "scraped",
        models.Lot.scraped_at >= ten_minutes_ago
    ).scalar()
    return {"total_lots_scraped_in_10_minutes": count}

@router.get("/throughput-10-minutes")
def throughput_10_minutes(db: Session = Depends(get_db)):
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    count = db.query(func.count(models.Lot.id)).filter(
        models.Lot.status == "scraped",
        models.Lot.scraped_at >= ten_minutes_ago
    ).scalar()
    throughput = count / 10
    return {"throughput_10_minutes": throughput}


@router.get("/summary-stats")
def summary_stats(db: Session = Depends(get_db)):
    total_lots = db.query(func.count(models.Lot.id)).scalar()
    total_auctions = db.query(func.count(models.Auction.id)).scalar()
    total_lots_pending = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "pending").scalar()
    total_lots_processing = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "processing").scalar()
    total_lots_scraped = db.query(func.count(models.Lot.id)).filter(models.Lot.status == "scraped").scalar()
    ten_minutes_ago = datetime.now() - timedelta(minutes=10)
    total_lots_scraped_in_10_minutes = db.query(func.count(models.Lot.id)).filter(
        models.Lot.status == "scraped",
        models.Lot.scraped_at >= ten_minutes_ago
    ).scalar()
    throughput_10_minutes = total_lots_scraped_in_10_minutes / 10

    return {
        "total_lots": total_lots,
        "total_auctions": total_auctions,
        "total_lots_pending": total_lots_pending,
        "total_lots_processing": total_lots_processing,
        "total_lots_scraped": total_lots_scraped,
        "total_lots_scraped_in_10_minutes": total_lots_scraped_in_10_minutes,
        "throughput_10_minutes": throughput_10_minutes
    }