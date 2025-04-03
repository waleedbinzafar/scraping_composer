import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./scraping_composer.db"

# Define a custom REGEXP function for SQLite
def regexp(expr, item):
    reg = re.compile(expr)
    return reg.search(item) is not None

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
# Add the REGEXP function to SQLite
engine.raw_connection().create_function("REGEXP", 2, regexp)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()