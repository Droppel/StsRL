from stssim.enemies.enemy import Enemy
from stssim.player import Player

class Card:
    def __init__(self):
        self.cost = 0

    def play(self, player: Player, enemy: Enemy):
        return