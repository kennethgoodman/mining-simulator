from Strategies import Strategy
from Blockchain import Blockchain
from Blockchain.Mempool import Mempool
from Utils.random_util import found_block


class Miner:
    def __init__(self, strategy: Strategy, hashpower: int, peers, total_hashpower: int, number: int,
                 my_defaultblockchain: Blockchain, published_defaultblockchain: Blockchain):
        self.strategy = strategy
        self.my_chain = my_defaultblockchain  # my current view of the blockchain
        self.published_chain = published_defaultblockchain  # their current view of the blockchain
        # TODO: add published chain for each peer
        # TODO: There may be strategies to publish the chain to x% of your peers to be even more selfish
        self.mempool = Mempool()   # my current view of the mempool
        self.hashpower = hashpower
        self.hashpower_proportion = 1.0 * self.hashpower / total_hashpower
        self.number = number
        self.peers = peers
        # TODO: take out hashpower proportion and change to be based on difficulty to allow for
        # TODO: strategies that only use a portion of the hashpower, especially with EDA

    def change_peers(self, peers):
        self.peers = peers

    def add_peer(self, peer):
        self.peers.append(peer)

    def __eq__(self, other):
        return self.number == other.number

    def receive_block(self, block) -> None:
        if block.miner == self:
            return
        elif any(block == b for b in self.published_chain.last_block):
            return
        self.published_chain.extend_with_reference(block)
        self.my_chain.extend_with_reference(block)
        if len(self.published_chain.last_block) == 1:
            for tx in block.transactions:
                try:
                    self.mempool.mempool.remove(tx)
                except ValueError as ve:
                    print(ve)
        # TODO: if a fork is resolved
        # TODO: have to add transactions back
        # if block.block_num == self.my_chain.last_block.block_num:  # two blocks found at the same time
        #     self.published_chain.extend_with_reference(block)
        #     print("found a conflict, two blocks found at the same time")
        # elif block.block_num < self.my_chain.last_block.block_num:
        #     self.published_chain.extend_with_reference(block)
        # elif block.previous_block is not None and self.my_chain.last_block.previous_block is not None and \
        #         block.previous_block.block_hash != self.my_chain.last_block.block_hash:
        #     # re-org
        #     self.mempool = block.miner.mempool.copy()  # overwrite our own mempool
        #     self.published_chain = block.miner.published_chain.copy()
        #     self.my_chain = block.miner.published_chain.copy()
        #     print("conflict resolved")
        #     # TODO: should only
        # else:  # regular publish
        #     for tx in block.transactions:
        #         self.mempool.mempool.remove(tx)
        #     self.published_chain.extend_with_reference(block)
        #     self.my_chain.extend_with_reference(block)
        # TODO: change to a strategy config to allow for waiting multiple blocks before reverting to published chain
        # TODO: Check if found block at the same time

    def found_block(self) -> bool:
        return found_block(self.hashpower_proportion,
                           average_time_for_blocks=self.my_chain.total_expected_time_per_block)

    def run_mining_round(self, current_time):
        if self.found_block():
            working_block = self.strategy.block_to_extend(current_time, self.my_chain, self.published_chain,
                                                          self.mempool, self)
            self.my_chain.extend(working_block)
            for tx in working_block.transactions:
                self.mempool.mempool.remove(tx)

    def run_publish_round(self):
        blocks_to_publish = self.strategy.blocks_to_publish(self.my_chain, self.published_chain, self.mempool)
        for block in blocks_to_publish:
            self.publish(block)

    def publish(self, block):
        self.published_chain.extend(block)
        for peer in self.peers:
            peer.receive_block(block)

    def add_txs_to_mempool(self, txs):
        for tx in txs:
            self.mempool.add(tx)


