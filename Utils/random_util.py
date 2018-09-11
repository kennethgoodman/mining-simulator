import random
from math import exp
from Blockchain.Transaction import Transaction
from Utils.Constants import SATOSHIS_PER_BITCOIN


def create_n_random_numbers_that_sum_to_one(n):
    random_numbers = [random.random() for _ in range(n)]
    total = sum(random_numbers)
    return [1.0 * x / total for x in random_numbers]


def create_random_transaction():
    size = random.randint(150, 180)  # between 150 and 1000 bytes
    tx_fee = int(size * max(1, random.gauss(4, 3.3)))  # min(1, N(4, 3.3))
    return Transaction(size, tx_fee)


def generate_random_transactions(num=5):
    txs = []
    for tx_i in range(num):
        txs.append(create_random_transaction())
    return txs


def probability_of_finding_block_in_x_seconds(x, average_seconds_per_block=600):
    return 1 - exp(-x / average_seconds_per_block)


def probability_of_finding_block_in_1_second(average_seconds_per_block=600):
    return probability_of_finding_block_in_x_seconds(1, average_seconds_per_block=average_seconds_per_block)


def probability_finding_blocks_test():
    def trial():
        i = 0
        r = probability_of_finding_block_in_1_second(average_seconds_per_block=600)
        while True:
            i += 1
            if random.random() <= r:
                return i
    trials = [trial() for _ in range(500_000)]
    average_block_time = sum(trials) / len(trials)
    assert abs(average_block_time - 600) <= 2, \
        "Must be within 2 seconds of 10 minutes, average_block_time={}".format(average_block_time)


def probability_of_individual_finding_block(proportion: float, average_time_for_blocks=600) -> float:
    return probability_of_finding_block_in_1_second(average_time_for_blocks) * proportion


cache = {}
def found_block(proportion, average_time_for_blocks=600):
    global cache
    if (proportion,average_time_for_blocks) not in cache:
        p = probability_of_individual_finding_block(proportion,average_time_for_blocks=average_time_for_blocks)
        cache[(proportion,average_time_for_blocks)] = p
    return random.random() <= cache[(proportion,average_time_for_blocks)]


def probability_finding_blocks_multiple_agents_test():
    def trial():
        while True:
            winners = []
            for miner_idx, r in enumerate(rs):  # can have multiple winners
                if random.random() <= r:
                    winners.append(miner_idx)
            if len(winners):
                return winners

    number_of_agents = 10
    proportions = create_n_random_numbers_that_sum_to_one(number_of_agents)
    rs = list(map(probability_of_individual_finding_block, proportions))
    winner_count = [0 for _ in range(number_of_agents)]

    for _ in range(50_000):
        winners = trial()
        for winner in winners:
            winner_count[winner] += 1

    winner_count = [x / sum(winner_count) for x in winner_count]  # normalize it

    for min_win_perc, miner_proportio in zip(winner_count, proportions):
        assert abs(min_win_perc - miner_proportio) < .01 / number_of_agents, \
            "Not within {}% error: winner_count={}, proportions={}".format(1/number_of_agents, winner_count, proportions)


if __name__ == '__main__':
    # probability_finding_blocks_multiple_agents_test()
    probability_finding_blocks_test()
    assert sum(create_n_random_numbers_that_sum_to_one(5)) == 1