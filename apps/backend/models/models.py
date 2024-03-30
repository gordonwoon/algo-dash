from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.schema import UniqueConstraint

from ..database import Base


class StockData(Base):
    __tablename__ = 'stockdata'
    id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    timeframe = Column(String)  # Include if you need different timeframes
    time = Column(DateTime, nullable=False)  # Adjusted to use DateTime
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    __table_args__ = (UniqueConstraint('ticker', 'time',
                      'timeframe', name='_ticker_time_timeframe_uc'),)
