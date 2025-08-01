import random
import pygame
import pickle

from scripts.constants import (CARD_WIDTH, CARD_HEIGHT, ENERGY_SPACE, SCREEN_WIDTH, \
        MAX_CARD_AMOUNT, PLANT_SELECTION_BATCH, PLANT_SELECTION_X, ZOMBIE_SELECTION_X, ZOMBIE_SELECTION_COLS)
from scripts.utils import (make_card_image, get_plants, get_zombies, cards_by_map, plants_by_id, \
        zombies_by_id, get_pos_from_permutation, get_permutation_from_pos)

class Generator:
    def __init__(self):
        self.occupied = [0] * MAX_CARD_AMOUNT

        # names oreder by id
        self.plant_info = get_plants()
        self.zombie_info = get_zombies()
        self.plants = plants_by_id() # list plants by ID
        self.zombies = zombies_by_id()

        self._designate = {'plants': self._reset_plants(), 'zombies': {}}
        
    def _reset_plants(self):
        plants = {}
        for i in range(MAX_CARD_AMOUNT):
            plants[i] = None
        return plants


    def designate(self):
        return self._designate

    # construct designate from name
    def _parse(self, map_data):
        plant_card_info = {}
        zombie_card_info = {}
        for pos, name in map_data['plant'].items():
            plant_card_info[pos] = self._designate_card('plants', name, pos)

        for pos, name in map_data['zombie'].items():
            zombie_card_info[pos] = self._designate_card('zombies', name, pos)

        self._designate['plants'] = plant_card_info
        self._designate['zombies'] = zombie_card_info


    # place plant Card in empty slot
    def make_plant_card_(self, name):
        plants = self._designate['plants']
        for place, obj in plants.items():
            if obj == None:
                x = ENERGY_SPACE + place * CARD_WIDTH
                pos = (x, 0)
                cost = self.plant_info[name]['cost']
                card = Card(pos, name, 'plants', cost)
                plants[place] = card
                break

        self._designate['plants'] = plants

    # create Card by mouse pos
    def make_zombie_card_(self, name, pos):
        _, row, col = get_permutation_from_pos(pos)
        permutation = (row, col)
         
        card = Card((0, 0), name, 'zombies', 0, 'designate')
        card.set_pos(get_pos_from_permutation(card, permutation))
        self._designate['zombies'][permutation] = card

    def make_cards_(self):
        
        # plants
        plant_cards = []
        for i in range(len(self.plants)):
            cost = self.plant_info[self.plants[i]]['cost']
            x = PLANT_SELECTION_X + (i %  PLANT_SELECTION_BATCH) * CARD_WIDTH
            pos = (x, 0) 
            plant_cards.append(Card(pos, self.plants[i], 'plants', cost))

        # zombies
        zombie_cards = []
        cost = 0
        for i in range(len(self.zombies)):
            # 0 1 2 -> row 0 
            # 0 1 2 -> row 1
            # 0 1 2 -> row 2
            # quotient, remainder = divmod(dividend, divisor)
            quotient, remainder = divmod(i, ZOMBIE_SELECTION_COLS)

            x = ZOMBIE_SELECTION_X + remainder * CARD_WIDTH
            y = CARD_HEIGHT + quotient * CARD_HEIGHT 
            pos = (x, y)

            zombie_cards.append(Card(pos, self.zombies[i], 'zombies', cost))

        return plant_cards, zombie_cards

    def load(self, map):
        pickle_in = open(f'map_{map}', 'rb')
        map_data = pickle.load(pickle_in)

        self._parse(map_data)
        
    def save(self, map):
        #self.card_generator.save(self.map)
        plant_info = {}
        for pos, card in self._designate['plants'].items():
            if card != None:
                plant_info[pos] = card.name

        zombie_info = {}
        for pos, card in self._designate['zombies'].items():
            zombie_info[pos] = card.name

        map_data = {}
        map_data['plant'] = plant_info
        map_data['zombie'] = zombie_info
        pickle_out = open(f'map_{map}', 'wb')
        pickle.dump(map_data, pickle_out)
        pickle_out.close()

    # remove plant card
    def remove_card(self, family, key):
        #self.occupied[index] = 0

        if family == 'plants':
            self._designate['plants'][key] = None
        elif family == 'zombies':
            del self._designate['zombies'][key]

    # make zombie Card by name
    def get_zombie_card(self, name, permutation, action='alternative'):
        card = Card((0, 0), name, 'zombies', 0, action)
        card.set_pos(get_pos_from_permutation(card, permutation))
        return card

    # make plant Card by name
    def get_plant_card(self, name, pos, action='alternative'):
        x = ENERGY_SPACE + pos * CARD_WIDTH
        y = 0
        cost = self.plant_info[name]['cost']
        return Card((x, y), name, 'plants', cost)

    def _designate_card(self, family, name, pos):
        if family == 'plants':
            return self.get_plant_card(name, pos)
        elif family == 'zombies':
            return self.get_zombie_card(name, pos, action='designate')
            


class Card:
    WIDTH = CARD_WIDTH
    HEIGHT = CARD_HEIGHT
    def __init__(self, pos, name, card_type, cost, action='alternative'):
        self.width = self.WIDTH
        self.height = self.HEIGHT
        self.image = make_card_image(card_type, self.width, self.height, name, cost)
        self.pos = list(pos)
        self.name = name
        self.family = card_type
        self.action = action

    #def get_id(self):
    #    return get_plants()[self.name]['id']

    def draw(self, surf, scroll=0):
        pos_x = self.pos[0] - scroll

        draw = False
        if self.action == 'alternative':
            draw = True
        elif self.action == 'designate':
            if pos_x + self.WIDTH < SCREEN_WIDTH:
                draw = True

        if draw:
            surf.blit(self.image, (pos_x, self.pos[1]))

    def get_rect(self):
        return pygame.Rect(*self.pos, self.width, self.height)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def set_pos(self, pos):
        self.pos = pos
