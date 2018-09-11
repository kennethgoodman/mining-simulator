from Blockchain import Blockchain
from Blockchain import Block
from Strategies.Base.Miner import Miner


def generate_block_on_longest_chain(prev_block, miner):
    return Block([], prev_block.block_time + 1, prev_block, prev_block.block_num + 1, miner)


def create_test_blockchain():
    miner_one = Miner(None, 1, [], 2, 0, None, None)
    miner_two = Miner(None, 1, [], 2, 1, None, None)
    b = Blockchain()
    block_one = generate_block_on_longest_chain(b.last_block[0], miner_one)
    b.extend(block_one)
    b.extend(generate_block_on_longest_chain(b.last_block[0], miner_one))
    edge1 = generate_block_on_longest_chain(b.last_block[0], miner_one)
    b.extend(edge1)
    edge2 = Block([], 2, block_one, 2, miner_two)
    b.extend(edge2)
    return b, edge1, edge2, miner_one, miner_two


def test_creating_edges_correctly():
    """
    create a blockchain:

    1 -> 2 -> 3
      -> 2

    :return:
    """
    b, edge1, edge2, miner_one, miner_two = create_test_blockchain()
    assert len(b.edges) == 2
    assert b.edges[0] == edge1
    assert b.edges[1] == edge2
    assert b.edges[1].previous_block == b.edges[0].previous_block.previous_block

    edge1 = Block([], 4, b.last_block[0], 4, miner_one)
    b.extend(edge1)
    assert b.edges[0] == edge1


def test_copy():
    b, edge1, edge2, miner_one, miner_two = create_test_blockchain()
    b = b.copy()
    assert len(b.edges) == 2
    assert b.edges[0] == edge1
    assert b.edges[1] == edge2
    assert b.edges[1].previous_block == b.edges[0].previous_block.previous_block


def test_add_same_block_again():
    b, edge1, edge2, miner_one, miner_two = create_test_blockchain()
    b.extend_with_reference(edge1)
    assert len(b.edges) == 2
    assert b.edges[0] == edge1
    assert b.edges[0].previous_block == edge1.previous_block


if __name__ == '__main__':
    test_creating_edges_correctly()
    test_copy()
    test_add_same_block_again()
