from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database.database import get_db
from app.models.models import Race, Driver, Circuit

app = FastAPI(title="F1 Predictor API")

@app.get("/")
def root():
    return {"message": "F1 Predictor API", "status": "running"}

@app.get("/health/db")
def health_check_db(db: Session = Depends(get_db)):
    """Check database connection"""
    try:
        # Try to query races
        race_count = db.query(Race).count()
        driver_count = db.query(Driver).count()
        circuit_count = db.query(Circuit).count()
        
        return {
            "status": "healthy",
            "database": "connected",
            "tables": {
                "races": race_count,
                "drivers": driver_count,
                "circuits": circuit_count
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "error",
            "error": str(e)
        }

@app.get("/races")
def get_races(limit: int = 10, db: Session = Depends(get_db)):
    """Get recent races"""
    races = db.query(Race).order_by(Race.date.desc()).limit(limit).all()
    return races

@app.get("/drivers")
def get_drivers(limit: int = 10, db: Session = Depends(get_db)):
    """Get drivers"""
    drivers = db.query(Driver).limit(limit).all()
    return drivers

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)