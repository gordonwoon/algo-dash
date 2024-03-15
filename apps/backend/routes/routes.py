from fastapi import APIRouter
from backend.schemas import schemas

router = APIRouter()


@router.post("/add_stock_data/", response_model=schemas.StockData)
def add_stock_data(stock_data: schemas.StockData):
    # Implement CRUD operation to add stock data
    return stock_data


@router.get("/get_stock_data/")
def get_stock_data():
    # Implement CRUD operation to get stock data
    return {"data": "stock data"}
