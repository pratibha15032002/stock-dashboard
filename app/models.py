from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String)
    date = Column(Date)
    open = Column(Float)
    close = Column(Float)
    high = Column(Float)
    low = Column(Float)
    volume = Column(Float)
    daily_return = Column(Float)
    moving_avg_7 = Column(Float)
