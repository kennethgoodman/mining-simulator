from Strategies import Miner


def trial(miners):
    blocks_found = [0 for _ in miners]
    for x in range(500_000):
        for i, miner in enumerate(miners):
            blocks_found[i] += miner.found_block()
    return blocks_found


def set_up():
    proportions = [.14, .1, .05, .3, .2, .01, .15, .05]
    tp = 10_000
    miners = []
    class mock_blockchain: total_expected_time_per_block=600
    for i, p in enumerate(proportions):
        miner = Miner(None, int(p * tp), None, tp, i, mock_blockchain, mock_blockchain)
        miners.append(miner)
    return miners, proportions


def run_test():
    miners, proportions = set_up()
    blocks_found = trial(miners)
    s = sum(blocks_found)
    for miner, bfs, p in zip(miners, blocks_found, proportions):
        print("Miner", miner.number, "with proportion", miner.hashpower_proportion, "found", bfs, "blocks.",
              "Total proportion of all rewards is", bfs / s, "with intended proportion", p)


if __name__ == '__main__':
    run_test()