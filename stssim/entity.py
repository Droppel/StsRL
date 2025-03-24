import math

class Entity:
    def __init__(self):
        super().__init__()
        self.health = 0
        self.block = 0
        self.strength = 0
        self.vulnerable = 0
        self.ritual = 0
    
    def damage(self, amount):
        if self.vulnerable > 0:
            amount = math.floor(amount * 1.5)

        if self.block > amount:
            self.block -= amount
            return
        amount -= self.block
        self.block = 0
        self.health -= amount
        return