from stssim.entity import Entity

class Player(Entity):
    def __init__(self):
        super().__init__()
        self.health = 30
        self.energy = 3