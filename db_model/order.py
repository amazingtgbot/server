from __future__ import annotations
from sqlalchemy import String, select, func ,BigInteger, Integer,update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from typing import Sequence

from .base import Base


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(
        "id", autoincrement=True, nullable=False, unique=True, primary_key=True
    )
    order_id: Mapped[int] = mapped_column("orderId", Integer, nullable=False)
    amount_in: Mapped[str] = mapped_column("amountIn", String(length=128), nullable=False, default="")
    amount_out_limit: Mapped[str] = mapped_column("amountOutLimit", String(length=128), nullable=False, default="")
    status: Mapped[int] = mapped_column("status", nullable=False)
    order_end_at: Mapped[int] = mapped_column("orderEndAt", BigInteger, default="")
    created_at: Mapped[int] = mapped_column("createdAt", BigInteger, default="")
    updated_at: Mapped[int] = mapped_column("updatedAt", BigInteger, default="")


    @classmethod
    async def save(
        cls, session: AsyncSession, order: Order
    ) -> Order:
        session.add(order)
        await session.flush()
        # To fetch notebook
        new = await cls.get_by_order_id(session, Order.order_id)
        # print(new)
        if not new:
            raise RuntimeError()
        return new

    @classmethod
    async def get_by_order_id(cls, session: AsyncSession, order_id: int) -> Order | None:
        stmt = select(cls).where(cls.order_id == order_id)
        return await session.scalar(stmt)

    @classmethod
    async def update(
        self, session: AsyncSession
    ) -> None:
        # self.pair_create_time = create_time
        await session.flush()
        #await session.refresh(self)


    @classmethod
    async def get_valid_list(cls, session: AsyncSession, now : String) -> Sequence[Order]:
        stmt = select(cls).where(cls.status == 0, cls.order_end_at >= now)
        ret = await session.scalars(stmt)
        return ret.fetchall()
        
    @classmethod
    async def get_max_order_id(cls, session: AsyncSession):
        stmt = select(func.max(cls.order_id))
        return await session.scalar(stmt)
