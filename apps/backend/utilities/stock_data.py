import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.models import StockData


async def fetch_and_store_stock_data(session: AsyncSession, ticker: str):
    latest_record_date = await get_latest_record_date(session, ticker)
    start_date = latest_record_date + \
        timedelta(days=1) if latest_record_date else datetime.now() - \
        timedelta(days=365)
    end_date = datetime.now()

    # Fetch stock data
    df = yf.download(ticker, start=start_date.strftime(
        "%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), ignore_tz=True)
    if df.empty:
        return []

    # Prepare data to be stored, excluding the last row
    records_to_store = []
    for i, (index, row) in enumerate(df.iterrows()):
        if i < len(df) - 1:  # Check if it's not the last row
            new_record = StockData(
                ticker=ticker.upper(),
                date=index.date(),
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=int(row['Volume'])
            )
            records_to_store.append(new_record)

    # Store filtered data in the database
    if records_to_store:
        session.add_all(records_to_store)
        await session.commit()

    # Fetch all existing stock data for the ticker from the database
    existing_data = await get_all_stock_data(session, ticker)

    # Convert existing data to the desired format
    existing_data_formatted = [
        {
            "date": data.date,
            "open": data.open,
            "high": data.high,
            "low": data.low,
            "close": data.close,
            "volume": data.volume
        } for data in existing_data
    ]

    # Append the last row of the newly fetched data if it exists
    if not df.empty:
        last_row = df.iloc[-1]
        last_row_formatted = {
            "date": df.index[-1].date(),
            "open": last_row['Open'],
            "high": last_row['High'],
            "low": last_row['Low'],
            "close": last_row['Close'],
            "volume": int(last_row['Volume'])
        }
        existing_data_formatted.append(last_row_formatted)

    # Return combined data
    return existing_data_formatted


async def get_latest_record_date(session: AsyncSession, ticker: str) -> datetime:
    query = select(StockData.date).where(StockData.ticker ==
                                         ticker.upper()).order_by(StockData.date.desc()).limit(1)
    result = await session.execute(query)
    latest_record = result.scalars().first()
    return latest_record if latest_record else datetime.now() - timedelta(days=365)


async def get_all_stock_data(session: AsyncSession, ticker: str):
    result = await session.execute(select(StockData).where(StockData.ticker == ticker.upper()))
    return result.scalars().all()
