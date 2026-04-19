import yfinance as yf
import pandas as pd
from sqlalchemy.orm import Session
from .models import Stock

def fetch_and_store(symbol: str, db: Session):
    data = yf.download(symbol, period="1y")

    data.reset_index(inplace=True)

    # ✅ Clean data (IMPORTANT FIX)
    data.fillna(0, inplace=True)

    data["daily_return"] = (data["Close"] - data["Open"]) / data["Open"]
    data["moving_avg_7"] = data["Close"].rolling(window=7).mean().fillna(0)

    for _, row in data.iterrows():
        try:
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
        except:
            continue  # skip bad rows

    db.commit()
