from stssim.entity import Entity
from stssim.player import Player

class Enemy(Entity):
    def __init__(self):
        super().__init__()
        self.intent = 0

    def update_intent(self, current_turn):
        return 0
    
    def do_turn(self, player: Player):
        pass