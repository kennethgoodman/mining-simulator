from Blockchain import Block
from typing import List
from collections import defaultdict
import random


class Blockchain:
    def __init__(self, num_blocks_per_diffculty_adjustment=2016, total_expected_time_per_block=60 * 10,
                 default_difficulty=1):
        self.num_blocks_per_diffculty_adjustment = num_blocks_per_diffculty_adjustment
        self.total_expected_time_per_block = total_expected_time_per_block
        self.last_difficulty = default_difficulty

        # self.blockchain = []
        self._edges = [Block.Block.create_genesis_block()]
        self.blockchain_idx = defaultdict(list)
        self.blockchain_idx[0] = [self._edges[0]]

    @property
    def edges(self) -> List[Block.Block]:  # For typing IDE support and ease-of-read
        return self._edges  # should order edges by length

    @property
    def last_block(self):
        farthest_edge_num = -1  # really should be one with most work, but the simulation has the same diff for blocks
        farthest_edges = []
        for edge in self.edges:
            if edge.block_num > farthest_edge_num:
                farthest_edge_num = edge.block_num
                farthest_edges = [edge]
            elif edge.block_num == farthest_edge_num:
                farthest_edges.append(edge)
        return farthest_edges

    # @property
    # def difficulty(self) -> int:
    #     if len(self.blockchain) < self.num_blocks_per_diffculty_adjustment:
    #         return self.last_difficulty
    #     if len(self.blockchain) % self.num_blocks_per_diffculty_adjustment == 0:
    #         blocks_to_find_da = self.blockchain[-self.num_blocks_per_diffculty_adjustment:]
    #         first_block_time = blocks_to_find_da[0]
    #         last_block_time = blocks_to_find_da[-1]
    #         total_time = last_block_time - first_block_time
    #         average_block_per_time = total_time / self.num_blocks_per_diffculty_adjustment
    #         difficulty_adjustment = average_block_per_time / self.total_expected_time_per_block
    #         new_difficulty = self.last_difficulty * difficulty_adjustment
    #         self.last_difficulty = new_difficulty
    #         return new_difficulty
    #     else:
    #         return self.last_difficulty
    # def get_last_block_hash(self) -> str:
    #     return self.blockchain[-1].previous_block_hash

    def add_edge(self, block: Block):
        # TODO: should edges be sorted by length?
        self._edges.append(block)

    def edit_change(self, block: Block, edge_idx: int):
        # TODO: should edges be sorted by length?
        self._edges[edge_idx] = block

    def extend(self, block: Block) -> None:
        edge_idx_to_change = None
        for edge_i, edge in enumerate(self.edges):
            if edge == block:  # already have this block
                return  #
            elif edge == block.previous_block:
                edge_idx_to_change = edge_i
                break
        if edge_idx_to_change is None:
            self.add_edge(block)
        else:
            self.edit_change(block, edge_idx_to_change)
        self.blockchain_idx[block.block_num].append(block)

    def extend_with_reference(self, block: Block) -> None:
        def iteratore_backwards_block(block_to_iterate):
            while block_to_iterate is not None:
                yield block_to_iterate
                block_to_iterate = block_to_iterate.previous_block

        for edge in self.edges:
            for b in iteratore_backwards_block(edge):
                if b == block.previous_block:
                    block = block.copy(b)
                    return self.extend(block)
                elif b.block_num < block.previous_block.block_num:
                    break

        raise ValueError("There must be some error here")

    @staticmethod
    def iterate_backwards(edge):
        while edge is not None:
            yield edge
            edge = edge.previous_block

    def __len__(self):
        return self.last_block[0].block_num

    def __contains__(self, block: Block):
        assert isinstance(block, Block.Block)
        return any(block == b for b in self.blockchain_idx.get(block.block_num, []))

    def __iter__(self):
        for edge in self.edges:
            yield edge

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        new_blockchain = Blockchain(num_blocks_per_diffculty_adjustment=self.num_blocks_per_diffculty_adjustment,
                           total_expected_time_per_block=self.total_expected_time_per_block,
                           default_difficulty=self.last_difficulty)
        for i in range(1, len(self)+1):
            blocks_at_level = self.blockchain_idx[i]
            for block in blocks_at_level:
                new_blockchain.extend_with_reference(block)
        return new_blockchain
