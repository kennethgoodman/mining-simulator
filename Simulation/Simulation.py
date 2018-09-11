from Strategies.Base.Miner import Miner
from typing import List
from Simulation import Game
from Utils.Constants import SATOSHIS_PER_BITCOIN


class Simulation:
    def __init__(self, miners: List[Miner], num_rounds: int, num_games: int):
        self.miners = miners
        self.num_rounds = num_rounds
        self.num_games = num_games

    def run(self, block_reward=50*SATOSHIS_PER_BITCOIN):
        for game_i in range(self.num_games):
            game = Game(self.miners, self.num_rounds)
            game.run_game(block_reward=block_reward)
