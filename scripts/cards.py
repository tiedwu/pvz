from scripts.constants import CARD_WIDTH, CARD_HEIGHT, ENERGY_SPACE, MAX_CARD_AMOUNT
from scripts.utils import make_card_image

class Generator:
    def __init__(self):
        self.occupied = [0] * MAX_CARD_AMOUNT

    def get_occupies(self):
        return self.occupied
    
    def get_card(self):
        place = self.get_place()
        print(place)
        if place == -1:
            return None
        x = ENERGY_SPACE + place * CARD_WIDTH
        print(x)
        pos = (x, 0)
        name = 'PeaShooter'
        cost = 150
        return Card(pos, name, cost)
    
    def get_place(self):
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

    def draw(self, surf):
        surf.blit(self.image, self.pos)