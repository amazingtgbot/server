
import time
from db import AsyncSession,AsyncSessionLocal
from db_model.order import Order
from .order_contract import OrderContract
from .quoter_config import qc

async def repository():
    async_session = AsyncSessionLocal

    #初始化合约
    contract = OrderContract(qc.blockchain, qc.address,qc.abi,qc.rpc)

    while True:
        async with async_session.begin() as session:
            max_order_id = await Order.get_max_order_id(session)
            print(max_order_id)
            #比对数据库中的限价单
            if max_order_id is None:
                max_order_id = 0

            #获取合约当前现价单下一个可用的ID
            contract_max_order_id = contract.get_max_order_id()
            print(contract_max_order_id)

            if contract_max_order_id-1 > max_order_id:
                #有新的限价单，插入数据库
                for id in range(max_order_id+1, contract_max_order_id):
                    contract_order = contract.get_order_info(id)
                    if contract_order is None:
                        continue
                    await Order.save(session, contract_order)

        print("sleep!")
        time.sleep(5)

    
async def get_max_order(async_session: AsyncSession):
    async with async_session.begin() as session:
        return await Order.get_max_order_id(session)

