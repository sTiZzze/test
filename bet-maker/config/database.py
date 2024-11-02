from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from config.config import settings

engine = create_async_engine(
    settings.db.SQLALCHEMY_DATABASE_URL
)

SessionLocal = async_sessionmaker(
    autocommit=False, autoflush=True, bind=engine)


class Base(DeclarativeBase):
    pass


@asynccontextmanager
async def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        await db.rollback()
    else:
        await db.commit()
    finally:
        await db.close()