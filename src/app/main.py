from sqlalchemy import text
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .core.database import get_db, engine
from .core.config import settings
from .models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Splitter API",
    description="A Splitwise-style expense splitting application",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {"message": "Splitter API is running", "database": "Connected"}


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Test database connection
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/config")
async def get_config():
    return {
        "database_url": settings.database_url,
        "environment": "development"
    }


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
