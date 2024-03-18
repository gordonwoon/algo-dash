from sqlalchemy.ext.asyncio import AsyncSession

from .database import SessionLocal


# Dependency to get database session
async def get_session() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
