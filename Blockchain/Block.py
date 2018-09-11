from typing import List
from Blockchain.Transaction import Transaction
from Blockchain import Blockchain
from Utils.hashlib_util import sha
from Strategies.Base.Miner import Miner


class Block:
    def __init__(self, transactions: List[Transaction], block_time: int, previous_block, block_num, miner: Miner):
        self.transactions = transactions
        self.block_time = block_time
        self.previous_block = previous_block
        self.block_num = block_num
        self.sum_of_hash_of_transactions = sum(map(hash, self.transactions))
        self.block_hash = sha(str(self.sum_of_hash_of_transactions) +
                              str(self.block_time) +
                              str(self.previous_block.block_hash if self.previous_block else None) +
                              str(self.block_num))
        self.miner = miner
        try:
            if self.previous_block is None:
                return
            assert self.block_num == self.previous_block.block_num + 1
        except AssertionError as e:
            raise e
        self.value_of_all_transactions = sum(tx.tx_fee for tx in self.transactions)

    # @property
    # def value_of_all_transactions(self):
    #     return sum(tx.tx_fee for tx in self.transactions)

    def __hash__(self):
        return self.block_hash

    @staticmethod
    def create_genesis_block():
        return Block([], 0, None, 0, None)

    @staticmethod
    def create_next_blocks(transactions, blockchain: Blockchain, current_time: int, miner):
        block_time = current_time
        previous_blocks = blockchain.last_block
        block_num = len(blockchain) + 1
        return [Block(transactions, block_time, previous_block, block_num, miner)
                 for previous_block in previous_blocks]

    @staticmethod
    def create_next_block(transactions, prev_block, current_time: int, miner):
        return Block(transactions, current_time, prev_block, prev_block.block_num + 1, miner)

    def __eq__(self, other):
        if other is None:
            return False

        if self.block_num == 0 and other.block_num == 0:
            return self.transactions == [] and other.transactions == [] and \
                   self.block_time == 0 and other.block_time == 0 and \
                   self.previous_block is None and \
                   other.previous_block is None

        return self.block_hash == other.block_hash and \
               self.previous_block.block_hash == other.previous_block.block_hash and \
               self.miner.number == other.miner.number

    def copy(self, prev_block_reference):
        transactions = [tx.copy() for tx in self.transactions]
        return Block(transactions, self.block_time, prev_block_reference, self.block_num, self.miner)