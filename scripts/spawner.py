import pygame
import random

from scripts.constants import ROAD_ROWS, ROAD_COLS, ZOMBIE_SPAWN_COL
from scripts.zombies import ZombieGenerator

from scripts.plants import PeaShooter, SunFlower, ThornyNut
from scripts.utils import get_permutation_from_pos


class Spawner:
    def __init__(self, name='zombie'):
        super().__init__()
        self.name = name
        self.exists = {}
        self.group = pygame.sprite.Group()

    def make_plant(self, name, pos):
        found, row, col = get_permutation_from_pos(pos)
        permutation = (row, col)
        if name == 'PeaShooter':
            sprite = PeaShooter(permutation)
        elif name == 'SunFlower':
            sprite = SunFlower(permutation)
        elif name == 'ThornyNut':
            sprite = ThornyNut(permutation)
        self.group.add(sprite)

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
                
                if self.name == 'zombie':
                    zombie_generator = ZombieGenerator()
                    sprite = zombie_generator.get_zombie(permutation)
                elif self.name == 'plant':
                    sprite = PeaShooter(permutation)
                #print(sprite)
                self.exists[permutation] = sprite
                self.group.add(sprite)
                break
            tried += 1
        
