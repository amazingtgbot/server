from typing import Annotated, AsyncIterator
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from db_model.base import Base
from tool.logger.logger import logger


# mysql+pymysql

#SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://root:qwer1234@localhost:3306/web3"
SQLALCHEMY_DATABASE_URL = "mysql+aiomysql://test:password@localhost:3306/web3"
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autoflush=False,
    future=True,
)

async def create_db_and_tables():

    async with async_engine.begin() as conn:

        # await conn.run_sync(Base.metadata.drop_all)           # delete all table at first
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        logger.info(e)


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
