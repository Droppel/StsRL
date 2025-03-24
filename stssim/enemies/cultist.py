from stssim.enemies.enemy import Enemy
import numpy as np

class Cultist(Enemy):
    # HP: 48-54
    # Attacks:
        # 1. Incantaion: Adds Ritual 3
        # 2. Dark Strike: Deals 6 damage
    # Always starts Incantation

    def __init__(self):
        super().__init__()
        self.health = np.random.randint(48, 55)
        self.block = 0

    def update_intent(self, current_turn):
        if current_turn == 0:
            return 0
        return 1

    def do_turn(self, player):
        if self.intent == 0:
            self.ritual += 3
            return
        if self.intent == 1:
            player.damage(6 + self.strength)
            return