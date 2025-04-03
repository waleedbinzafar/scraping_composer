from fastapi import FastAPI
from app.database import engine
from app import models
from app.routes import websites, auctions, lots, stats

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Scraping Composer is live"}

# Include routers
app.include_router(websites.router, prefix="/websites", tags=["websites"])
app.include_router(auctions.router, prefix="/auctions", tags=["auctions"])
app.include_router(lots.router, prefix="/lots", tags=["lots"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])