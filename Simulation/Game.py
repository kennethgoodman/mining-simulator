from Strategies.Base.Miner import Miner
from typing import List
from Utils.random_util import generate_random_transactions
from Utils.Constants import SATOSHIS_PER_BITCOIN

import time


def normalize_list(aList):
    s = sum(aList)
    return [x/s for x in aList]


class Game:
    def __init__(self, miners: List[Miner], num_rounds: int):
        self.miners = miners
        self.num_rounds = num_rounds

    def calculate_and_log_results(self, block_reward):
        chain = self.miners[0].published_chain
        rewards = [0 for _ in self.miners]
        total_number_of_blocks = [0 for _ in self.miners]
        for block in chain.iterate_backwards(chain.last_block[0]):
            if block.block_num == 0:  # at genesis block
                break
            rewards[block.miner.number] += block_reward + block.value_of_all_transactions
            total_number_of_blocks[block.miner.number] += 1
        proportions = [miner.hashpower_proportion for miner in self.miners]
        rewards = normalize_list(rewards)
        total_number_of_blocks = normalize_list(total_number_of_blocks)
        for miner_i, (miner_r, miner_p, miner_bt) in enumerate(zip(rewards, proportions, total_number_of_blocks)):
            print("Miner", miner_i, "with proportion of hashpower", miner_p, "got ", miner_r,
                  "perecent of all rewards and", miner_bt, "percent of all blocks")

    def run_game(self, block_reward=50 * SATOSHIS_PER_BITCOIN):
        start = time.time()
        last = start
        for round_i in range(self.num_rounds):
            if round_i % 100 == 0 and round_i != 0:
                new_last = time.time()
                time_since_start = round(new_last - start, 1)
                time_since_last = round(new_last - last, 1)
                print("starting round", round_i, "there are currently", len(self.miners[0].published_chain), "blocks.",
                      time_since_start, "seconds since we started.", time_since_last, "seconds for the last 100 blocks.",
                      "Average time per block", round(time_since_start / round_i, 5))
                last = new_last
            self.run_round(round_i)
        self.calculate_and_log_results(block_reward)
        print("There were {} forks".format(len(self.miners[0].my_chain.edges)))


    def run_round(self, current_time):
        if max(len(miner.mempool) for miner in self.miners) < 1500:  # cap transactions for efficiency
            txs = generate_random_transactions(num=1)
            for miner in self.miners:
                # TODO: include only sending txs to some miners
                miner.add_txs_to_mempool(txs)

        for miner in self.miners:
            miner.run_mining_round(current_time)

        for miner in self.miners:
            miner.run_publish_round()
            # TODO: add random nodes - strategy can be to add nodes throughout the network and to not publish to miners
