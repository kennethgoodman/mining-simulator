from Blockchain.Blockchain import Blockchain
from Strategies.DefaultCompliant import DefaultStrategy
from Utils.random_util import create_n_random_numbers_that_sum_to_one
from Strategies.Base.Miner import Miner
from Simulation.Simulation import Simulation


def get_random_percents():
    random_percents = create_n_random_numbers_that_sum_to_one(num_miners)
    while any(rp > .4 for rp in random_percents):
        random_percents = create_n_random_numbers_that_sum_to_one(num_miners)
    return random_percents


def get_miner(num_blocks_per_diffculty_adjustment, total_expected_time_per_block, percent, miner_i):
    defaultblockchain1 = Blockchain(num_blocks_per_diffculty_adjustment=num_blocks_per_diffculty_adjustment,
                                    total_expected_time_per_block=total_expected_time_per_block)
    defaultblockchain2 = Blockchain(num_blocks_per_diffculty_adjustment=num_blocks_per_diffculty_adjustment,
                                    total_expected_time_per_block=total_expected_time_per_block)
    miner = Miner(DefaultStrategy(), percent * total_hashes_per_second, [],
                  total_hashes_per_second,
                  miner_i, defaultblockchain1, defaultblockchain2)
    return miner


def get_miners(random_percents, num_blocks_per_diffculty_adjustment, total_expected_time_per_block):
    miners = []
    for miner_i, percent in enumerate(random_percents):
        miners.append(get_miner(num_blocks_per_diffculty_adjustment, total_expected_time_per_block, percent, miner_i))
    return miners


def add_peers_to_miners(miners):
    for i, miner1 in enumerate(miners):
        for j, miner2 in enumerate(miners):
            if i == j:
                continue
            miner1.add_peer(miner2)


if __name__ == '__main__':
    num_miners = 10
    total_hashes_per_second = 50_000
    num_blocks_per_diffculty_adjustment = 2016
    total_expected_time_per_block = 200
    num_rounds = total_expected_time_per_block * 5_000  # 50 blocks
    num_games = 1
    random_percents = get_random_percents()
    miners = get_miners(random_percents, num_blocks_per_diffculty_adjustment, total_expected_time_per_block)
    add_peers_to_miners(miners)
    simul = Simulation(miners, num_rounds, num_games)
    simul.run(block_reward=0)
