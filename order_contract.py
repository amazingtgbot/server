from web3 import Web3
from db_model.order import Order
import time


class OrderContract:

    def __init__(self, blockchain, address, abi, rpc, account = '', key = ''):
        self.chainId = blockchain
        self.address = address
        self.abi = abi
        self.w3 = Web3(Web3.HTTPProvider(rpc))
        self.contract = self.setup_contract()
        self.account = account
        self.key = key 

    def setup_contract(self):
        contract = self.w3.eth.contract(address=self.address, abi=self.abi)
        return contract

    def get_block_number(self):
        return self.w3.eth.block_number

    def get_max_order_id(self):
        return self.contract.functions.currentOrderId().call()

    def get_order_info(self, order_id:int) -> Order:
        contract_order = self.contract.functions.orders(order_id).call()
        if contract_order is None:
            return None
        
        
        now = int(time.time())
        return Order (
            order_id = order_id,
            amount_in = contract_order[0],
            amount_out_limit = contract_order[1],
            status = 0,
            order_end_at = contract_order[2],
            created_at = now,
            updated_at = now
        )
        
    def get_timestamp(self):
        return self.contract.functions.timestamp().call()

    #获取订单是否可以执行
    def get_order_quote(self, order :Order) -> bool:
        return self.contract.functions.getOrderState(order.order_id).call()
        
        '''
        if len(ret) == 0 :
            return False
        else:
            return True
        str = HexBytes(ret).hex()
        if str == '0x':
            return False
        else:
            return True
        '''
    
    def transaction(self, order: Order,function_name: str) -> bool:
        tx = self.contract.functions[function_name](order.order_id)
        transaction = {
                'from': self.account,
                'gas': 180000,
                'nonce': self.w3.eth.get_transaction_count(self.account),
                'maxFeePerGas': 100000000000,
                'maxPriorityFeePerGas': 1500000000,
            }
        txn = tx.build_transaction(transaction)
        print(txn)
        signd_transaction = self.w3.eth.account.sign_transaction(
            txn,
            private_key= self.key)
        try:
            ret = self.w3.eth.send_raw_transaction(signd_transaction.rawTransaction)
            txn_receipt = self.w3.eth.wait_for_transaction_receipt(ret)
            print(txn_receipt)
            return txn_receipt['status'] == 1
        except:
            return False


        


        





