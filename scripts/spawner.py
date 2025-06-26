import pygame
import random

from scripts.constants import ROAD_ROWS, ROAD_COLS, ZOMBIE_SPAWN_COL
from scripts.utils import make_object_image, get_pos_from_permutation
from scripts.zombies import Zombie
from scripts.plants import Plant


class Spawner:
    def __init__(self, name='zombie'):
        super().__init__()
        self.name = name
        self.exists = {}
        self.group = pygame.sprite.Group()

    def generate(self):
        max_tries = 3
        tried = 0
        while tried < max_tries:
            row = random.randint(1, ROAD_ROWS)
            if self.name == 'zombie':
                col = random.randint(ROAD_COLS, ZOMBIE_SPAWN_COL)
            elif self.name == 'plant':
                col = random.randint(1, ROAD_COLS)
            permutation = (row, col)
            if permutation not in self.exists:
                images = {}
                image = make_object_image(self.name)
                images['idle'] = [image]
                
                if self.name == 'zombie':
                    zombie = Zombie(images, get_pos_from_permutation(image, permutation))
                    sprite = zombie.get_zombie
                    print(sprite)
                elif self.name == 'plant':
                    sprite = Plant(images, get_pos_from_permutation(image, permutation))
                self.exists[permutation] = sprite
                self.group.add(sprite)
                break
            tried += 1
        
