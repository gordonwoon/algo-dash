from datetime import datetime, timedelta

import yfinance as yf
from backend.models.models import StockData
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def fetch_and_store_stock_data(session: AsyncSession, ticker: str):
    async with session.begin():
        # Check the latest date of data for the given ticker
        result = await session.execute(
            select(StockData).filter(StockData.ticker == ticker.upper()
                                     ).order_by(StockData.date.desc()).limit(1)
        )
        latest_record = result.scalars().first()

        if latest_record:
            start_date = latest_record.date + timedelta(days=1)
        else:
            start_date = datetime.now() - timedelta(days=365)
        end_date = datetime.now()

        # Fetch stock data from yfinance
        df = yf.download(ticker, start=start_date.strftime(
            "%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))

        # Store new data in the database
        for date, row in df.iterrows():
            new_stock_data = StockData(
                ticker=ticker.upper(),
                date=date.date(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=int(row['Volume'])
            )
            session.add(new_stock_data)

        await session.commit()

        # Fetch and return all data for the ticker as an example
        result = await session.execute(select(StockData).filter(StockData.ticker == ticker.upper()))
        all_data = result.scalars().all()
        return all_data
