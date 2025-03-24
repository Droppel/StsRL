from stssim.enemies.enemy import Enemy
import numpy as np

class JawWorm(Enemy):
    # HP: 42-46
    # Attacks:
        # 1. Bellow: + 5 strength, block 9
        # 2. Trash: block 5, deal 7 damage
        # 3. Chomp: deal 12 damage
    # Always starts with Chomp

    def __init__(self):
        super().__init__()
        self.health = np.random.randint(42, 47)
        self.block = 0
        self.attack_counts = [0, 0, 0]

    def update_intent(self, current_turn):
        if current_turn == 0:
            self.attack_counts = [0, 0, 1]
            return 2
        
        selected_intent = 0
        if self.attack_counts[0] > 1:
            selected_intent = 1 if np.random.randint(55) < 35 else 2
        elif self.attack_counts[1] > 2:
            selected_intent = 0 if np.random.randint(70) < 45 else 2
        elif self.attack_counts[2] > 1:
            selected_intent = 0 if np.random.randint(75) < 45 else 1
        else:
            selected_intent = np.random.choice([0, 1, 2], p=[0.45, 0.30, 0.25])
        self.attack_counts = [0 if i != selected_intent else self.attack_counts[i] for i in range(len(self.attack_counts))]
        self.intent = selected_intent
        return

    def do_turn(self, player):
        if self.intent == 0:
            self.block += 9
            self.strength += 5
            return
        if self.intent == 1:
            self.block += 5
            player.damage(7 + self.strength)
            return
        if self.intent == 2:
            player.damage(12 + self.strength)
            return