import pygame
import random

from scripts.constants import ROAD_ROWS, ROAD_COLS, ZOMBIE_SPAWN_COL
from scripts.zombies import ZombieGenerator

#from scripts.plants import PeaShooter, SunFlower, ThornyNut
from scripts.plants import *
from scripts.zombies import *

from scripts.utils import get_permutation_from_pos, occupied_place


class Spawner:
    def __init__(self, name='zombie'):
        super().__init__()
        self.name = name
        self.exists = {}
        self.group = pygame.sprite.Group()
        self.occupied_ = {}

    def check_empty(self):
        if len(self.group) == 0:
            return True
        return False

    def reset(self):
        self.group.empty()
        self.occupied_ = {}

    def remove_plant(self, plant):
        self.group.remove(plant)
        _, row, col = get_permutation_from_pos(plant.pos)
        #del self.occupied[(row, col)]
        del self.occupied_[(row, col)]

    def make_plant_(self, name, pos):
        _, row, col = get_permutation_from_pos(pos)
        permutation = (row, col)

        success = False
        #print(self.occupied_.keys())
        if permutation not in self.occupied_.keys() and row != -1:
            success = True
            sprite = globals()[name](permutation)
            self.group.add(sprite)
            self.occupied_[permutation] = sprite

        return success

    def make_zombie_(self, name, permutation):
        sprite = globals()[name](permutation)
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
                self.occupied[permutation] = 1
                self.group.add(sprite)
                break
            tried += 1
        
