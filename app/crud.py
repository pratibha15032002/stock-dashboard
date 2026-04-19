from sqlalchemy.orm import Session
from .models import Stock

def get_companies(db: Session):
    return db.query(Stock.symbol).distinct().all()

def get_last_30_days(db: Session, symbol: str):
    return db.query(Stock).filter(Stock.symbol == symbol).order_by(Stock.date.desc()).limit(30).all()

def get_summary(db: Session, symbol: str):
    data = db.query(Stock).filter(Stock.symbol == symbol).all()
    closes = [d.close for d in data]

    return {
        "52_week_high": max(closes),
        "52_week_low": min(closes),
        "average_close": sum(closes) / len(closes)
    }

def compare_stocks(db: Session, s1: str, s2: str):
    data1 = get_last_30_days(db, s1)
    data2 = get_last_30_days(db, s2)

    return {
        "stock1": [d.close for d in data1],
        "stock2": [d.close for d in data2]
    }
