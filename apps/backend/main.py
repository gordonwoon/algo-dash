from fastapi import FastAPI
from backend.routes import routes

app = FastAPI()

app.include_router(routes.router)
