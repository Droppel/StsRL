class Entity:
    def __init__(self):
        super().__init__()
        self.health = 0
        self.block = 0
        self.strength = 0
        self.vulnerable = 0
    
    def damage(self, amount):
        if self.block > amount:
            self.block -= amount
            return
        amount -= self.block
        self.block = 0
        self.health -= amount
        return