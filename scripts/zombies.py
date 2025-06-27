import random

from scripts.entities import Entity
from scripts.constants import ZOMBIES_APPEARS
from scripts.utils import make_object_images

class ZombieGenerator:
    ZOMBIES_APPEARS = ZOMBIES_APPEARS
    def __init__(self, map='map0'):
        self.map = map

    def set_map(self, map):
        self.map = map

    def get_zombie(self, permutation):
        zombie = None
        choices = [key for key in self.ZOMBIES_APPEARS[self.map].keys()]
        weights = self.ZOMBIES_APPEARS['map0'].values()
        choosed = random.choices(population=choices, weights=weights)
        if choosed[0] == 'zombie_1':
            zombie = Zombie_1(permutation)
        elif choosed[0] == 'zombie_2':
            zombie = Zombie_2(permutation)

        return zombie

class Zombie(Entity):
    def __init__(self, permutation, images=make_object_images('zombie')):
        super().__init__(None, permutation, images)

    def get_velocity(self):
        return self.velocity

class Zombie_1(Zombie):
    #IMAGES = {'idle': make_walk_images('zombie', 1), 'walk': make_walk_images('zombie', 1)}
    IMAGES = make_object_images('zombie', 1)
    VEL = [-1, 0]
    ANIMATION_DURATION = 1 * 60
    def __init__(self, permutation):
        super().__init__(permutation, images=self.IMAGES)
        self.velocity = self.VEL
        self.animation_duration = self.ANIMATION_DURATION

class Zombie_2(Zombie):
    #IMAGES = {'idle': [make_object_image('zombie', 2)]}
    #IMAGES = {'idle': make_walk_images('zombie', 2), 'walk': make_walk_images('zombie', 2)}
    IMAGES = make_object_images('zombie', 2)
    VEL = [-2, 0]
    ANIMATION_DURATION = 1 * 60
    def __init__(self, permutation):
        super().__init__(permutation, images=self.IMAGES)
        self.velocity = self.VEL
        self.animation_duration = self.ANIMATION_DURATION


