from datetime import datetime

from pydantic import BaseModel


class StockData(BaseModel):
    ticker: str
    timeframe: str
    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int

    class Config:
        orm_mode = True
