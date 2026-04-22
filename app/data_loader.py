import yfinance as yf
from sqlalchemy.orm import Session
from .models import Stock

def fetch_and_store(symbol: str, db: Session):

    
    db.query(Stock).filter(Stock.symbol == symbol).delete()
    db.commit()

   
    data = yf.download(symbol, period="1y")

    if data.empty:
        print("No data fetched!")
        return

    data.reset_index(inplace=True)

    data.fillna(0, inplace=True)

    data["daily_return"] = (data["Close"] - data["Open"]) / data["Open"]
    data["moving_avg_7"] = data["Close"].rolling(window=7).mean().fillna(0)

    
    for _, row in data.iterrows():
        stock = Stock(
            symbol=symbol,
            date=row["Date"],
            open=float(row["Open"]),
            close=float(row["Close"]),
            high=float(row["High"]),
            low=float(row["Low"]),
            volume=float(row["Volume"]),
            daily_return=float(row["daily_return"]),
            moving_avg_7=float(row["moving_avg_7"]),
        )
        db.add(stock)

    db.commit()
    print("Data stored successfully!")