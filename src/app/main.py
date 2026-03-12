from sqlalchemy import text
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .core.database import get_db, engine
from .core.config import settings
from .models import Base
from .routers import users, groups, expenses

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Splitter API",
    description="A Splitwise-style expense splitting application",
    version="1.0.0"
)

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)

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



@app.get("/config")
async def get_config():
    return {
        "database_url": settings.database_url,
        "environment": "development"
    }
