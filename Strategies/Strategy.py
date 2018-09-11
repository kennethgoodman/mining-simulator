from Blockchain import Block# import Block
from Blockchain.Transaction import Transaction
from typing import List


class Strategy:
    def __init__(self):
        pass

    def block_to_extend(self, current_time: int, current_chain, published_chain, mempool, miner) -> Block:
        raise NotImplementedError("Need To Implement")

    def transactions_to_include(self, current_chain, published_chain, mempool) -> List[Transaction]:
        raise NotImplementedError("Need To Implement")

    def blocks_to_publish(self, current_chain, published_chain, mempool):
        raise NotImplementedError("Need To Implement")
