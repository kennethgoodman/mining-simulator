from Blockchain import Block
from Blockchain import Blockchain
from typing import List
from Strategies import Strategy
from Blockchain import Mempool
import random


class DefaultStrategy(Strategy):
    def block_to_extend(self, current_time: int, current_chain: Blockchain,
                        published_chain: Blockchain, mempool: Mempool, miner) -> Block:
        transactions = self.transactions_to_include(current_chain, published_chain, mempool)
        blocks = Block.Block.create_next_blocks(transactions, published_chain, current_time, miner)
        for block in blocks:
            if block.miner == miner:
                return block  # pick your own block to mine on top of
        return random.choice(blocks)  # if more than one option, pick a random one

    def transactions_to_include(self, current_chain: Blockchain, published_chain: Blockchain, mempool: Mempool):
        return mempool.get_top_1mb_transactions()

    def blocks_to_publish(self, current_chain: Blockchain, published_chain: Blockchain, mempool: Mempool):
        blocks = []
        for edge in current_chain.edges:
            for block in current_chain.iterate_backwards(edge):
                if block in published_chain:
                    break
                blocks.append(block)
        return blocks
