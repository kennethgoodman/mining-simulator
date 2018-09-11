from Blockchain.Block import Block
from Blockchain.Blockchain import Blockchain
from typing import List
from Strategies.Strategy import Strategy
from Strategies.Base.Miner import Miner
from Blockchain.Mempool import Mempool


class DefaultStrategy(Strategy):
    def block_to_extend(self, current_time: int, current_chain: Blockchain,
                        published_chain: Blockchain, mempool: Mempool, miner: Miner) -> Block:
        total_value_left = miner.mempool.get_value_of_transactions()
        if any(b.miner == miner for b in current_chain.last_block):
            transactions = self.transactions_to_include(None, None, mempool)
            for b in current_chain.last_block:
                if b.miner == miner:
                    return Block.create_next_block(transactions, b, current_time, miner)
        elif any(b.value_of_all_transactions < total_value_left for b in current_chain.last_block):
            # mine on the block that has value less than transaction
            transactions = self.transactions_to_include(None, None, mempool)
            min_block_amount = float('inf')
            min_block = None
            for b in current_chain.last_block:
                if b.value_of_all_transactions < min_block_amount:
                    min_block_amount = b.value_of_all_transactions
                    min_block = b
            return Block.create_next_block(transactions, min_block, current_time, miner)
        else:
            # fork the chain, what to do if the fork is two deep? currently ignore
            # TODO: don't ignore two deep forks
            transactions = mempool.get_transaction_list().copy()
            block_transactions = current_chain.last_block[0].previous_block.transactions
            for tx in block_transactions:
                transactions.add(tx)
            transactions = self.transactions_to_include(None, None, transactions)
            block = current_chain.last_block[0].previous_block
            return Block.create_next_block(transactions, block, current_time, miner)

    def transactions_to_include(self, current_chain: Blockchain, published_chain: Blockchain, transactions):
        total_value = sum(tx.tx_fee for tx in transactions)
        target_value = total_value // 2 - 1
        transactions_to_include = []
        current_value = 0
        for tx in transactions:
            if current_value + tx.tx_fee >= target_value:
                break
            transactions_to_include.append(tx)
            current_value += tx.tx_fee
        return transactions

    def blocks_to_publish(self, current_chain: Blockchain, published_chain: Blockchain, mempool: Mempool) \
            -> List[Block]:
        blocks = []
        for edge in current_chain.edges:
            for block in current_chain.iterate_backwards(edge):
                if block in published_chain:
                    break
                blocks.append(block)
        return blocks
