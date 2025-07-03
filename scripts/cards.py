import random
import pygame

from scripts.constants import CARD_WIDTH, CARD_HEIGHT, ENERGY_SPACE, MAX_CARD_AMOUNT
from scripts.utils import make_card_image, get_plants, cards_by_map

class Generator:
    def __init__(self):
        self.occupied = [0] * MAX_CARD_AMOUNT

    def get_occupies(self):
        return self.occupied
    
    def _get_card(self, name=None):
        if not name:
            name, cost = self._take_card()
        else:
            cost = cost = get_plants()[name]['cost']
        place = self._get_place()
        if place == -1:
            return None
        x = ENERGY_SPACE + place * CARD_WIDTH
        pos = (x, 0)
        return Card(pos, name, cost)

    def make_cards(self, map):
        cards = cards_by_map(map)
        choices = []
        for card in cards:
            choices.append(self._get_card(card))
        return choices
    
    def _take_card(self):
        plants = get_plants()
        names = list(plants.keys())
        name = random.choice(names)
        cost = plants[name]['cost']
        return name, cost
    
    def _get_place(self):
        for index in range(MAX_CARD_AMOUNT):
            if self.occupied[index] == 0:
                self.occupied[index] = 1
                return index
        return -1

class Card:
    WIDTH = CARD_WIDTH
    HEIGHT = CARD_HEIGHT
    def __init__(self, pos, name, cost):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.image = make_card_image(self.width, self.height, name, cost)
        self.pos = list(pos)
        self.name = name

    def draw(self, surf):
        surf.blit(self.image, self.pos)

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)