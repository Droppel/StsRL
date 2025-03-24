from stssim.cards.card import Card
from stssim.enemies.enemy import Enemy
from stssim.player import Player

class Defend(Card):
    def __init__(self):
        super().__init__()
        self.cost = 1

    def play(self, player: Player, enemy: Enemy):
        player.block += 5
        return