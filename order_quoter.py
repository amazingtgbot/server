import time
from db import AsyncSessionLocal
from db_model.order import Order
from .order_contract import OrderContract
from .quoter_config import qc

async def quoter():
    async_session = AsyncSessionLocal
    #初始化合约
    contract = OrderContract(qc.blockchain,qc.address,qc.abi,qc.rpc,qc.account,qc.key)

    while True:
        async with async_session.begin() as session:
            order_list = await Order.get_valid_list(session,contract.get_timestamp())
            for order in order_list:
                function_name = contract.get_order_quote(order)
                if function_name == 'cancel':
                    #更新订单为已取消
                    order_update = await Order.get_by_order_id(session,order.order_id)
                    if order_update is not None:
                        order_update.status = 2
                        order_update.updated_at = int(time.time())
                        await order_update.update(session)
                        print('order is cencel:'+ str(order.order_id))
                elif len(function_name) != 0:
                    if contract.transaction(order, function_name):
                        #更新订单为已交易
                        order_update = await Order.get_by_order_id(session,order.order_id)
                        if order_update is not None:
                            order_update.status = 1
                            order_update.updated_at = int(time.time())
                            await order_update.update(session)
                        print('order is finished:'+ str(order.order_id))
                
        print("sleep!")
        time.sleep(5)