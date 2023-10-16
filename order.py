from .order_repository import repository
from .order_quoter import quoter
import asyncio


def order():
    loop = asyncio.get_event_loop()
    loop.create_task(repository())
    loop.create_task(quoter())

    pass