from stssim.enemies.enemy import Enemy
import numpy as np

class Cultist(Enemy):
    # HP: 50-56
    # Attacks:
        # 1. Incantaion: Adds Ritual 5
        # 2. Dark Strike: Deals 6 damage
    # Always starts Incantation

    def __init__(self):
        super().__init__()
        self.health = np.random.randint(50, 57)
        self.block = 0

    def update_intent(self, current_turn):
        if current_turn == 0:
            return 0
        return 1

    def do_turn(self, player):
        if self.intent == 0:
            self.ritual += 5
            return
        if self.intent == 1:
            player.damage(6 + self.strength)
            return