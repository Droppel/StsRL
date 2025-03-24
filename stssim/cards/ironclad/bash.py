from stssim.cards.card import Card
from stssim.enemies.enemy import Enemy
from stssim.player import Player

class Bash(Card):
    def __init__(self):
        super().__init__()
        self.cost = 2

    def play(self, player: Player, enemy: Enemy):
        enemy.damage(8)
        enemy.vulnerable += 2
        return