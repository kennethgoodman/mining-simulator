from Blockchain.Block import Block
from Blockchain.Blockchain import Blockchain
from typing import List
from Strategies.Strategy import Strategy
from Blockchain.Mempool import Mempool
import random


class PettyCompliant(Strategy):
    def block_to_extend(self, current_time: int, current_chain: Blockchain,
                        published_chain: Blockchain, mempool: Mempool, miner) -> Block:
        transactions = self.transactions_to_include(current_chain, published_chain, mempool)
        if len(published_chain) <= len(current_chain):
            chain_to_build_on = current_chain
        else:
            chain_to_build_on = published_chain

        blocks = Block.create_next_blocks(transactions, chain_to_build_on, current_time, miner)
        if blocks[0].block_num == 0:
            raise ValueError("")
        for block in blocks:
            if block.miner == miner:
                return block

        amount_of_fees = float('inf')
        block_to_pick = None
        for block in blocks:
            value_of_all_transactions = block.value_of_all_transactions
            if value_of_all_transactions < amount_of_fees:
                amount_of_fees = value_of_all_transactions
                block_to_pick = block
        return block_to_pick  # if more than one option, pick the one with the fewest transaction fees

    def transactions_to_include(self, current_chain: Blockchain, published_chain: Blockchain, mempool: Mempool):
        return mempool.get_top_1mb_transactions()

    def blocks_to_publish(self, current_chain: Blockchain, published_chain: Blockchain, mempool: Mempool) \
            -> List[Block]:
        blocks = []
        for edge in current_chain.edges:
            for block in current_chain.iterate_backwards(edge):
                if block in published_chain:
                    break
                blocks.append(block)
        return blocks
