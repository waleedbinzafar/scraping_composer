from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

# Website schemas
class WebsiteCreate(BaseModel):
    name: str
    link: HttpUrl

class WebsiteOut(BaseModel):
    id: int
    name: str
    link: HttpUrl

    class Config:
        from_attributes = True  # Updated from 'orm_mode'

# Auction schemas
class AuctionCreate(BaseModel):
    website_name: str
    auction_link: HttpUrl
    auction_title: str
    n_lots: int
    last_scraped: Optional[datetime] = None

class AuctionOut(BaseModel):
    id: int
    auction_link: HttpUrl
    auction_title: str
    n_lots: int
    last_scraped: Optional[datetime]

    class Config:
        from_attributes = True  # Updated from 'orm_mode'

# Lot schemas
class LotCreate(BaseModel):
    auction_id: int
    lot_link: HttpUrl
    lot_title: str
    lot_number: Optional[str] = None

class LotOut(BaseModel):
    id: int
    auction_id: int
    lot_link: HttpUrl
    lot_title: str
    lot_number: Optional[str]
    price: Optional[str]
    image_links: Optional[str]
    is_scraped: bool
    status: Optional[str]
    lot_description: Optional[str]
    created_at: datetime
    updated_at: datetime
    scraped_at: Optional[datetime]

    class Config:
        from_attributes = True

class LotScrapedInfo(BaseModel):
    lot_id: int
    price: Optional[str] = None
    image_links: Optional[str] = None