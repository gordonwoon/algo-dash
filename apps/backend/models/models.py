from ..database import Base
from sqlalchemy import Column, DateTime, Float, Integer, String, UniqueConstraint


class StockData(Base):
    __tablename__ = "stockdata"

    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True)
    timeframe = Column(String)
    date = Column(DateTime)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    __table_args__ = (UniqueConstraint('ticker', 'date',
                      'timeframe', name='_ticker_date_timeframe_uc'),)
