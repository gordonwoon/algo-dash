import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.models import StockData


async def fetch_and_store_stock_data(session: AsyncSession, ticker: str):
    # Simplify the process of getting the latest record date and determining date ranges
    latest_record_date = await get_latest_record_date(session, ticker)
    start_date = latest_record_date + \
        timedelta(days=1) if latest_record_date else datetime.now() - \
        timedelta(days=365)
    end_date = datetime.now()

    # Fetch stock data
    df = yf.download(ticker, start=start_date.strftime(
        "%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"))
    if df.empty:
        return []

    # Store new data in the database
    records = []
    for date, row in df.iterrows():
        new_record = StockData(
            ticker=ticker.upper(),
            date=date.date(),
            open=row['Open'],
            high=row['High'],
            low=row['Low'],
            close=row['Close'],
            volume=int(row['Volume'])
        )
        records.append(new_record)
    session.add_all(records)
    await session.commit()

    # Return all data for the ticker
    return await get_all_stock_data(session, ticker)


async def get_latest_record_date(session: AsyncSession, ticker: str) -> datetime:
    query = select(StockData.date).where(StockData.ticker ==
                                         ticker.upper()).order_by(StockData.date.desc()).limit(1)
    result = await session.execute(query)
    latest_record = result.scalars().first()
    return latest_record if latest_record else datetime.now() - timedelta(days=365)


async def get_all_stock_data(session: AsyncSession, ticker: str):
    result = await session.execute(select(StockData).where(StockData.ticker == ticker.upper()))
    return result.scalars().all()
