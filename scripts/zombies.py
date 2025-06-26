import random

from scripts.entities import Entity
from scripts.constants import ZOMBIES_APPEARS

class Zombie(Entity):
    def __init__(self, images, pos):
        super().__init__(images, pos)

    def get_velocity(self):
        return self.velocity

    def get_zombie(self):
        zombie = None
        choices = [key for key in ZOMBIES_APPEARS['map0'].keys()]
        weights = ZOMBIES_APPEARS['map0'].values()
        choosed = random.choices(population=choices, weights=weights)
        print(choosed)
        if choosed == 'zombie_1':
            zombie = Zombie_1(self.images, self.pos)
        elif choosed == 'zombie_2':
            zombie = Zombie_2(self.images, self.pos)

        return zombie

class Zombie_1(Zombie):
    VEL = [-0.1, 0]
    def __init__(self, images, pos):
        super().__init__(images, pos)
        self.velocity = self.VEL

class Zombie_2(Zombie):
    VEL = [-0.2, 0]
    def __init__(self, images, pos):
        super().__init__(images, pos)
        self.velocity = self.VEL


