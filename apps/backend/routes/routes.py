from ..dependencies import get_session
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..utilities import stock_data  # Ensure this points to your module
from fastapi.encoders import jsonable_encoder

router = APIRouter()


@router.get("/stock/{ticker}")
async def get_stock_data(ticker: str, session: AsyncSession = Depends(get_session)):
    try:
        data = await stock_data.fetch_and_store_stock_data(session, ticker)
        formatted_data = [jsonable_encoder(stock) for stock in data]

        # Format or serialize 'data' as needed before returning
        # Example formatting
        return {"data": [dict(row) for row in formatted_data]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
