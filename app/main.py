from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from . import crud, data_loader

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "Stock Dashboard API Running"}

@app.post("/load/{symbol}")
def load_data(symbol: str, db: Session = Depends(get_db)):
    data_loader.fetch_and_store(symbol, db)
    return {"message": f"{symbol} data loaded"}

@app.get("/companies")
def companies(db: Session = Depends(get_db)):
    return crud.get_companies(db)

@app.get("/data/{symbol}")
def stock_data(symbol: str, db: Session = Depends(get_db)):
    return crud.get_last_30_days(db, symbol)

@app.get("/summary/{symbol}")
def summary(symbol: str, db: Session = Depends(get_db)):
    return crud.get_summary(db, symbol)

@app.get("/compare")
def compare(symbol1: str, symbol2: str, db: Session = Depends(get_db)):
    return crud.compare_stocks(db, symbol1, symbol2)
