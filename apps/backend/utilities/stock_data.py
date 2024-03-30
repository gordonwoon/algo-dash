from datetime import datetime, timedelta

import pytz
import yfinance as yf
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ..models.models import StockData


async def fetch_and_store_stock_data(session: AsyncSession, ticker: str):
    utc_zone = pytz.utc
    latest_record_time = await get_latest_record_time(session, ticker)
    # Ensure start_date is in UTC if it comes from the database already in UTC
    start_date = latest_record_time + \
        timedelta(days=1) if latest_record_time else datetime.now(
            tz=utc_zone) - timedelta(days=365)
    end_date = datetime.now(tz=utc_zone)  # Ensure end_date is in UTC

    # Fetch stock data
    df = yf.download(ticker, start=start_date.strftime(
        "%Y-%m-%d"), end=end_date.strftime("%Y-%m-%d"), ignore_tz=True)
    if df.empty:
        return []

    records_to_store = []
    for i, (index, row) in enumerate(df.iterrows()):
        if i < len(df) - 1:  # Check if it's not the last row
            # Convert the index to UTC datetime if not already
            utc_datetime = index.tz_localize(
                'UTC') if index.tzinfo is None else index.tz_convert('UTC')
            new_record = StockData(
                ticker=ticker.upper(),
                time=utc_datetime.to_pydatetime(),  # Ensure this is a datetime object in UTC
                open=row['Open'],
                high=row['High'],
                low=row['Low'],
                close=row['Close'],
                volume=int(row['Volume'])
            )
            records_to_store.append(new_record)

    if records_to_store:
        session.add_all(records_to_store)
        await session.commit()

    # Fetch and prepare the existing data similar to before, ensuring times are returned in UTC
    existing_data = await get_all_stock_data(session, ticker)

    # Convert existing data to the desired format
    existing_data_formatted = [
        {
            # Formatting datetime to 'yyyy-mm-dd'
            "time": data.time.strftime("%Y-%m-%d"),
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
            # Adjusted for 'yyyy-mm-dd'
            "time": df.index[-1].strftime("%Y-%m-%d"),
            "open": last_row['Open'],
            "high": last_row['High'],
            "low": last_row['Low'],
            "close": last_row['Close'],
            "volume": int(last_row['Volume'])
        }
        existing_data_formatted.append(last_row_formatted)

    return existing_data_formatted


async def get_latest_record_time(session: AsyncSession, ticker: str) -> datetime:
    # Adjusted to query based on the `time` field
    query = select(StockData.time).where(StockData.ticker ==
                                         ticker.upper()).order_by(StockData.time.desc()).limit(1)
    result = await session.execute(query)
    latest_record = result.scalars().first()
    return latest_record if latest_record else datetime.now() - timedelta(days=365)


async def get_all_stock_data(session: AsyncSession, ticker: str):
    result = await session.execute(select(StockData).where(StockData.ticker == ticker.upper()).order_by(StockData.time.asc()))
    return result.scalars().all()
