from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from .database import Base, engine  # Adjust import path as needed
from .routes import routes

app = FastAPI()


# Ensure your database tables are created
# Note: It's often better to manage database migrations with tools like Alembic
@app.on_event("startup")
async def startup_event():
    # Example: Create database tables if not exist (consider using Alembic for migrations)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown_event():
    # If you've established a resource that needs to be closed, close it here
    await engine.dispose()  # Example: Dispose of the connection pool


app.include_router(routes.router)
