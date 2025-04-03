from sqlalchemy.orm import Session
from app import models, schemas

# Website CRUD
def create_website(db: Session, website: schemas.WebsiteCreate):
    db_website = models.Website(
        name=website.name,
        link=str(website.link)  # Convert HttpUrl to string
    )
    db.add(db_website)
    db.commit()
    db.refresh(db_website)
    return db_website

def get_website_by_name(db: Session, name: str):
    return db.query(models.Website).filter(models.Website.name == name).first()

# Auction CRUD
def create_auction(db: Session, auction: schemas.AuctionCreate):
    website = get_website_by_name(db, auction.website_name)
    if not website:
        raise ValueError("Website not found")

    db_auction = models.Auction(
        auction_link=str(auction.auction_link),  # Convert HttpUrl to string
        auction_title=auction.auction_title,
        n_lots=auction.n_lots,
        last_scraped=auction.last_scraped,
        website_id=website.id
    )
    db.add(db_auction)
    db.commit()
    db.refresh(db_auction)
    return db_auction

def get_auction_by_id(db: Session, auction_id: int):
    return db.query(models.Auction).filter(models.Auction.id == auction_id).first()

def get_auction_by_link(db: Session, auction_link: str):
    return db.query(models.Auction).filter(models.Auction.auction_link == auction_link).first()

def get_lot_by_link(db: Session, lot_link: str):
    return db.query(models.Lot).filter(models.Lot.lot_link == lot_link).first()

# Lot CRUD
def create_lot(db: Session, lot: schemas.LotCreate):
    db_lot = models.Lot(
        auction_id=lot.auction_id,
        lot_link=str(lot.lot_link),
        lot_title=lot.lot_title,
        lot_number=lot.lot_number,
    )
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot