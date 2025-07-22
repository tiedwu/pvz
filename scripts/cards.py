import random
import pygame

from scripts.constants import (CARD_WIDTH, CARD_HEIGHT, ENERGY_SPACE, \
        MAX_CARD_AMOUNT, PLANT_SELECTION_BATCH, PLANT_SELECTION_X, ZOMBIE_SELECTION_X, ZOMBIE_SELECTION_COLS)
from scripts.utils import (make_card_image, get_plants, get_zombies, cards_by_map, plants_by_id, \
        zombies_by_id, get_pos_from_permutation, get_permutation_from_pos)

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
        card = None
        card_type = 'plants'


        if name:
            cost = get_plants()[name]['cost']
        else:
            name, cost = self._take_card()

        place = self._get_place()

        if place != -1:
            x = ENERGY_SPACE + place * CARD_WIDTH
            pos = (x, 0)
                
            card = Card(pos, name, card_type, cost)

        return place, card

    def make_cards_by_map(self, map):
        choices = []
        cards = cards_by_map(map)
        for card in cards:
            _, got = self._get_card(card)
            choices.append(got)
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

    def remove_card(self, index):
        self.occupied[index] = 0

    def get_zombie_card(self, name, permutation):
        card = Card((0, 0), name, 'zombies', 0)
        card.set_pos(get_pos_from_permutation(card, permutation))
        return card
        #return Card(get_pos_from_permutation(permutation), name, 'zombies', 0)

    def make_zombie_card(self, name, pos):
        _, row, col = get_permutation_from_pos(pos)
        permutation = (row, col)
        card = self.get_zombie_card(name, permutation) 
        return permutation, card


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

    def draw(self, surf, scroll=0):
        pos_x = self.pos[0] - scroll
        surf.blit(self.image, (pos_x, self.pos[1]))

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_pos(self, pos):
        self.pos = pos
