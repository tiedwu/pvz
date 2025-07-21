import random
import pygame

from scripts.constants import (CARD_WIDTH, CARD_HEIGHT, ENERGY_SPACE, \
        MAX_CARD_AMOUNT, PLANT_SELECTION_BATCH, PLANT_SELECTION_X, ZOMBIE_SELECTION_X, ZOMBIE_SELECTION_COLS)
from scripts.utils import make_card_image, get_plants, get_zombies, cards_by_map, plants_by_id, zombies_by_id

class Generator:
    def __init__(self):
        self.occupied = [0] * MAX_CARD_AMOUNT

        #self.plants = self.make_cards('plants')
        #self.zombies = self.make_cards('zombies')
        
        # names oreder by id
        self.plant_info = get_plants()
        self.zombie_info = get_zombies()
        self.plants = plants_by_id()
        self.zombies = zombies_by_id()

    def get_cards(self):
        return self._get_cards('plants'), self._get_cards('zombies')

    def _get_cards(self, card_type):
        choices = []
        if card_type == 'plants':
            objs = self.plants
        elif card_type == 'zombies':
            objs = self.zombies

        for i in range(len(objs)):
            if card_type == 'plants':
                cost = self.plant_info[objs[i]]['cost']
                x = PLANT_SELECTION_X + (i %  PLANT_SELECTION_BATCH) * CARD_WIDTH

                pos = (x, 0)
            elif card_type == 'zombies':
                cost = 0
                # 0 1 2 -> row 0 
                # 0 1 2 -> row 1
                # 0 1 2 -> row 2
                # quotient, remainder = divmod(dividend, divisor)
                quotient, remainder = divmod(i, ZOMBIE_SELECTION_COLS)

                x = ZOMBIE_SELECTION_X + remainder * CARD_WIDTH
                y = CARD_HEIGHT + quotient * CARD_HEIGHT 
                pos = (x, y)

            choices.append(Card(pos, objs[i], card_type, cost))

        return choices   

    def get_occupies(self):
        return self.occupied


    def get_card_in_box(self, card):
        return self._get_card(card, placement='box')

    def _get_card(self, name=None, placement='box'):
        if not name:
            name, cost = self._take_card()

        if placement == 'box':
            place = self._get_place()
            card_type = 'plants'
            cost = get_plants()[name]['cost']
            if place == -1:
                return None

            x = ENERGY_SPACE + place * CARD_WIDTH
            pos = (x, 0)

        return Card(pos, name, card_type, cost)

    def make_cards_by_map(self, map):
        choices = []
        cards = cards_by_map(map)
        for card in cards:
            choices.append(self._get_card(card, placement='box'))
        return choices

    def _take_card(self):
        plants = get_plants()
        names = list(plants.keys())
        name = random.choice(names)
        cost = plants[name]['cost']
        return name, cost
    
    def _get_place(self):
        for index in range(len(self.occupied)):
            if self.occupied[index] == 0:
                self.occupied[index] = 1
                return index
        return -1

class Card:
    WIDTH = CARD_WIDTH
    HEIGHT = CARD_HEIGHT
    def __init__(self, pos, name, card_type, cost):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.image = make_card_image(card_type, self.width, self.height, name, cost)
        self.pos = list(pos)
        self.name = name
        self.family = card_type

    def get_id(self):
        return get_plants()[self.name]['id']

    def draw(self, surf):
        surf.blit(self.image, self.pos)

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)
