from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class Website(Base):
    __tablename__ = "websites"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    link = Column(String, unique=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    last_scraped = Column(DateTime, nullable=True)

    auctions = relationship("Auction", back_populates="website")

class Auction(Base):
    __tablename__ = "auctions"
    id = Column(Integer, primary_key=True, index=True)
    auction_link = Column(String, unique=True)
    auction_title = Column(String)
    n_lots = Column(Integer)
    last_scraped = Column(DateTime, nullable=True)

    website_id = Column(Integer, ForeignKey("websites.id"))
    website = relationship("Website", back_populates="auctions")
    lots = relationship("Lot", back_populates="auction")

class Lot(Base):
    __tablename__ = "lots"
    id = Column(Integer, primary_key=True, index=True)
    auction_id = Column(Integer, ForeignKey("auctions.id"))
    lot_link = Column(String, unique=True)
    lot_title = Column(String)
    lot_number = Column(String, nullable=True)
    price = Column(String, nullable=True)
    image_links = Column(String, nullable=True)  # Will store JSON string
    is_scraped = Column(Boolean, default=False)
    status = Column(String, nullable=True, default="pending")  # Status of the lot
    lot_description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    scraped_at = Column(DateTime, nullable=True)

    auction = relationship("Auction", back_populates="lots")